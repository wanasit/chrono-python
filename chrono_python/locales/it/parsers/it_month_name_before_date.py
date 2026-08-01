import re
from chrono_python import chrono
from chrono_python.locales.it import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    r"(?:-|/|\s*,?\s*)"
    f"({constants.ORDINAL_NUMBER_PATTERN})(?!\\s*(?:am|pm))\\s*"
    r"(?:"
    r"(?:al|\-)\s*"
    f"({constants.ORDINAL_NUMBER_PATTERN})\\s*"
    r")?"
    r"(?:"
    r"(?:-|/|\s*,\s*|\s+)"
    f"({constants.YEAR_PATTERN})"
    r")?"
    r"(?=\W|$)(?!\:\d)",
    re.IGNORECASE,
)


class ITMonthNameBeforeDate(chrono.Parser):
    def __init__(self, should_skip_year_like_date: bool = False):
        self.should_skip_year_like_date = should_skip_year_like_date

    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month = constants.MONTH_DICTIONARY[match.group(1).lower()]
        day_str = match.group(2)
        day = constants.parse_ordinal_number_pattern(day_str)
        if day > 31:
            return None

        if self.should_skip_year_like_date:
            if not match.group(3) and not match.group(4) and re.match(r"^2[0-5]$", day_str):
                return None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.DAY, day)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        if not match.group(3):
            return context.create_parsed_result(match.start(), match.end(), moment)

        end_day = constants.parse_ordinal_number_pattern(match.group(3))
        end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
        return context.create_parsed_result(
            match.start(), match.end(), start=moment, end=end_moment
        )
