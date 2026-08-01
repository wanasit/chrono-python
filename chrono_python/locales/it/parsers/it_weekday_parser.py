import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.it import constants
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:(questo|questa|quest'|scorso|scorsa|prossimo|prossima)\s*)?"
    f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)}|weekend|fine\\s*settimana)"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(scorso|scorsa|prossimo|prossima)(?:\s*settimana)?)?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class ITWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier_word = (match.group(1) or match.group(3) or "").lower()
        modifier = None
        if modifier_word in ("scorso", "scorsa"):
            modifier = "last"
        elif modifier_word in ("prossimo", "prossima"):
            modifier = "next"
        elif modifier_word in ("questo", "questa", "quest'"):
            modifier = "this"

        weekday_word = match.group(2).lower()
        if weekday_word in constants.WEEKDAY_DICTIONARY:
            weekday = constants.WEEKDAY_DICTIONARY[weekday_word]
        elif weekday_word == "weekend" or re.search(r"fine\s*settimana", weekday_word):
            weekday = 0 if modifier == "last" else 6
        else:
            return None

        return create_parsing_components_at_weekday(context.reference, weekday, modifier)
