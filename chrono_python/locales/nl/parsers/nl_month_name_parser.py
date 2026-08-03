import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.nl import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"\s*"
    r"(?:"
    f"[,-]?\\s*({constants.YEAR_PATTERN})?"
    r")?"
    r"(?=[^\s\w]|\s+[^0-9]|\s+$|$)",
    re.IGNORECASE,
)


class NLMonthNameParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        components = ParsingCivilTimeMoment.of(context.reference)
        components.imply(CivilTimeComponent.DAY, 1)

        month_name = match.group(1)
        month = constants.MONTH_DICTIONARY[month_name.lower()]
        components.assign(CivilTimeComponent.MONTH, month)

        if match.group(2):
            year = constants.parse_year(match.group(2))
            components.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, 1)
            components.imply(CivilTimeComponent.YEAR, year)

        return components
