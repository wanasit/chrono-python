import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:^|\s|T|\b)"
    r"(?:um\s*)?"
    r"(\d{1,2})"
    r"(?:"
        r"(?::|\.)(\d{1,2})"
        r"(?::(\d{1,2}))?"
        r"(?:\s*uhr)?"
    r"|"
        r"\s*uhr(?:\s*(\d{1,2})(?:\s*min(?:uten)?)?)?"
    r")"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class DESpecificTimeExpressionParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        hour = int(match.group(1))
        if hour > 24:
            return None

        minute = 0
        second = 0

        if match.group(2) is not None:
            minute = int(match.group(2))
        elif match.group(4) is not None:
            minute = int(match.group(4))

        if match.group(3) is not None:
            second = int(match.group(3))

        if minute >= 60 or second >= 60:
            return None

        component = ParsingCivilTimeMoment.of(context.reference)
        component.assign(CivilTimeComponent.HOUR, hour)
        component.assign(CivilTimeComponent.MINUTE, minute)
        component.assign(CivilTimeComponent.SECOND, second)

        if hour < 12:
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)

        return component
