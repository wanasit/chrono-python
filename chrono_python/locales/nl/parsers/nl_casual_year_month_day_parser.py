import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.nl.constants import MONTH_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.types import Moment

PATTERN = re.compile(
    rf"([0-9]{{4}})[\.\/\s]"
    rf"(?:({patterns.match_any(MONTH_DICTIONARY)})|([0-9]{{1,2}}))[\.\/\s]"
    rf"([0-9]{{1,2}})"
    rf"(?=\W|$)",
    re.IGNORECASE,
)


class NLCasualYearMonthDayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month_num_str = match.group(3)
        month_name_str = match.group(2)
        if month_num_str:
            month = int(month_num_str)
        elif month_name_str:
            month = MONTH_DICTIONARY[month_name_str.lower()]
        else:
            return None

        if month < 1 or month > 12:
            return None

        year = int(match.group(1))
        day = int(match.group(4))

        component = ParsingCivilTimeMoment.of(context.reference)
        component.assign(CivilTimeComponent.DAY, day)
        component.assign(CivilTimeComponent.MONTH, month)
        component.assign(CivilTimeComponent.YEAR, year)
        return component
