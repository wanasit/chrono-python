import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class SVTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:kl(?:ockan|\.)?|från)\s*)?"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|till|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:klockan|på\s*(?:morgonen?|förmiddagen?|middagen?|eftermiddagen?|kvällen?|natten?)|om\s*(?:morgonen?|förmiddagen?|middagen?|eftermiddagen?|kvällen?|natten?)))?(?!/)(?=\W|$)"

    def following_suffix(self) -> str:
        return r"(?:\s*(?:klockan|på\s*(?:morgonen?|förmiddagen?|middagen?|eftermiddagen?|kvällen?|natten?)|om\s*(?:morgonen?|förmiddagen?|middagen?|eftermiddagen?|kvällen?|natten?)))?(?!/)(?=\W|$)"

    def get_am_pm_pattern(self) -> str:
        return r"(a\.m\.|p\.m\.|am?|pm?)"

    def check_and_return_without_following_pattern(
        self, result: chrono.ParsedResult
    ) -> chrono.ParsedResult | None:
        if re.search(r"klockan|kl", result.text, re.IGNORECASE):
            return result
        return super().check_and_return_without_following_pattern(result)

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            match_str_lower = match.group(0).lower()
            hour_str = match.group(2)
            minute_str = match.group(3)
            if hour_str is not None and minute_str is not None:
                if any(kw in match_str_lower for kw in ["klockan", "kl", "kl."]):
                    hour = int(hour_str)
                    minute = int(minute_str)
                    if 0 <= hour <= 24 and 0 <= minute < 60:
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

        return components
