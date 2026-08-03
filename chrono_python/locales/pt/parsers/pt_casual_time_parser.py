import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:esta\s*)?(manha|manhã|tarde|meia-noite|meio-dia|noite)(?=\W|$)",
    re.IGNORECASE,
)


class PTCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        target_word = match.group(1).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if target_word == "tarde":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 15)
        elif target_word == "noite":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 22)
        elif target_word in ("manha", "manhã"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 6)
        elif target_word == "meia-noite":
            next_day = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(next_day)
            component.imply_similar_time(next_day)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
        elif target_word == "meio-dia":
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 12)
        else:
            return None

        return component
