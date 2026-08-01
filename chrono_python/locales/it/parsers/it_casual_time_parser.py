import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(stamattina|stasera|stanotte|stamani)|(?:questa\s*)?(mattina|pomeriggio|sera|notte|mezzanotte|mezzogiorno))(?=\W|$)",
    re.IGNORECASE,
)


class ITCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_word = (match.group(1) or match.group(2)).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if target_word in ("stamattina", "stamani", "mattina"):
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "pomeriggio":
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word in ("stasera", "sera"):
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word in ("stanotte", "notte"):
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "mezzanotte":
            ref_dt = context.reference.datetime()
            if ref_dt.hour > 2:
                ref_dt = ref_dt + datetime.timedelta(days=1)
            component = ParsingCivilTimeMoment.of(ref_dt)
            component.assign(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "mezzogiorno":
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        return component
