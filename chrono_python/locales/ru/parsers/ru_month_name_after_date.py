import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"(?:с)?\s*"
    f"({constants.ORDINAL_NUMBER_PATTERN})"
    r"(?:\s{0,3}(?:по|-|–|до)?\s{0,3}"
    f"({constants.ORDINAL_NUMBER_PATTERN}))?"
    r"(?:-|/|\s{0,3}(?:of)?\s{0,3})"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"(?:(?:-|/|,?\s{0,3})"
    f"({constants.YEAR_PATTERN}(?![^\\s]\\d)))?",
    re.IGNORECASE,
)


class RUMonthNameAfterDate(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_str = match.group(1)
        day = constants.parse_ordinal_number_pattern(day_str)
        if day > 31:
            return None

        month = constants.MONTH_DICTIONARY[match.group(3).lower()]

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.DAY, day)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        if not match.group(2):
            return moment

        end_day = constants.parse_ordinal_number_pattern(match.group(2))
        end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
        return context.create_parsed_result(
            match.start(), match.end(), start=moment, end=end_moment
        )
