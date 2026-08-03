import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class UKTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:в|у|о|об|з|із|від)\s*)?"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|до|і|по|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:ранку|вечора|по обіді|після обіду))?(?!/)(?=\W|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)

        if components is None:
            match_str = match.group(0)
            hour_str = match.group(2)
            minute_str = match.group(3)
            if hour_str is not None:
                match_str_lower = match_str.lower()
                hour_idx = match_str.find(hour_str)
                prefix_part = match_str_lower[:hour_idx]
                suffix_part = match_str_lower[hour_idx + len(hour_str):]
                has_prefix = bool(re.search(r"(?:^|\s)(?:в|у|о|об|з|із|від)\s*$", prefix_part))
                has_suffix = bool(re.search(r"(?:ранку|вечора|по обіді|після обіду)", suffix_part))
                if has_prefix or has_suffix:
                    hour = int(hour_str)
                    minute = int(minute_str) if minute_str is not None else 0
                    if hour <= 24 and minute < 60:
                        comp = ParsingCivilTimeMoment.of(context.reference)
                        comp.assign(CivilTimeComponent.HOUR, hour)
                        comp.assign(CivilTimeComponent.MINUTE, minute)
                        comp.imply(CivilTimeComponent.SECOND, 0)
                        comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                        if hour < 12:
                            comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                        else:
                            comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                        ref_dt = context.reference.datetime()
                        comp.imply(CivilTimeComponent.YEAR, ref_dt.year)
                        comp.imply(CivilTimeComponent.MONTH, ref_dt.month)
                        comp.imply(CivilTimeComponent.DAY, ref_dt.day)
                        components = comp

        if components is None:
            return None

        match_str_lower = match.group(0).lower()
        if match_str_lower.endswith("вечора"):
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None:
                if 6 <= hour < 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                elif hour < 6:
                    components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif match_str_lower.endswith("по обіді") or match_str_lower.endswith("після обіду"):
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None and 0 <= hour <= 6:
                components.assign(CivilTimeComponent.HOUR, hour + 12)
        elif match_str_lower.endswith("ранку"):
            components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            hour = components.get(CivilTimeComponent.HOUR)
            if hour is not None and hour < 12:
                components.assign(CivilTimeComponent.HOUR, hour)

        return components
