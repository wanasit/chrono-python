import re

from chrono_python.types import Timeunit
from chrono_python.utils import patterns

FULL_MONTH_NAME_DICTIONARY = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

MONTH_NAME_DICTIONARY = {
    **FULL_MONTH_NAME_DICTIONARY,
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}

FULL_TIME_UNIT_DICTIONARY = {
    'second': Timeunit.SECOND,
    'seconds': Timeunit.SECOND,
    'minute': Timeunit.MINUTE,
    'minutes': Timeunit.MINUTE,
    'hour': Timeunit.HOUR,
    'hours': Timeunit.HOUR,
    'day': Timeunit.DAY,
    'days': Timeunit.DAY,
    'week': Timeunit.WEEK,
    'weeks': Timeunit.WEEK,
    'month': Timeunit.MONTH,
    'months': Timeunit.MONTH,
    'year': Timeunit.YEAR,
    'years': Timeunit.YEAR
}

TIME_UNIT_DICTIONARY = {
    **FULL_TIME_UNIT_DICTIONARY,
    's': Timeunit.SECOND,
    'sec': Timeunit.SECOND,
    'm': Timeunit.MINUTE,
    'min': Timeunit.MINUTE,
    'mins': Timeunit.MINUTE,
    'h': Timeunit.HOUR,
    'hr': Timeunit.HOUR,
    'hrs': Timeunit.HOUR,
    'd': Timeunit.DAY,
    'w': Timeunit.WEEK,
    'mon': Timeunit.MONTH,
    'y': Timeunit.YEAR,
    'yr': Timeunit.YEAR,
    'yrs': Timeunit.YEAR
}

PATTERN_ORDINAL_NUMBER: str = r'[0-9]{1,2}(?:st|nd|rd|th)?'
PATTERN_NUMBER = r'[0-9]+'

PATTERN_YEAR: str = r'(?:[1-9][0-9]{0,3}\\s{0,2}(?:BE|AD|BC|BCE|CE)|[1-2][0-9]{3}|[5-9][0-9]|2[0-5])'

PATTERN_SINGLE_TIME_UNIT = f'({PATTERN_NUMBER})\\s{{0,4}}({patterns.match_any(TIME_UNIT_DICTIONARY)})'
PATTERN_SINGLE_TIME_UNIT_COMPILED = re.compile(PATTERN_SINGLE_TIME_UNIT, re.IGNORECASE)

PATTERN_TIME_UNITS = patterns.repeat(f'{PATTERN_SINGLE_TIME_UNIT}')


def parse_ordinal_number(match_text: str) -> int:
    num = match_text.lower()

    num = num.replace('st', '')
    num = num.replace('nd', '')
    num = num.replace('rd', '')
    num = num.replace('th', '')
    return int(num)


def parse_year(match_text: str) -> int:
    year = match_text.lower()

    year = year.replace('be', '')
    year = year.replace('ad', '')
    year = year.replace('bc', '')
    year = year.replace('bce', '')
    year = year.replace('ce', '')
    return int(year)


def parse_time_units(match_text: str) -> dict[Timeunit, int]:
    result = {}
    remaining_text = match_text
    match = PATTERN_SINGLE_TIME_UNIT_COMPILED.search(remaining_text)
    while match:
        value = int(match.group(1))
        unit = match.group(2).lower()
        result[TIME_UNIT_DICTIONARY[unit]] = value

        remaining_text = remaining_text[match.end():]
        match = PATTERN_SINGLE_TIME_UNIT_COMPILED.search(remaining_text)

    return result
