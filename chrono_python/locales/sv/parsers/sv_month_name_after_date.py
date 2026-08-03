import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.sv import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"(?:den\s*?)?"
    r"([0-9]{1,2})"
    r"(?:\s*(?:till|\-|\–|\s)\s*([0-9]{1,2}))?\s*"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"(?:(?:-|/|,?\s*)([0-9]{4}(?![^\s]\d)))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class SVMonthNameAfterDate(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month = constants.MONTH_DICTIONARY[match.group(3).lower()]
        day = int(match.group(1))
        if day > 31:
            return None

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

        end_day = int(match.group(2))
        end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
        return context.create_parsed_result(
            match.start(), match.end(), start=moment, end=end_moment
        )
