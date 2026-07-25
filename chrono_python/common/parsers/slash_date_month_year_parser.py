import re

from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.common import calendars
from chrono_python.utils.patterns import to_hankaku

# Regex matching date formats with slash "/", dot ".", or hyphen "-"
# e.g., 7/10, 7/12/2020, 7.12.2020, 30-12-16, ７／１０
PATTERN = re.compile(
    r'([^\d０-９]|^)'
    r'([0-3０-３]?[0-9０-９])[\/\.\-／]([0-3０-３]?[0-9０-９])'
    r'(?:[\/\.\-／]([0-9０-９]{4}|[0-9０-９]{2}))?'
    r'(?=[^\d０-９]|$)',
    re.IGNORECASE
)


class SlashDateMonthYearParser(chrono.Parser):
    """Parser for date formats with slash "/" (or dot ".") between numbers.

    For examples:
    - 7/10
    - 7/12/2020
    - 7.12.2020
    """

    def __init__(self, little_endian: bool = False):
        self.little_endian = little_endian

    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        group1 = match.group(1) or ""

        index = match.start() + len(group1)
        index_end = match.end()

        # Skip if there are digits immediately before or after the matched segment
        if index > 0:
            text_before = context.text[:index]
            if re.search(r'[\d０-９][/\.─\-／]?$', text_before):
                return None

        if index_end < len(context.text):
            text_after = context.text[index_end:]
            if re.match(r'^[/\.─\-／]?[\d０-９]', text_after):
                return None

        text = context.text[index:index_end]

        # Skip version-like numbers (e.g., '1.12', '1.12.12')
        if re.match(r'^\d\.\d$', text) or re.match(r'^\d\.\d{1,2}\.\d{1,2}\s*$', text):
            return None

        # MM/dd -> OK, MM.dd -> NG (must have a slash unless it has a year)
        if not match.group(4) and '/' not in text and '／' not in text:
            return None

        # Resolve month/day group index based on endianness
        month_group = 3 if self.little_endian else 2
        day_group = 2 if self.little_endian else 3

        month = int(to_hankaku(match.group(month_group)))
        day = int(to_hankaku(match.group(day_group)))

        # Check and swap month and day if month is > 12 (implying wrong endianness guess)
        if month < 1 or month > 12:
            if month > 12:
                if 1 <= day <= 12 and month <= 31:
                    day, month = month, day
                else:
                    return None
            else:
                return None

        if day < 1 or day > 31:
            return None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.DAY, day)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(4):
            raw_year = int(to_hankaku(match.group(4)))
            year = calendars.find_most_likely_ad_year(raw_year)
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        return context.create_parsed_result(index, index_end, moment)
