import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.utils import patterns

_YEAR_PATTERN = r'(?:[1-9][0-9]{0,3}\s{0,2}(?:BE|AD|BC|BCE|CE)|[1-9][0-9]{3})'

PATTERN = re.compile(
    f'({_YEAR_PATTERN})' +  # Group 1: Year
    r'(?:\s*[-.\/,]?\s*|\s+of\s+)' +
    f'({patterns.match_any(constants.MONTH_NAME_DICTIONARY)})' +  # Group 2: Month
    r'(?:' +
        r'(?:[\s\/\.\,-]+)' +
        f'({constants.PATTERN_ORDINAL_NUMBER})' +  # Group 3: Day
        r'(?:' +
            r'\s{0,3}(?:to|-|–|until|through|till)\s{0,3}' +
            f'({constants.PATTERN_ORDINAL_NUMBER})' +  # Group 4: End Day
        r')?' +
    r')?' +
    r'(?=\W|$)',
    re.IGNORECASE
)

_YEAR_GROUP = 1
_MONTH_NAME_GROUP = 2
_DAY_GROUP = 3
_END_DAY_GROUP = 4


class ENMonthNameAfterYear(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        year = constants.parse_year(match[_YEAR_GROUP])
        month_name = match[_MONTH_NAME_GROUP].lower()
        month = constants.MONTH_NAME_DICTIONARY[month_name]

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.YEAR, year)

        day_str = match[_DAY_GROUP]
        if day_str:
            day = constants.parse_ordinal_number(day_str)
            if day > 31:
                return None
            moment.assign(CivilTimeComponent.DAY, day)
        else:
            moment.imply(CivilTimeComponent.DAY, 1)

        end_day_str = match[_END_DAY_GROUP]
        if end_day_str:
            end_day = constants.parse_ordinal_number(end_day_str)
            if end_day > 31:
                return None
            end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
            return context.create_parsed_result(match.start(), match.end(), start=moment, end=end_moment)

        return context.create_parsed_result(match.start(), match.end(), moment)
