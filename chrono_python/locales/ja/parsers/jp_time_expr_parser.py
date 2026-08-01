import re
from datetime import date, timedelta

from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import (
    AbstractTimeExprParser,
    HOUR_GROUP,
    MINUTE_GROUP,
    SECOND_GROUP,
    MILLI_SECOND_GROUP,
    AM_PM_HOUR_GROUP,
)
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.locales.ja.constants import NUMBER, ja_string_to_number
from chrono_python.utils.patterns import to_hankaku
from chrono_python.utils.re import Match

KJS = "".join(NUMBER.keys())

# Primary time pattern template for Japanese.
# Note: Capturing group indices must strictly follow AbstractTimeExprParser base class:
#   Group 1: Prefix (<primary_prefix>)
#   Group 2: Hour ([0-9０-９]+|[" + KJS + r"]+)
#   Group 3: Minute ([0-9０-９]+|半|[" + KJS + r"]+)
#   Group 4: Second ([0-9０-９]+|[" + KJS + r"]+)
#   Group 5: Millisecond (\d{1,6})
#   Group 6: AM/PM (<am_pm_pattern>)
PRIMARY_TIME_PATTERN_TEMPLATE = (
    r"<primary_prefix>"
    r"(?:(?:午前|午後|A\.M\.|P\.M\.|AM|PM)[\s,，、]*)?"
    r"([0-9０-９]+|[" + KJS + r"]+)"                  # Hour
    r"(?:\s*)(?:時(?!間)|:|：)"
    r"(?:"
        r"\s*"
        r"([0-9０-９]+|半|[" + KJS + r"]+)"            # Minute
        r"(?:\s*)(?:分|:|：)?"
    r")?"
    r"(?:"
        r"\s*"
        r"([0-9０-９]+|[" + KJS + r"]+)"              # Second
        r"(?:\s*)(?:秒)?"
    r")?"
    r"(?:\.(\d{1,6}))?"                               # Millisecond
    r"(?:\s*<am_pm_pattern>)?"                        # AM/PM
    r"<primary_suffix>"
)

# Following time pattern template for Japanese range expressions.
# Note: Capturing group indices must strictly follow AbstractTimeExprParser base class:
#   Group 1: Following phase connector (<following_phase>)
#   Group 2: Hour ([0-9０-９]+|[" + KJS + r"]+)
#   Group 3: Minute ([0-9０-９]+|半|[" + KJS + r"]+)
#   Group 4: Second ([0-9０-９]+|[" + KJS + r"]+)
#   Group 5: Millisecond (\d{1,6})
#   Group 6: AM/PM (<am_pm_pattern>)
FOLLOWING_TIME_PATTERN_TEMPLATE = (
    r"^"
    r"(<following_phase>)"                           # Phase connector matching group
    r"(?:(?:午前|午後|A\.M\.|P\.M\.|AM|PM)[\s,，、]*)?"
    r"([0-9０-９]+|[" + KJS + r"]+)"                  # Hour
    r"(?:\s*)(?:時(?!間)|:|：)"
    r"(?:"
        r"\s*"
        r"([0-9０-９]+|半|[" + KJS + r"]+)"            # Minute
        r"(?:\s*)(?:分|:|：)?"
    r")?"
    r"(?:"
        r"\s*"
        r"([0-9０-９]+|[" + KJS + r"]+)"              # Second
        r"(?:\s*)(?:秒)?"
    r")?"
    r"(?:\.(\d{1,6}))?"                               # Millisecond
    r"(?:\s*<am_pm_pattern>)?"                        # AM/PM
    r"<following_suffix>"
)


def parse_ja_number(str_val: str | None) -> int | None:
    if str_val is None:
        return None
    try:
        return int(to_hankaku(str_val))
    except ValueError:
        return ja_string_to_number(str_val)


class JPTimeExprParser(AbstractTimeExprParser):
    """Japanese time expression parser inheriting from AbstractTimeExprParser."""

    def primary_prefix(self) -> str:
        return r"(^|(?<=[^\da-zA-Z_０-９]))"

    def following_phase(self) -> str:
        return r"\s*(?:から|\-|–|－|\~|\〜)\s*"

    def primary_suffix(self) -> str:
        return r"(?!/)(?=[^\da-zA-Z_０-９]|$)"

    def following_suffix(self) -> str:
        return r"(?!/)(?=[^\da-zA-Z_０-９]|$)"

    def get_am_pm_pattern(self) -> str:
        return r"(午前|午後|A\.M\.|P\.M\.|AM?|PM?)"

    def get_primary_time_pattern_template(self) -> str:
        return PRIMARY_TIME_PATTERN_TEMPLATE

    def get_following_time_pattern_template(self) -> str:
        return FOLLOWING_TIME_PATTERN_TEMPLATE

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        return self._extract_time_components_from_match(context, match, is_following=False)

    def extract_following_time_components(
        self, context: chrono.ParsingContext, match: Match, result: chrono.ParsedResult
    ) -> ParsingCivilTimeMoment | None:
        return self._extract_time_components_from_match(context, match, is_following=True, result=result)

    def _extract_time_components_from_match(
        self,
        context: chrono.ParsingContext,
        match: Match,
        is_following: bool = False,
        result: chrono.ParsedResult | None = None,
    ) -> ParsingCivilTimeMoment | None:
        components = ParsingCivilTimeMoment.of(context.reference)

        hour_str = match.group(HOUR_GROUP)
        if hour_str is None:
            return None

        hour = parse_ja_number(hour_str)
        if hour is None or hour > 24:
            return None

        minute_str = match.group(MINUTE_GROUP)
        minute_certain = True
        if minute_str is not None:
            if minute_str == "半":
                minute = 30
            else:
                minute = parse_ja_number(minute_str)
            if minute is None or minute >= 60:
                return None
        else:
            if hour > 100:
                minute = hour % 100
                hour = hour // 100
                if minute >= 60 or hour > 24:
                    return None
            else:
                minute = 0
                minute_certain = False

        second_str = match.group(SECOND_GROUP)
        if second_str is not None:
            second = parse_ja_number(second_str)
            if second is None or second >= 60:
                return None
            components.assign(CivilTimeComponent.SECOND, second)
        else:
            components.imply(CivilTimeComponent.SECOND, 0)

        milli_str = match.group(MILLI_SECOND_GROUP)
        if milli_str is not None:
            milli = int(milli_str[:3])
            if milli >= 1000:
                return None
            components.assign(CivilTimeComponent.MILLI_SECOND, milli)

        am_pm_str = match.group(AM_PM_HOUR_GROUP)
        if am_pm_str is None:
            matched_text = match.group(0)
            prefix_match = re.search(r'(午前|午後|A\.M\.|P\.M\.|AM|PM)', matched_text, re.IGNORECASE)
            if prefix_match:
                am_pm_str = prefix_match.group(1)
            elif not is_following and match.start() > 0:
                text_before = context.text[:match.start()]
                before_match = re.search(r'(午前|午後|A\.M\.|P\.M\.|AM|PM)[\s,，、]*$', text_before, re.IGNORECASE)
                if before_match:
                    am_pm_str = before_match.group(1)

        def imply_next_day(moment_to_imply):
            ref_dt = context.reference.datetime()
            y = moment_to_imply.get(CivilTimeComponent.YEAR) or ref_dt.year
            m = moment_to_imply.get(CivilTimeComponent.MONTH) or ref_dt.month
            d_val = moment_to_imply.get(CivilTimeComponent.DAY) or ref_dt.day
            try:
                next_date = date(y, m, d_val) + timedelta(days=1)
                moment_to_imply.imply(CivilTimeComponent.DAY, next_date.day)
                moment_to_imply.imply(CivilTimeComponent.MONTH, next_date.month)
                moment_to_imply.imply(CivilTimeComponent.YEAR, next_date.year)
            except ValueError:
                pass

        meridiem = None
        if am_pm_str is not None:
            if hour > 12:
                return None
            ampm_lower = am_pm_str.lower()
            if am_pm_str == "午前" or ampm_lower.startswith("a"):
                meridiem = Meridiem.AM
                if hour == 12:
                    hour = 0
                    if is_following and not components.is_certain(CivilTimeComponent.DAY):
                        imply_next_day(components)
            elif am_pm_str == "午後" or ampm_lower.startswith("p"):
                meridiem = Meridiem.PM
                if hour != 12:
                    hour += 12

            if is_following and result and not result.moment.is_certain(CivilTimeComponent.MERIDIEM):
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

        if minute_certain:
            components.assign(CivilTimeComponent.MINUTE, minute)
        else:
            components.imply(CivilTimeComponent.MINUTE, minute)

        if meridiem is not None:
            components.assign(CivilTimeComponent.MERIDIEM, meridiem)
        elif is_following and result:
            start_at_pm = (
                result.moment.is_certain(CivilTimeComponent.MERIDIEM) and
                result.moment.get(CivilTimeComponent.HOUR) > 12
            )
            if start_at_pm:
                if result.moment.get(CivilTimeComponent.HOUR) - 12 > hour:
                    components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                elif hour <= 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            elif hour > 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            elif hour <= 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            if hour < 12:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            else:
                components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

        ref_dt = context.reference.datetime()
        components.imply(CivilTimeComponent.YEAR, ref_dt.year)
        components.imply(CivilTimeComponent.MONTH, ref_dt.month)
        components.imply(CivilTimeComponent.DAY, ref_dt.day)

        if is_following and result and components.datetime() < result.moment.datetime():
            imply_next_day(components)

        return components
