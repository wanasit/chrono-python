import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(gisteren|morgen|van)(ochtend|middag|namiddag|avond|nacht)(?=\W|$)",
    re.IGNORECASE,
)


class NLCasualDateTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        date_text = match.group(1).lower()
        time_text = match.group(2).lower()
        component = ParsingCivilTimeMoment.of(context.reference)
        target_date = context.reference.datetime()

        if date_text == "gisteren":
            previous_day = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(previous_day)
        elif date_text == "van":
            component.assign_similar_date(target_date)
        elif date_text == "morgen":
            next_day = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(next_day)
            component.imply_similar_time(next_day)

        if time_text == "ochtend":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 6)
        elif time_text == "middag":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 12)
        elif time_text == "namiddag":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 15)
        elif time_text == "avond":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 20)
        elif time_text == "nacht":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 0)

        return component
