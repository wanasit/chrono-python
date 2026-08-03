import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"((?:в)\s*)?"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"\s*"
    r"(?:[,-]?\s*"
    f"({constants.YEAR_PATTERN}))?"
    r"(?=[^\s\w]|\s+[^0-9]|\s+$|$)",
    re.IGNORECASE,
)


class RUMonthNameParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month_name = match.group(2).lower()

        # Skip unlikely words like "янв", "фев" if not full month name and too short
        if len(match.group(0)) <= 3 and month_name not in constants.FULL_MONTH_NAME_DICTIONARY:
            return None

        month = constants.MONTH_DICTIONARY[month_name]
        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.imply(CivilTimeComponent.DAY, 1)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(3):
            year = constants.parse_year(match.group(3))
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, 1)
            moment.imply(CivilTimeComponent.YEAR, year)

        return moment
