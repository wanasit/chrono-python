import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.utils import patterns

_YEAR_PATTERN = r'(?:[1-9][0-9]{0,3}\s{0,2}(?:BE|AD|BC|BCE|CE)|[1-9][0-9]{3})'

PATTERN = re.compile(
    f'({_YEAR_PATTERN})' +
    r'(?:\s*[-.\/,]?\s*|\s+of\s+)' +
    f'({patterns.match_any(constants.MONTH_NAME_DICTIONARY)})' +
    r'(?=[^\s\w]|\s+[^0-9]|\s+$|$)',
    re.IGNORECASE
)

_YEAR_GROUP = 1
_MONTH_NAME_GROUP = 2


class ENMonthNameAfterYear(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        year = constants.parse_year(match[_YEAR_GROUP])
        month_name = match[_MONTH_NAME_GROUP].lower()
        month = constants.MONTH_NAME_DICTIONARY[month_name]

        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.imply(CivilTimeComponent.DAY, 1)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.YEAR, year)

        return context.create_parsed_result(match.start(), match.end(), moment)
