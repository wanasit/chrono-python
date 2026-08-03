import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(morgens|vormittags|mittags|nachmittags|abends|nachts)|(?:am\s*)?(morgen|vormittag|mittag|nachmittag|abend|nacht)|(mitternacht))(?=\W|$)",
    re.IGNORECASE,
)


class DECasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_word = (match.group(1) or match.group(2) or match.group(3)).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if target_word in ("morgens", "morgen"):
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word in ("vormittags", "vormittag"):
            component.imply(CivilTimeComponent.HOUR, 10)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word in ("mittags", "mittag"):
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word in ("nachmittags", "nachmittag"):
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word in ("abends", "abend"):
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif target_word in ("nachts", "nacht"):
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif target_word == "mitternacht":
            ref_dt = context.reference.datetime()
            if ref_dt.hour > 2:
                ref_dt = ref_dt + datetime.timedelta(days=1)
            component = ParsingCivilTimeMoment.of(ref_dt)
            component.assign(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        return component
