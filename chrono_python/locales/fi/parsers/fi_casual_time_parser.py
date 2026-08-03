import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(tänä\s*)?(aamulla|aamuna|aamupäivällä|päivällä|iltapäivällä|illalla|yöllä|keskiyöllä)(?=\W|$)",
    re.IGNORECASE,
)


class FICasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        time_keyword = match.group(2).lower()
        component = ParsingCivilTimeMoment.of(context.reference)
        component.imply_similar_time(target_date)
        return FICasualTimeParser.extract_time_components(component, time_keyword)

    @staticmethod
    def extract_time_components(
        component: ParsingCivilTimeMoment, time_keyword: str
    ) -> ParsingCivilTimeMoment:
        if time_keyword in ("aamulla", "aamuna"):
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif time_keyword == "aamupäivällä":
            component.imply(CivilTimeComponent.HOUR, 9)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif time_keyword == "päivällä":
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif time_keyword == "iltapäivällä":
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif time_keyword == "illalla":
            component.imply(CivilTimeComponent.HOUR, 18)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif time_keyword == "yöllä":
            component.imply(CivilTimeComponent.HOUR, 22)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif time_keyword == "keskiyöllä":
            curr_hour = component.get(CivilTimeComponent.HOUR)
            if curr_hour is not None and curr_hour > 1:
                dt = component.datetime() + datetime.timedelta(days=1)
                component.imply_similar_date(dt)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)

        return component
