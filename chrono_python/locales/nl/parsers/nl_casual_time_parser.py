import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(deze)?\s*(namiddag|avond|middernacht|ochtend|middag|'s middags|'s avonds|'s ochtends)(?=\W|$)",
    re.IGNORECASE,
)


class NLCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        component = ParsingCivilTimeMoment.of(context.reference)

        day_prefix = match.group(1)
        if day_prefix and day_prefix.lower() == "deze":
            component.assign(CivilTimeComponent.DAY, target_date.day)
            component.assign(CivilTimeComponent.MONTH, target_date.month)
            component.assign(CivilTimeComponent.YEAR, target_date.year)

        moment_text = match.group(2).lower()
        if moment_text in ("namiddag", "'s namiddags"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 15)
        elif moment_text in ("avond", "'s avonds"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 20)
        elif moment_text == "middernacht":
            next_day = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(next_day)
            component.imply_similar_time(next_day)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
        elif moment_text in ("ochtend", "'s ochtends"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 6)
        elif moment_text in ("middag", "'s middags"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 12)
        else:
            return None

        return component
