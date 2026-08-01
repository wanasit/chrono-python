import re
from chrono_python import chrono
from chrono_python.common.parsers.time_expr_parser import TimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class ITTimeExprParser(TimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:alle?|dalle?)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|a|fino\s*a|alle?|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:di\s*(?:sera|notte|mattina|pomeriggio)))?(?!/)(?=\W|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            match_str = match.group(0)
            hour_str = match.group(2)
            if hour_str is not None and match.group(3) is None:  # minute_str is None
                hour_idx = match_str.find(hour_str)
                if hour_idx != -1 and re.search(r"\b(?:alle?|dalle?|a|da)\b", match_str[:hour_idx].lower()):
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

        if components is None:
            return None

        match_str_lower = match.group(0).lower()
        if "di sera" in match_str_lower or "di notte" in match_str_lower:
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None:
                if 6 <= hour < 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                elif hour < 6:
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif "di pomeriggio" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None and 0 <= hour <= 6:
                components.assign(CivilTimeComponent.HOUR, hour + 12)
        elif "di mattina" in match_str_lower:
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return components
