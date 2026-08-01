"""Time expression parsing module.

Provides `AbstractTimeExprParser`, an abstract base parser for extracting time expressions (e.g. "1:30", "1:30am", "1:30-2:10pm").

Overridable Pattern Templates:
- `PRIMARY_TIME_PATTERN_TEMPLATE`: Primary regex template for matching initial time expressions.
- `FOLLOWING_TIME_PATTERN_TEMPLATE`: Following regex template for matching range end times (e.g., "- 2:10pm").

Subclasses may override `get_primary_time_pattern_template()` and `get_following_time_pattern_template()` to supply
custom templates (or override `primary_prefix()`, `primary_suffix()`, `following_phase()`, `following_suffix()`,
and `get_am_pm_pattern()`).

IMPORTANT FOR SUBCLASSES:
When overriding template strings, subclasses MUST preserve the capturing group index convention:
- Group 1: Left boundary / prefix or following phase connector
- Group 2: Hour
- Group 3: Minute (optional)
- Group 4: Second (optional)
- Group 5: Millisecond (optional)
- Group 6: AM/PM indicator (optional)
"""

import re
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment, DateTimePrecision
from chrono_python.utils.re import Match

HOUR_GROUP = 2
MINUTE_GROUP = 3
SECOND_GROUP = 4
MILLI_SECOND_GROUP = 5
AM_PM_HOUR_GROUP = 6

# Default primary time expression pattern template with placeholders:
#   <primary_prefix>, <primary_suffix>, and <am_pm_pattern>.
# Returned by `AbstractTimeExprParser.get_primary_time_pattern_template()`.
#
# Used by `get_primary_time_pattern_through_cache()` to compile `pattern()` by replacing placeholders.
#
# IMPORTANT FOR SUBCLASSES: Subclasses overriding this template must maintain the capturing group ordering:
#   Group 1: Left boundary & prefix (e.g., "at", "from")
#   Group 2: Hour
#   Group 3: Minute (optional)
#   Group 4: Second (optional)
#   Group 5: Millisecond (optional)
#   Group 6: AM/PM (optional)
PRIMARY_TIME_PATTERN_TEMPLATE = (
    r"<primary_prefix>"                      # Left boundary & prefix (e.g., "at", "from")
    r"(\d{1,4})"                              # Hour (1-4 digits, handles 24h or HHMM)
    r"(?:"
        r"(?:\.|:|：)"                        # Hour-minute separator (., :, or full-width colon)
        r"(\d{1,2})"                          # Minute
        r"(?:"
            r"(?::|：)"                       # Minute-second separator (: or full-width colon)
            r"(\d{2})"                        # Second
            r"(?:\.(\d{1,6}))?"               # Millisecond (1-6 digits)
        r")?"
    r")?"
    r"(?:\s*<am_pm_pattern>)?"                # AM/PM indicator (optional, with optional leading space)
    r"<primary_suffix>"                       # Suffix constraint (optional o'clock/night/etc.)
)

# Default following time expression pattern template (for date/time ranges) with placeholders:
#   <following_phase>, <following_suffix>, and <am_pm_pattern>.
# Returned by `AbstractTimeExprParser.get_following_time_pattern_template()`.
#
# Used by `get_following_time_pattern_through_cache()` to extract range end components.
#
# IMPORTANT FOR SUBCLASSES: Subclasses overriding this template must maintain the capturing group ordering:
#   Group 1: Following phase/connector (e.g., "-", "to", "until")
#   Group 2: Hour
#   Group 3: Minute (optional)
#   Group 4: Second (optional)
#   Group 5: Millisecond (optional)
#   Group 6: AM/PM (optional)
FOLLOWING_TIME_PATTERN_TEMPLATE = (
    r"^"                                      # Anchor to the beginning of the remaining text
    r"(<following_phase>)"                    # Phase connector matching group
    r"(\d{1,4})"                              # Hour
    r"(?:"
        r"(?:\.|\:|：)"                       # Hour-minute separator
        r"(\d{1,2})"                          # Minute
        r"(?:"
            r"(?:\.|\:|：)"                   # Minute-second separator
            r"(\d{1,2})(?:\.(\d{1,6}))?"       # Second and optional millisecond
        r")?"
    r")?"
    r"(?:\s*<am_pm_pattern>)?"                # AM/PM indicator
    r"<following_suffix>"                     # Suffix constraint
)


class AbstractTimeExprParser(chrono.Parser):
    """Abstract base parser that extracts common time expressions (e.g. 1:30, 1:30am, 1:30-2:10pm).

    This parser handles standard time expressions, mostly in English but adaptable.
    Sub-classes or specialized implementations can override the prefix/suffix/between pattern templates.
    """

    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self._cached_primary_time_pattern = None
        self._cached_following_time_pattern = None

    def get_primary_time_pattern_template(self) -> str:
        return PRIMARY_TIME_PATTERN_TEMPLATE

    def get_following_time_pattern_template(self) -> str:
        return FOLLOWING_TIME_PATTERN_TEMPLATE

    def get_am_pm_pattern(self) -> str:
        return r"(a\.m\.|p\.m\.|am?|pm?)"

    def primary_prefix(self) -> str:
        # Roll left boundary constraints directly into the prefix
        return r"(^|\s|T|\b)"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|to)\s*"

    def primary_suffix(self) -> str:
        return r"(?!/)(?=\W|$)"

    def following_suffix(self) -> str:
        return r"(?!/)(?=\W|$)"

    def pattern_flags(self) -> re.RegexFlag:
        return re.IGNORECASE

    def pattern(self) -> re.Pattern:
        return self.get_primary_time_pattern_through_cache()

    def get_primary_time_pattern_through_cache(self) -> re.Pattern:
        if self._cached_primary_time_pattern is not None:
            return self._cached_primary_time_pattern

        primary_prefix = self.primary_prefix()
        primary_suffix = self.primary_suffix()
        am_pm_pattern = self.get_am_pm_pattern()
        pattern_str = (
            self.get_primary_time_pattern_template()
            .replace("<primary_prefix>", primary_prefix)
            .replace("<primary_suffix>", primary_suffix)
            .replace("<am_pm_pattern>", am_pm_pattern)
        )
        self._cached_primary_time_pattern = re.compile(pattern_str, self.pattern_flags())
        return self._cached_primary_time_pattern

    def get_following_time_pattern_through_cache(self) -> re.Pattern:
        if self._cached_following_time_pattern is not None:
            return self._cached_following_time_pattern

        following_phase = self.following_phase()
        following_suffix = self.following_suffix()
        am_pm_pattern = self.get_am_pm_pattern()
        pattern_str = (
            self.get_following_time_pattern_template()
            .replace("<following_phase>", following_phase)
            .replace("<following_suffix>", following_suffix)
            .replace("<am_pm_pattern>", am_pm_pattern)
        )
        self._cached_following_time_pattern = re.compile(pattern_str, re.IGNORECASE)
        return self._cached_following_time_pattern

    def extract(self, context: chrono.ParsingContext, match: Match) -> chrono.ParsedResult | Moment | None:
        start_moment = self.extract_primary_time_components(context, match)
        if start_moment is None:
            return None

        # match.group(1) is the left boundary group
        boundary_len = len(match.group(1) or "")
        index = match.start() + boundary_len
        text = match.group(0)[boundary_len:]

        result = context.create_parsed_result(index, index + len(text), start_moment)

        # Skip over potential overlapping patterns, similar to match.index updating in JS
        remaining_index = match.end()
        remaining_text = context.text[remaining_index:]

        following_pattern = self.get_following_time_pattern_through_cache()
        following_match = following_pattern.match(remaining_text)

        # Pattern "456-12", "2022-12" should not be time without proper context
        if re.match(r'^\d{3,4}', text) and following_match:
            following_text = following_match.group(0)
            if re.match(r'^\s*([+-])\s*\d{2,4}$', following_text):
                return None
            if re.match(r'^\s*([+-])\s*\d{2}\W\d{2}', following_text):
                return None

        if not following_match or re.match(r'^\s*([+-])\s*\d{3,4}$', following_match.group(0)):
            return self.check_and_return_without_following_pattern(result)

        following_match_obj = Match.from_re_match(following_match)
        end_moment = self.extract_following_time_components(context, following_match_obj, result)
        if end_moment:
            end_index = remaining_index + len(following_match.group(0))
            range_result = context.create_parsed_result(index, end_index, start_moment, end_moment)
            return self.check_and_return_with_following_pattern(range_result)
        else:
            return self.check_and_return_without_following_pattern(result)

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = ParsingCivilTimeMoment.of(context.reference)
        minute = 0
        meridiem = None

        # ----- Hours
        hour_str = match.group(HOUR_GROUP)
        if hour_str is None:
            return None
        hour = int(hour_str)

        minute_str = match.group(MINUTE_GROUP)
        ampm_str = match.group(AM_PM_HOUR_GROUP)

        # Check for dot separator ambiguity (e.g. version/decimal numbers like 1.12 or 12.10)
        match_str = match.group(0)
        if minute_str is not None:
            hour_idx = match_str.find(hour_str)
            if hour_idx != -1:
                sep_start = hour_idx + len(hour_str)
                sep_end = match_str.find(minute_str, sep_start)
                if sep_start < sep_end:
                    separator = match_str[sep_start:sep_end]
                    if '.' in separator:
                        # Separator is a dot. Reject if there's no clear time context.
                        has_time_context = False
                        if ampm_str is not None:
                            has_time_context = True
                        elif any(word in match_str.lower() for word in ["night", "afternoon", "morning", "clock", "h", "heures"]):
                            has_time_context = True
                        elif re.search(r'\b(?:at|from|à|a|de)\b', match_str[:hour_idx].lower()):
                            has_time_context = True

                        if not has_time_context:
                            return None

        # Check for single number ambiguity (e.g. "12" in "Version 1.12", or just a plain number "12")
        if minute_str is None:
            has_time_context = False
            if ampm_str is not None:
                has_time_context = True
            elif any(word in match_str.lower() for word in ["night", "afternoon", "morning", "clock", "h", "heures"]):
                has_time_context = True
            else:
                hour_idx = match_str.find(hour_str)
                if hour_idx != -1 and re.search(r'\b(?:at|from|à|a|de)\b', match_str[:hour_idx].lower()):
                    has_time_context = True

            if not has_time_context:
                return None

        if hour > 100:
            # When time is like '2019', it is more likely a year.
            # Especially if there is no minute part and no am/pm.
            if len(hour_str) == 4 and minute_str is None and ampm_str is None:
                return None

            if self.strict_mode or minute_str is not None:
                return None

            minute = hour % 100
            hour = hour // 100

        if hour > 24:
            return None

        # ----- Minutes
        if minute_str is not None:
            if len(minute_str) == 1 and ampm_str is None:
                # Skip single digit minute e.g. "at 1.1 xx"
                return None
            minute = int(minute_str)

        if minute >= 60:
            return None

        if hour > 12:
            meridiem = Meridiem.PM

        # ----- AM & PM
        if ampm_str is not None:
            if hour > 12:
                return None
            ampm = ampm_str[0].lower()
            if ampm == 'a':
                meridiem = Meridiem.AM
                if hour == 12:
                    hour = 0
            elif ampm in ('p', 'm'):
                meridiem = Meridiem.PM
                if hour != 12:
                    hour += 12

        components.assign(CivilTimeComponent.HOUR, hour)
        components.assign(CivilTimeComponent.MINUTE, minute)

        if meridiem is not None:
            components.assign(CivilTimeComponent.MERIDIEM, meridiem)
        else:
            if hour < 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            else:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

        # ----- Millisecond
        millisecond_str = match.group(MILLI_SECOND_GROUP)
        if millisecond_str is not None:
            millisecond = int(millisecond_str[:3])
            if millisecond >= 1000:
                return None
            components.assign(CivilTimeComponent.MILLI_SECOND, millisecond)

        # ----- Second
        second_str = match.group(SECOND_GROUP)
        if second_str is not None:
            second = int(second_str)
            if second >= 60:
                return None
            components.assign(CivilTimeComponent.SECOND, second)



        # Imply year, month, day from reference
        ref_dt = context.reference.datetime()
        components.imply(CivilTimeComponent.YEAR, ref_dt.year)
        components.imply(CivilTimeComponent.MONTH, ref_dt.month)
        components.imply(CivilTimeComponent.DAY, ref_dt.day)

        return components

    def extract_following_time_components(
        self, context: chrono.ParsingContext, match: Match, result: chrono.ParsedResult
    ) -> ParsingCivilTimeMoment | None:
        components = ParsingCivilTimeMoment.of(context.reference)

        # ----- Millisecond
        millisecond_str = match.group(MILLI_SECOND_GROUP)
        if millisecond_str is not None:
            millisecond = int(millisecond_str[:3])
            if millisecond >= 1000:
                return None
            components.assign(CivilTimeComponent.MILLI_SECOND, millisecond)

        # ----- Second
        second_str = match.group(SECOND_GROUP)
        if second_str is not None:
            second = int(second_str)
            if second >= 60:
                return None
            components.assign(CivilTimeComponent.SECOND, second)

        hour_str = match.group(HOUR_GROUP)
        if hour_str is None:
            return None
        hour = int(hour_str)
        minute = 0
        meridiem = None

        # ----- Minute
        minute_str = match.group(MINUTE_GROUP)
        if minute_str is not None:
            minute = int(minute_str)
        elif hour > 100:
            minute = hour % 100
            hour = hour // 100

        if minute >= 60 or hour > 24:
            return None

        if hour >= 12:
            meridiem = Meridiem.PM

        # Helper to imply next day safely
        def imply_next_day(moment_to_imply):
            ref_dt = context.reference.datetime()
            y = moment_to_imply.get(CivilTimeComponent.YEAR) or ref_dt.year
            m = moment_to_imply.get(CivilTimeComponent.MONTH) or ref_dt.month
            d_val = moment_to_imply.get(CivilTimeComponent.DAY) or ref_dt.day
            from datetime import date, timedelta
            try:
                next_date = date(y, m, d_val) + timedelta(days=1)
                moment_to_imply.imply(CivilTimeComponent.DAY, next_date.day)
                moment_to_imply.imply(CivilTimeComponent.MONTH, next_date.month)
                moment_to_imply.imply(CivilTimeComponent.YEAR, next_date.year)
            except ValueError:
                pass

        # ----- AM & PM
        ampm_str = match.group(AM_PM_HOUR_GROUP)
        if ampm_str is not None:
            if hour > 12:
                return None

            ampm = ampm_str[0].lower()
            if ampm == "a":
                meridiem = Meridiem.AM
                if hour == 12:
                    hour = 0
                    if not components.is_certain(CivilTimeComponent.DAY):
                        imply_next_day(components)

            elif ampm == "p":
                meridiem = Meridiem.PM
                if hour != 12:
                    hour += 12

            if not result.moment.is_certain(CivilTimeComponent.MERIDIEM):
                if meridiem == Meridiem.AM:
                    result.moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                    if result.moment.get(CivilTimeComponent.HOUR) == 12:
                        result.moment.assign(CivilTimeComponent.HOUR, 0)
                else:
                    result.moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                    if result.moment.get(CivilTimeComponent.HOUR) != 12:
                        result.moment.assign(
                            CivilTimeComponent.HOUR,
                            result.moment.get(CivilTimeComponent.HOUR) + 12
                        )

        components.assign(CivilTimeComponent.HOUR, hour)
        components.assign(CivilTimeComponent.MINUTE, minute)

        if meridiem is not None:
            components.assign(CivilTimeComponent.MERIDIEM, meridiem)
        else:
            start_at_pm = (
                result.moment.is_certain(CivilTimeComponent.MERIDIEM) and
                result.moment.get(CivilTimeComponent.HOUR) > 12
            )
            if start_at_pm:
                if result.moment.get(CivilTimeComponent.HOUR) - 12 > hour:
                    # 10pm - 1 (am)
                    components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                elif hour <= 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            elif hour > 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            elif hour <= 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        # Imply year, month, day from reference
        ref_dt = context.reference.datetime()
        components.imply(CivilTimeComponent.YEAR, ref_dt.year)
        components.imply(CivilTimeComponent.MONTH, ref_dt.month)
        components.imply(CivilTimeComponent.DAY, ref_dt.day)

        if components.datetime() < result.moment.datetime():
            imply_next_day(components)

        return components

    def check_and_return_without_following_pattern(self, result: chrono.ParsedResult) -> chrono.ParsedResult | None:
        # Single digit (e.g "1") should not be counted as time expression (without proper context)
        if re.match(r'^\d$', result.text):
            return None

        # Three or more digit (e.g. "203", "2014") should not be counted as time expression (without proper context)
        if re.match(r'^\d\d\d+$', result.text):
            return None

        # Instead of "am/pm", it ends with "a" or "p" (e.g "1a", "123p"), this seems unlikely
        if re.search(r'\d[apAP]$', result.text):
            return None

        # If it ends only with numbers or dots
        ending_with_numbers = re.search(r'[^\d:.](\d[\d.]+)$', result.text)
        if ending_with_numbers:
            ending_numbers = ending_with_numbers.group(1)

            # In strict mode (e.g. "at 1" or "at 1.2"), this should not be accepted
            if self.strict_mode:
                return None

            # If it ends only with dot single digit, e.g. "at 1.2"
            if '.' in ending_numbers and not re.match(r'\d(\.\d{2})+$', ending_numbers):
                return None

            # If it ends only with numbers above 24, e.g. "at 25"
            ending_number_val = int(ending_numbers.split('.')[0])
            if ending_number_val > 24:
                return None

        return result

    def check_and_return_with_following_pattern(self, result: chrono.ParsedResult) -> chrono.ParsedResult | None:
        if re.match(r'^\d+-\d+$', result.text):
            return None

        # If it ends only with numbers or dots
        ending_with_numbers = re.search(r'[^\d:.](\d[\d.]+)\s*-\s*(\d[\d.]+)$', result.text)
        if ending_with_numbers:
            # In strict mode (e.g. "at 1-3" or "at 1.2 - 2.3"), this should not be accepted
            if self.strict_mode:
                return None

            starting_numbers = ending_with_numbers.group(1)
            ending_numbers = ending_with_numbers.group(2)

            # If it ends only with dot single digit, e.g. "at 1.2"
            if '.' in ending_numbers and not re.match(r'\d(\.\d{2})+$', ending_numbers):
                return None

            # If it ends only with numbers above 24, e.g. "at 25"
            ending_number_val = int(ending_numbers.split('.')[0])
            starting_number_val = int(starting_numbers.split('.')[0])
            if ending_number_val > 24 or starting_number_val > 24:
                return None

        return result
