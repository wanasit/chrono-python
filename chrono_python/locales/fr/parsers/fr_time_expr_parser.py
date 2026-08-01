import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match

# Primary time pattern template for French.
# Note: Capturing group indices must strictly follow AbstractTimeExprParser base class:
#   Group 1: Prefix (<primary_prefix>)
#   Group 2: Hour (\d{1,4})
#   Group 3: Minute (\d{1,2})
#   Group 4: Second (\d{1,2})
#   Group 5: Millisecond (\d{1,6})
#   Group 6: AM/PM (<am_pm_pattern>)
PRIMARY_TIME_PATTERN_TEMPLATE = (
    r"<primary_prefix>"
    r"(\d{1,4})"                              # Hour (1-4 digits)
    r"(?:h|:|min|m|\.)?"
    r"(?:"
        r"\s*(\d{1,2})"                       # Minute
        r"(?:m|min|:|s|\.)?"
    r")?"
    r"(?:\s*(\d{1,2})s?)?"                    # Second
    r"(?:\.(\d{1,6}))?"                       # Millisecond
    r"(?:\s*<am_pm_pattern>)?"                # AM/PM
    r"<primary_suffix>"
)

# Following time pattern template for French range expressions.
# Note: Capturing group indices must strictly follow AbstractTimeExprParser base class:
#   Group 1: Following phase connector (<following_phase>)
#   Group 2: Hour (\d{1,4})
#   Group 3: Minute (\d{1,2})
#   Group 4: Second (\d{1,2})
#   Group 5: Millisecond (\d{1,6})
#   Group 6: AM/PM (<am_pm_pattern>)
FOLLOWING_TIME_PATTERN_TEMPLATE = (
    r"^"
    r"(<following_phase>)"                    # Phase connector matching group
    r"(\d{1,4})"                              # Hour
    r"(?:h|:|min|m|\.)?"
    r"(?:"
        r"\s*(\d{1,2})"                       # Minute
        r"(?:m|min|:|s|\.)?"
    r")?"
    r"(?:\s*(\d{1,2})s?)?"                    # Second
    r"(?:\.(\d{1,6}))?"                       # Millisecond
    r"(?:\s*<am_pm_pattern>)?"                # AM/PM
    r"<following_suffix>"
)


class FRTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T)(?:(?:[àa]|de)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|[àa]|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:h(?:eures)?|heures?))?(?!/)(?=\W|$)"

    def following_suffix(self) -> str:
        return r"(?:\s*(?:h(?:eures)?|heures?))?(?!/)(?=\W|$)"

    def get_am_pm_pattern(self) -> str:
        return r"(a\.m\.|p\.m\.|am?|pm?|mp)"

    def get_primary_time_pattern_template(self) -> str:
        return PRIMARY_TIME_PATTERN_TEMPLATE

    def get_following_time_pattern_template(self) -> str:
        return FOLLOWING_TIME_PATTERN_TEMPLATE

    def check_and_return_without_following_pattern(
        self, result: chrono.ParsedResult
    ) -> chrono.ParsedResult | None:
        # Ignore 4-digit numbers like "2020" without time indicators
        if re.match(r"^\s*\d{4}\s*$", result.text) and not re.search(r"[hH]", result.text):
            return None
        return result

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            # Fallback for range start hours without explicit minute, suffix, or "h" indicator (e.g. "13-15h").
            # "13" alone in "13-15h" lacks minute digits and suffix, so super() returns None;
            # this fallback allows bare numbers <= 24 to be parsed as hours when followed by a range.
            match_str = match.group(0)
            hour_str = match.group(2)
            minute_str = match.group(3)
            ampm_str = match.group(6)
            if hour_str is not None and minute_str is None and ampm_str is None:
                hour = int(hour_str)
                if hour <= 24:
                    comp = ParsingCivilTimeMoment.of(context.reference)
                    comp.assign(CivilTimeComponent.HOUR, hour)
                    comp.assign(CivilTimeComponent.MINUTE, 0)
                    comp.imply(CivilTimeComponent.SECOND, 0)
                    comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                    if hour < 12:
                        comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                    else:
                        comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                    components = comp

        return components
