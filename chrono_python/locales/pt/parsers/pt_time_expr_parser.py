import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class PTTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:ao?|às?|das|da|de|do)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|a(?:o)?|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:h(?:oras)?|horas?))?(?!/)(?=\W|$)"

    def following_suffix(self) -> str:
        return r"(?:\s*(?:h(?:oras)?|horas?))?(?!/)(?=\W|$)"

    def get_am_pm_pattern(self) -> str:
        return r"(a\.m\.|p\.m\.|am?|pm?)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components is None:
            match_str = match.group(0)
            hour_str = match.group(2)
            minute_str = match.group(3)
            ampm_str = match.group(6)
            if hour_str is not None and minute_str is None:
                hour_num = int(hour_str)
                if len(hour_str) in (3, 4) and hour_num > 100:
                    h = hour_num // 100
                    m = hour_num % 100
                    if 0 <= h <= 24 and 0 <= m < 60:
                        comp = ParsingCivilTimeMoment.of(context.reference)
                        comp.assign(CivilTimeComponent.HOUR, h)
                        comp.assign(CivilTimeComponent.MINUTE, m)
                        comp.imply(CivilTimeComponent.SECOND, 0)
                        comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                        if ampm_str is not None:
                            ampm = ampm_str[0].lower()
                            if ampm == "a":
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                                if h == 12:
                                    comp.assign(CivilTimeComponent.HOUR, 0)
                            elif ampm in ("p", "m"):
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                                if h != 12:
                                    comp.assign(CivilTimeComponent.HOUR, h + 12 if h < 12 else h)
                        else:
                            if h < 12:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                            else:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                        return comp
                elif 0 <= hour_num <= 24:
                    remaining_text = context.text[match.end():]
                    following_match = self.get_following_time_pattern_through_cache().match(remaining_text)
                    hour_idx = match_str.find(hour_str)
                    prefix_part = match_str[:hour_idx].lower() if hour_idx != -1 else ""
                    has_prefix = bool(re.search(r"(?:at|from|à|às|a|ao|de|das|da|do)", prefix_part))
                    if following_match or has_prefix:
                        comp = ParsingCivilTimeMoment.of(context.reference)
                        comp.assign(CivilTimeComponent.HOUR, hour_num)
                        comp.assign(CivilTimeComponent.MINUTE, 0)
                        comp.imply(CivilTimeComponent.SECOND, 0)
                        comp.imply(CivilTimeComponent.MILLI_SECOND, 0)
                        if ampm_str is not None:
                            ampm = ampm_str[0].lower()
                            if ampm == "a":
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                                if hour_num == 12:
                                    comp.assign(CivilTimeComponent.HOUR, 0)
                            elif ampm in ("p", "m"):
                                comp.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                                if hour_num != 12:
                                    comp.assign(CivilTimeComponent.HOUR, hour_num + 12 if hour_num < 12 else hour_num)
                        else:
                            if hour_num < 12:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                            else:
                                comp.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                        return comp
        return components
