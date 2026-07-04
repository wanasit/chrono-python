import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en.constants import WEEKDAY_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:on\s*?)?"
    r"(?:(this|last|past|next)\s*)?"
    rf"({patterns.match_any(WEEKDAY_DICTIONARY)}|weekend|weekday)"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(?:of\s*)?(this|last|past|next)\s*week)?"
    r"(?=\W|$)",
    re.IGNORECASE
)

PREFIX_GROUP = 1
WEEKDAY_GROUP = 2
POSTFIX_GROUP = 3


class ENWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        prefix = match[PREFIX_GROUP]
        postfix = match[POSTFIX_GROUP]

        modifier_word = prefix or postfix or ""
        modifier_word = modifier_word.lower()

        modifier = None
        if modifier_word in ("last", "past"):
            modifier = "last"
        elif modifier_word == "next":
            modifier = "next"
        elif modifier_word == "this":
            modifier = "this"

        weekday_word = match[WEEKDAY_GROUP].lower()

        if weekday_word in WEEKDAY_DICTIONARY:
            weekday = WEEKDAY_DICTIONARY[weekday_word]
        elif weekday_word == "weekend":
            weekday = 0 if modifier == "last" else 6
        elif weekday_word == "weekday":
            ref_weekday = (context.reference.datetime().weekday() + 1) % 7
            if ref_weekday == 0 or ref_weekday == 6:
                weekday = 5 if modifier == "last" else 1
            else:
                weekday = ref_weekday - 1
                weekday = weekday - 1 if modifier == "last" else weekday + 1
                weekday = (weekday % 5) + 1
        else:
            return None

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
