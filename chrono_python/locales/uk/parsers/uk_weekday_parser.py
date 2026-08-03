import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.uk import constants
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:в\s*)?"
    r"(?:у\s*)?"
    r"(?:(цей|минулого|минулий|попередній|попереднього|наступного|наступний|наступному)\s*)?"
    f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(?:на|у|в)\s*(цьому|минулому|наступному)\s*тижні)?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class UKWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        weekday_word = match.group(2).lower()
        if weekday_word not in constants.WEEKDAY_DICTIONARY:
            return None

        weekday = constants.WEEKDAY_DICTIONARY[weekday_word]
        modifier_word = (match.group(1) or match.group(3) or "").lower()

        modifier = None
        if modifier_word in ("минулого", "минулий", "попередній", "попереднього", "минулому"):
            modifier = "last"
        elif modifier_word in ("наступного", "наступний", "наступному"):
            modifier = "next"
        elif modifier_word in ("цей", "цього", "цьому"):
            modifier = "this"

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
