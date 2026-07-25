import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r'(?:this)?\s{0,3}(morning|afternoon|evening|night|midnight|midday|noon)(?=\W|$)',
    re.IGNORECASE
)


class ENCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        target_word = match.group(1).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if target_word == "afternoon":
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif target_word in ("evening", "night"):
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 20)
        elif target_word == "midnight":
            target_date = context.reference.datetime()
            if target_date.hour > 2:
                target_date = target_date + datetime.timedelta(days=1)
            component.imply_similar_date(target_date)
            component.assign(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif target_word == "morning":
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif target_word in ("noon", "midday"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.assign(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        else:
            return None

        return component
