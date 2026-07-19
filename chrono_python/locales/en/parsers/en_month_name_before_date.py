import logging
import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

# Pattern for Month-Day-Year formats (e.g., "January 1st, 2023", "Jan 1 2023", "Feb 10-12, 2024")
# Examples:
# - "January 1st, 2023"
# - "Jan 1 2023"
# - "Feb 10-12, 2024"
PATTERN = re.compile(
    f'({patterns.match_any(constants.MONTH_NAME_DICTIONARY)})' +  # Group 1: Month
    f'(?:\\s*[,-/]?\\s*)' +
    f'({constants.PATTERN_ORDINAL_NUMBER})' +  # Group 2: Day
    (f'(?:'
     + f'\\s{{0,3}}(?:to|-|–|until|through|till)\\s{{0,3}}'
     + f'({constants.PATTERN_ORDINAL_NUMBER})'  # Group 3: (Optional) End Day
     + f')?') +
    (f'(?:'
     + f'\\s{{0,3}}(?:-|/|,|\\s)\\s{{0,3}}'
     + f'({constants.PATTERN_YEAR}(?!\\S\\d))'  # Group 4: (Optional) Year
     + f')?') +
    f'(?=\\W|$)',
    re.IGNORECASE
)


class ENMonthNameBeforeDate(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        month_name = match.group(1).lower()
        month = constants.MONTH_NAME_DICTIONARY.get(month_name)
        # This check should ideally not be needed if patterns.match_any works correctly,
        # but as a safeguard:
        if month is None:
            return None  # Should not happen if regex matches

        day_str = match.group(2)
        day = constants.parse_ordinal_number(day_str)
        if day > 31:  # Basic validation
            return None

        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.DAY, day)

        year_str = match.group(4)
        if year_str:
            logging.info(f'{match.groups()}')
            year = constants.parse_year(year_str)
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        # Handling date range (e.g., "January 1st to 5th")
        end_day_str = match.group(3)
        if not end_day_str:
            # Not a range, just a single date
            # Further validation for day based on month/year could be added here
            # e.g., if day > calendars.days_in_month(moment.get(DateTimeComponent.YEAR), month): return None
            return moment

        # It's a date range
        end_day = constants.parse_ordinal_number(end_day_str)
        if end_day > 31:  # Basic validation for end_day
            return None

        # Create the end moment for the range. It shares the same month and year.
        end_moment = moment.clone()
        end_moment.assign(CivilTimeComponent.DAY, end_day)

        # Further validation for end_day (e.g., end_day > day, end_day fits in month) could be added.
        # For now, consistent with the little-endian parser's approach.

        return context.create_parsed_result(match.start(), match.end(), start=moment, end=end_moment)
