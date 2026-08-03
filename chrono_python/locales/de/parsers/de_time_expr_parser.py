import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class DETimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:um|von|ab)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|bis\s*zu|bis\s*zum|bis|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:uhr|am\s*(?:morgen|nachmittag|abend)|in\s*der\s*nacht|abends|morgens|nachts))?(?!/)(?=\W|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            return None

        match_str_lower = match.group(0).lower()
        if "abend" in match_str_lower or "nacht" in match_str_lower:
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None:
                if 6 <= hour < 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                elif hour < 6:
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif "nachmittag" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None and 0 <= hour <= 6:
                components.assign(CivilTimeComponent.HOUR, hour + 12)
        elif "morgen" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return components
