import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru.constants import WEEKDAY_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:в\s*?)?"
    r"(?:(эту|этот|прошлый|прошлую|следующий|следующую|следующего)\s*)?"
    f"({patterns.match_any(WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*на\s*(этой|прошлой|следующей)\s*неделе)?"
    r"(?=[^\w]|$)",
    re.IGNORECASE,
)


class RUWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_of_week = match.group(2).lower()
        weekday = WEEKDAY_DICTIONARY[day_of_week]

        prefix = match.group(1) or ""
        postfix = match.group(3) or ""
        modifier_word = (prefix or postfix).lower()

        modifier = None
        if modifier_word in ("прошлый", "прошлую", "прошлой"):
            modifier = "last"
        elif modifier_word in ("следующий", "следующую", "следующей", "следующего"):
            modifier = "next"
        elif modifier_word in ("этот", "эту", "этой"):
            modifier = "this"

        return create_parsing_components_at_weekday(
            context.reference,
            weekday,
            modifier,
        )
