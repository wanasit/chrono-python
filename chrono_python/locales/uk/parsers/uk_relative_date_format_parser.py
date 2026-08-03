import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.uk import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment, ReferenceMoment, Timeunit
from chrono_python.utils import patterns

PATTERN = re.compile(
    r"(в минулому|у минулому|на минулому|минулого|на наступному|в наступному|у наступному|наступного|на цьому|в цьому|у цьому|цього)\s*"
    f"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})(?=\\s*|\\W|$)",
    re.IGNORECASE,
)


class UKRelativeDateFormatParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier = match.group(1).lower()
        unit_word = match.group(2).lower()
        if unit_word not in constants.TIME_UNIT_DICTIONARY:
            return None

        timeunit = constants.TIME_UNIT_DICTIONARY[unit_word]

        if modifier in ("на наступному", "в наступному", "у наступному", "наступного"):
            return ReferenceMoment.of(context.reference, {timeunit: 1})

        if modifier in ("на минулому", "в минулому", "у минулому", "минулого"):
            return ReferenceMoment.of(context.reference, {timeunit: -1})

        components = ParsingCivilTimeMoment.of(context.reference)
        ref_date = context.reference.datetime()

        if timeunit == Timeunit.WEEK:
            day_of_week_sun0 = (ref_date.weekday() + 1) % 7
            sun_date = ref_date - datetime.timedelta(days=day_of_week_sun0)
            components.imply(CivilTimeComponent.DAY, sun_date.day)
            components.imply(CivilTimeComponent.MONTH, sun_date.month)
            components.imply(CivilTimeComponent.YEAR, sun_date.year)
        elif timeunit == Timeunit.MONTH:
            components.imply(CivilTimeComponent.DAY, 1)
            components.assign(CivilTimeComponent.MONTH, ref_date.month)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)
        elif timeunit == Timeunit.YEAR:
            components.imply(CivilTimeComponent.DAY, 1)
            components.imply(CivilTimeComponent.MONTH, 1)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)

        return components
