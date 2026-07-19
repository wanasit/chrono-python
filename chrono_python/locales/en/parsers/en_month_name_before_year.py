import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r'((?:in)\s*)?' +
    f'({patterns.match_any(constants.MONTH_NAME_DICTIONARY)})' +
    r'\s*' +
    r'(?:' +
    rf'(?:,|-|of)?\s*({constants.PATTERN_YEAR})' +
    r')?' +
    r'(?=[^\s\w]|\s+[^0-9]|\s+$|$)',
    re.IGNORECASE
)

_PREFIX_GROUP = 1
_MONTH_NAME_GROUP = 2
_YEAR_GROUP = 3


class ENMonthNameBeforeYear(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        month_name = match[_MONTH_NAME_GROUP].lower()

        # skip some unlikely words "jan", "mar", ..
        if len(match[0]) <= 3 and month_name not in constants.FULL_MONTH_NAME_DICTIONARY:
            return None

        # Calculate custom start and end index
        prefix_len = len(match[_PREFIX_GROUP]) if match[_PREFIX_GROUP] else 0
        start_index = match.start() + prefix_len
        end_index = match.end()

        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.imply(CivilTimeComponent.DAY, 1)

        month = constants.MONTH_NAME_DICTIONARY[month_name]
        moment.assign(CivilTimeComponent.MONTH, month)

        if match[_YEAR_GROUP]:
            year = constants.parse_year(match[_YEAR_GROUP])
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, 1)
            moment.imply(CivilTimeComponent.YEAR, year)

        return context.create_parsed_result(start_index, end_index, moment)
