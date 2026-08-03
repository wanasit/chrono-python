import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.nl.constants import WEEKDAY_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:op\s*)?"
    r"(?:(deze|vorige|afgelopen|volgende|komende|aankomende)\s*(?:week\s*)?)?"
    rf"({patterns.match_any(WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(deze|vorige|afgelopen|volgende|komende|aankomende))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)

PREFIX_GROUP = 1
WEEKDAY_GROUP = 2
POSTFIX_GROUP = 3


class NLWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_of_week = match.group(WEEKDAY_GROUP).lower()
        weekday = WEEKDAY_DICTIONARY.get(day_of_week)
        if weekday is None:
            return None

        prefix = match.group(PREFIX_GROUP)
        postfix = match.group(POSTFIX_GROUP)
        modifier_word = (prefix or postfix or "").lower()

        modifier = None
        if modifier_word in ("vorige", "afgelopen"):
            modifier = "last"
        elif modifier_word in ("volgende", "komende", "aankomende"):
            modifier = "next"
        elif modifier_word == "deze":
            modifier = "this"

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
