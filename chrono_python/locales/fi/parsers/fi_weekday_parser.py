import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.fi import constants
from chrono_python.utils import patterns
from chrono_python.common.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:(?:,|\(|\（)\s*)?"
    r"(?:(viime|edellinen|edellisenä|ensi|seuraava|seuraavana|tämä|tänä)\s*)?"
    rf"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
    r"(?:\s*(?:,|\)|\）))?"
    r"(?:\s*(viime|ensi|seuraava)\s*viikolla)?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class FIWeekdayParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1)
        day_of_week_str = match.group(2).lower()
        postfix = match.group(3)

        offset = constants.WEEKDAY_DICTIONARY[day_of_week_str]

        modifier_word = (prefix or postfix or "").lower()

        modifier = None
        if re.search(r"viime|edellinen|edellisenä", modifier_word):
            modifier = "last"
        elif re.search(r"ensi|seuraava|seuraavana", modifier_word):
            modifier = "next"

        return create_parsing_components_at_weekday(context.reference, offset, modifier)
