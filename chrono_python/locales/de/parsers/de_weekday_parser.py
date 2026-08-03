import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.de.constants import WEEKDAY_DICTIONARY
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:am\s*)?"
    r"(?:(diesen|diese|dieser|diesem|dieses|letzten|letzte|letzter|letztem|letztes|vergangenen|vergangene|vergangener|vergangenem|vergangenes|nächsten|nächste|nächster|nächstem|nächstes|naechsten|naechste|naechster|naechstem|naechstes|kommenden|kommende|kommender|kommendem|kommendes)\s*)?"
    rf"({patterns.match_any(WEEKDAY_DICTIONARY)}|wochenende)"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(letzte\s*woche|nächste\s*woche|naechste\s*woche|diese\s*woche|letzten|letzte|vergangenen|vergangene|nächsten|nächste|naechsten|naechste|kommenden|kommende))?"
    r"(?=\W|\d|$)",
    re.IGNORECASE,
)


class DEWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier_word = (match.group(1) or match.group(3) or "").lower()
        modifier = None
        if re.search(r"letzte|vergangene", modifier_word):
            modifier = "last"
        elif re.search(r"nächste|naechste|kommende", modifier_word):
            modifier = "next"
        elif re.search(r"diese", modifier_word):
            modifier = "this"

        weekday_word = match.group(2).lower()
        if weekday_word in WEEKDAY_DICTIONARY:
            weekday = WEEKDAY_DICTIONARY[weekday_word]
        elif weekday_word == "wochenende":
            weekday = 0 if modifier == "last" else 6
        else:
            return None

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
