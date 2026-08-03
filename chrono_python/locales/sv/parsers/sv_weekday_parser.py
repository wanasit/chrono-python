import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.sv import constants
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:på\s*)?"
    r"(?:(förra|senaste|nästa|kommande)\s*)?"
    f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(förra|senaste|nästa|kommande)\s*vecka)?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class SVWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_of_week = match.group(2).lower()
        offset = constants.WEEKDAY_DICTIONARY[day_of_week]

        prefix = match.group(1)
        postfix = match.group(3)

        modifier_word = (prefix or postfix or "").lower()

        modifier = None
        if re.search(r"förra|senaste", modifier_word):
            modifier = "last"
        elif re.search(r"nästa|kommande", modifier_word):
            modifier = "next"

        return create_parsing_components_at_weekday(context.reference, offset, modifier)
