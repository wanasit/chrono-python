import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.es import constants
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:(este|esta|pasado|pasada|pr[oó]ximo|pr[oó]xima)\s*)?"
    f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(este|esta|pasado|pasada|pr[oó]ximo|pr[oó]xima)\s*semana)?"
    r"(?=\W|\d|$)",
    re.IGNORECASE,
)


class ESWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_of_week = match.group(2).lower()
        weekday = constants.WEEKDAY_DICTIONARY.get(day_of_week)
        if weekday is None:
            return None

        prefix = match.group(1)
        postfix = match.group(3)
        norm = (prefix or postfix or "").lower()

        modifier = None
        if norm in ("pasado", "pasada", "este", "esta"):
            modifier = "this"
        elif norm in ("próximo", "proximo", "próxima", "proxima"):
            modifier = "next"

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
