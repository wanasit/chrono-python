import re

from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class ENTimeExprParser(AbstractTimeExprParser):
    """English subclass of AbstractTimeExprParser that overrides English-specific time patterns and logic."""

    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:at|from)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|to|until|through|till|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:o\W*clock|at\s*night|in\s*the\s*(?:morning|afternoon)))?(?!/)(?=\W|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            return None

        # Custom morning/afternoon/night handling if present in the matched segment
        match_str_lower = match.group(0).lower()
        if "night" in match_str_lower:
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None:
                if 6 <= hour < 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                elif hour < 6:
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif "afternoon" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None and 0 <= hour <= 6:
                components.assign(CivilTimeComponent.HOUR, hour + 12)
        elif "morning" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return components
