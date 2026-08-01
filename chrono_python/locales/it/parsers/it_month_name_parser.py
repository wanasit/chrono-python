import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.it import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"((?:a|in|di|del)\s*)?"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"\s*"
    r"(?:"
    rf"(?:,|-|del)?\s*({constants.YEAR_PATTERN})"
    r")?"
    r"(?=[^\s\w]|\s+[^0-9]|\s+$|$)",
    re.IGNORECASE,
)


class ITMonthNameParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month_name = match.group(2).lower()
        if len(match.group(0)) <= 3 and month_name not in constants.FULL_MONTH_NAME_DICTIONARY:
            return None

        prefix = match.group(1) or ""
        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.imply(CivilTimeComponent.DAY, 1)

        month = constants.MONTH_DICTIONARY[month_name]
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(3):
            year_str = match.group(3)
            sep = match.group(0)[len(prefix) + len(match.group(2)): match.group(0).find(year_str)]
            if "-" in sep and len(year_str) <= 2:
                return None
            year = constants.parse_year(year_str)
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, 1)
            moment.imply(CivilTimeComponent.YEAR, year)

        if prefix:
            start_index = match.start() + len(prefix)
            return context.create_parsed_result(start_index, match.end(), moment)

        return moment
