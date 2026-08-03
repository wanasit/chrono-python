import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment, ReferenceMoment, Timeunit
from chrono_python.utils import patterns

PATTERN = re.compile(
    r"(в прошлом|на прошлой|на следующей|в следующем|на этой|в этом)\s*"
    f"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})",
    re.IGNORECASE,
)


class RURelativeDateFormatParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier = match.group(1).lower()
        unit_word = match.group(2).lower()
        timeunit = constants.TIME_UNIT_DICTIONARY[unit_word]

        if modifier in ("на следующей", "в следующем"):
            return ReferenceMoment.of(context.reference, {timeunit: 1})

        if modifier in ("в прошлом", "на прошлой"):
            return ReferenceMoment.of(context.reference, {timeunit: -1})

        # "на этой", "в этом"
        components = ParsingCivilTimeMoment.of(context.reference)
        ref_dt = context.reference.datetime()

        if timeunit == Timeunit.WEEK:
            days_since_sunday = (ref_dt.weekday() + 1) % 7
            start_of_week = ref_dt - datetime.timedelta(days=days_since_sunday)
            components.imply(CivilTimeComponent.DAY, start_of_week.day)
            components.imply(CivilTimeComponent.MONTH, start_of_week.month)
            components.imply(CivilTimeComponent.YEAR, start_of_week.year)
        elif timeunit == Timeunit.MONTH:
            components.imply(CivilTimeComponent.DAY, 1)
            components.assign(CivilTimeComponent.MONTH, ref_dt.month)
            components.assign(CivilTimeComponent.YEAR, ref_dt.year)
        elif timeunit == Timeunit.YEAR:
            components.imply(CivilTimeComponent.DAY, 1)
            components.imply(CivilTimeComponent.MONTH, 1)
            components.assign(CivilTimeComponent.YEAR, ref_dt.year)

        return components
