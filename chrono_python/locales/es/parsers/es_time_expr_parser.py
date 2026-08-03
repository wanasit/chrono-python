import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class ESTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T)(?:(?:a\s*las|de\s*las|las?|al?|de|del)\s*)?"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|a(?:l)?|\?)\s*"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            hour_str = match.group(2)
            minute_str = match.group(3)
            ampm_str = match.group(6)
            if hour_str is not None and minute_str is None:
                hour_val = int(hour_str)
                if hour_val > 100:
                    if len(hour_str) == 4 and ampm_str is None:
                        return None
                    minute = hour_val % 100
                    hour = hour_val // 100
                    if hour <= 24 and minute < 60:
                        comp = ParsingCivilTimeMoment.of(context.reference)
                        comp.assign(CivilTimeComponent.HOUR, hour)
                        comp.assign(CivilTimeComponent.MINUTE, minute)
                        comp.imply(CivilTimeComponent.SECOND, 0)
                        comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                        if ampm_str is not None:
                            if ampm_str[0].lower() == 'a':
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                                if hour == 12:
                                    comp.assign(CivilTimeComponent.HOUR, 0)
                            else:
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                                if hour < 12:
                                    comp.assign(CivilTimeComponent.HOUR, hour + 12)
                        else:
                            if hour < 12:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                            else:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

                        ref_dt = context.reference.datetime()
                        comp.imply(CivilTimeComponent.YEAR, ref_dt.year)
                        comp.imply(CivilTimeComponent.MONTH, ref_dt.month)
                        comp.imply(CivilTimeComponent.DAY, ref_dt.day)
                        components = comp
                elif hour_val <= 24:
                    comp = ParsingCivilTimeMoment.of(context.reference)
                    comp.assign(CivilTimeComponent.HOUR, hour_val)
                    comp.assign(CivilTimeComponent.MINUTE, 0)
                    comp.imply(CivilTimeComponent.SECOND, 0)
                    comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                    if ampm_str is not None:
                        if ampm_str[0].lower() == 'a':
                            comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                            if hour_val == 12:
                                comp.assign(CivilTimeComponent.HOUR, 0)
                        else:
                            comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                            if hour_val < 12:
                                comp.assign(CivilTimeComponent.HOUR, hour_val + 12)
                    else:
                        if hour_val < 12:
                            comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                        else:
                            comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

                    ref_dt = context.reference.datetime()
                    comp.imply(CivilTimeComponent.YEAR, ref_dt.year)
                    comp.imply(CivilTimeComponent.MONTH, ref_dt.month)
                    comp.imply(CivilTimeComponent.DAY, ref_dt.day)
                    components = comp

        return components
