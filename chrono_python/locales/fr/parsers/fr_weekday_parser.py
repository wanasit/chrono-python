import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.fr.constants import WEEKDAY_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:ce\s*)?"
    rf"({patterns.match_any(WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(dernier|prochain)\s*)?"
    r"(?=\W|\d|$)",
    re.IGNORECASE,
)


class FRWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_of_week = match.group(1).lower()
        if day_of_week not in WEEKDAY_DICTIONARY:
            return None
        weekday = WEEKDAY_DICTIONARY[day_of_week]

        suffix = (match.group(2) or "").lower()
        modifier = None
        if suffix == "dernier":
            modifier = "last"
        elif suffix == "prochain":
            modifier = "next"

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
