import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(cet?)?\s*(matin|soir|après-midi|aprem|a midi|à minuit)(?=\W|$)",
    re.IGNORECASE,
)


class FRCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_word = match.group(2).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if target_word in ("après-midi", "aprem"):
            component.imply(CivilTimeComponent.HOUR, 14)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word == "soir":
            component.imply(CivilTimeComponent.HOUR, 18)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word == "matin":
            component.imply(CivilTimeComponent.HOUR, 8)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "a midi":
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "à minuit":
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        return component
