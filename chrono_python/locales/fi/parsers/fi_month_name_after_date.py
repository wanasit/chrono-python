import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.fi import constants
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"([0-9]{1,2})\.?"
    r"(?:\s*(?:-|\–|\s)\s*([0-9]{1,2})\.?)?\s*"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"(?:(?:-|/|,?\s*)([0-9]{4}(?![^\s]\d)))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class FIMonthNameAfterDate(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day_str = match.group(1)
        day = int(day_str)
        if day > 31:
            return None

        month = constants.MONTH_DICTIONARY[match.group(3).lower()]

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.DAY, day)

        year_str = match.group(4)
        if year_str:
            year_num = constants.parse_year(year_str)
            moment.assign(CivilTimeComponent.YEAR, year_num)
        else:
            year_num = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year_num)

        end_day_str = match.group(2)
        if end_day_str:
            end_day = int(end_day_str)
            end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
            return context.create_parsed_result(
                match.start(), match.end(), start=moment, end=end_moment
            )

        return moment
