import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.it import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment, ReferenceMoment
from chrono_python.utils import patterns

PATTERN = re.compile(
    r"(?:"
    r"(?:il\s*|la\s*|l'\s*)?(questo|questa|quest'|scorso|scorsa|prossimo|prossima|dopo\s*questo|dopo\s*questa)\s*"
    f"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})"
    r"|"
    r"(?:il\s*|la\s*|l'\s*)"
    rf"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})\s*"
    r"(scorso|scorsa|prossimo|prossima)"
    r")(?=\W|$)",
    re.IGNORECASE,
)


class ITRelativeDateFormatParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        if match.group(1):
            modifier = match.group(1).lower()
            unit_word = match.group(2).lower()
        else:
            modifier = match.group(4).lower()
            unit_word = match.group(3).lower()

        if unit_word not in constants.TIME_UNIT_DICTIONARY:
            return None

        timeunit = constants.TIME_UNIT_DICTIONARY[unit_word]

        if modifier in ("prossimo", "prossima") or modifier.startswith("dopo"):
            return ReferenceMoment.of(context.reference, {timeunit: 1})

        if modifier in ("scorso", "scorsa"):
            return ReferenceMoment.of(context.reference, {timeunit: -1})

        components = ParsingCivilTimeMoment.of(context.reference)
        ref_date = context.reference.datetime()

        if "settimana" in unit_word:
            day_of_week_sun0 = (ref_date.weekday() + 1) % 7
            sun_date = ref_date - datetime.timedelta(days=day_of_week_sun0)
            components.imply(CivilTimeComponent.DAY, sun_date.day)
            components.imply(CivilTimeComponent.MONTH, sun_date.month)
            components.imply(CivilTimeComponent.YEAR, sun_date.year)
        elif "mese" in unit_word:
            components.imply(CivilTimeComponent.DAY, 1)
            components.assign(CivilTimeComponent.MONTH, ref_date.month)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)
        elif "anno" in unit_word:
            components.imply(CivilTimeComponent.DAY, 1)
            components.imply(CivilTimeComponent.MONTH, 1)
            components.assign(CivilTimeComponent.YEAR, ref_date.year)

        return components
