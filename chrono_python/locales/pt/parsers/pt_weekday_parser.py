import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.utils import patterns
from chrono_python.locales.pt import constants
from chrono_python.types import Moment


def compile_pattern() -> re.Pattern:
    return re.compile(
        r"(?:(?:\,|\(|\（)\s*)?"
        r"(?:(este|esta|passado|passada|pr[oó]ximo|pr[oó]xima)\s*)?"
        f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
        r"(?:\s*(?:\,|\)|\）))?"
        r"(?:\s*(este|esta|passado|passada|pr[oó]ximo|pr[oó]xima)\s*semana)?"
        r"(?=\W|\d|$)",
        re.IGNORECASE,
    )


class PTWeekdayParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

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
        if norm in ("passado", "passada"):
            modifier = "this"
        elif norm in ("próximo", "proximo", "próxima", "proxima"):
            modifier = "next"
        elif norm in ("este", "esta"):
            modifier = "this"

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
