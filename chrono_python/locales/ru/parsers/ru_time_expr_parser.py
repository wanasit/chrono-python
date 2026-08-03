import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.utils.re import Match


class RUTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:в|с)\s*)?"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|до|и|по|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:утра|вечера|после полудня))?(?!/)(?=[^\w]|$)"

    def following_suffix(self) -> str:
        return r"(?:\s*(?:утра|вечера|после полудня))?(?!/)(?=[^\w]|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_primary_time_components(context, match)
        if components:
            match_str = match.group(0)
            if match_str.endswith("вечера"):
                hour = components.get(CivilTimeComponent.HOUR)
                if hour is not None:
                    if 6 <= hour < 12:
                        components.assign(CivilTimeComponent.HOUR, hour + 12)
                        components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                    elif hour < 6:
                        components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

            elif match_str.endswith("после полудня"):
                components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                hour = components.get(CivilTimeComponent.HOUR)
                if hour is not None and 0 <= hour <= 6:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)

            elif match_str.endswith("утра"):
                components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return components

    def extract_following_time_components(
        self, context: chrono.ParsingContext, match: Match, result: chrono.ParsedResult
    ) -> ParsingCivilTimeMoment | None:
        components = super().extract_following_time_components(context, match, result)
        if components:
            match_str = match.group(0)
            if match_str.endswith("вечера"):
                components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                hour = components.get(CivilTimeComponent.HOUR)
                if hour is not None and hour < 12:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
                if not result.moment.is_certain(CivilTimeComponent.MERIDIEM):
                    start_hour = result.moment.get(CivilTimeComponent.HOUR)
                    if start_hour is not None and start_hour < 12:
                        result.moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                        result.moment.assign(CivilTimeComponent.HOUR, start_hour + 12)
            elif match_str.endswith("после полудня"):
                components.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                hour = components.get(CivilTimeComponent.HOUR)
                if hour is not None and 0 <= hour <= 6:
                    components.assign(CivilTimeComponent.HOUR, hour + 12)
            elif match_str.endswith("утра"):
                components.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return components
