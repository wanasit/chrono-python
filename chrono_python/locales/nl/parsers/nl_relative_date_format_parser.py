import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.nl import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment, ReferenceMoment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    return re.compile(
        rf"(dit|deze|(?:aan)?komend|volgend|afgelopen|vorig)e?\s*({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})(?=\W|$)",
        re.IGNORECASE,
    )


MODIFIER_WORD_GROUP = 1
RELATIVE_WORD_GROUP = 2


class NLRelativeDateFormatParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier = match.group(MODIFIER_WORD_GROUP).lower()
        unit_word = match.group(RELATIVE_WORD_GROUP).lower()

        if unit_word not in constants.TIME_UNIT_DICTIONARY:
            return None

        timeunit = constants.TIME_UNIT_DICTIONARY[unit_word]

        if modifier in ("volgend", "komend", "aankomend"):
            return ReferenceMoment.of(context.reference, {timeunit: 1})

        if modifier in ("afgelopen", "vorig"):
            return ReferenceMoment.of(context.reference, {timeunit: -1})

        components = ParsingCivilTimeMoment.of(context.reference)
        ref_date = context.reference.datetime()

        if "week" in unit_word:
            day_of_week_sun0 = (ref_date.weekday() + 1) % 7
            sun_date = ref_date - datetime.timedelta(days=day_of_week_sun0)
            components.imply(CivilTimeComponent.DAY, sun_date.day)
            components.imply(CivilTimeComponent.MONTH, sun_date.month)
            components.imply(CivilTimeComponent.YEAR, sun_date.year)
        elif "maand" in unit_word:
            components.imply(CivilTimeComponent.DAY, 1)
            components.assign(CivilTimeComponent.MONTH, ref_date.month)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)
        elif "jaar" in unit_word:
            components.imply(CivilTimeComponent.DAY, 1)
            components.imply(CivilTimeComponent.MONTH, 1)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)

        return components
