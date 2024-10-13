import re

from chrono_python.types import DateTimeUnit
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
    'second': DateTimeUnit.SECOND,
    'seconds': DateTimeUnit.SECOND,
    'minute': DateTimeUnit.MINUTE,
    'minutes': DateTimeUnit.MINUTE,
    'hour': DateTimeUnit.HOUR,
    'hours': DateTimeUnit.HOUR,
    'day': DateTimeUnit.DAY,
    'days': DateTimeUnit.DAY,
    'week': DateTimeUnit.WEEK,
    'weeks': DateTimeUnit.WEEK,
    'month': DateTimeUnit.MONTH,
    'months': DateTimeUnit.MONTH,
    'year': DateTimeUnit.YEAR,
    'years': DateTimeUnit.YEAR
}

TIME_UNIT_DICTIONARY = {
    **FULL_TIME_UNIT_DICTIONARY,
    's': DateTimeUnit.SECOND,
    'sec': DateTimeUnit.SECOND,
    'm': DateTimeUnit.MINUTE,
    'min': DateTimeUnit.MINUTE,
    'mins': DateTimeUnit.MINUTE,
    'h': DateTimeUnit.HOUR,
    'hr': DateTimeUnit.HOUR,
    'hrs': DateTimeUnit.HOUR,
    'd': DateTimeUnit.DAY,
    'w': DateTimeUnit.WEEK,
    'mon': DateTimeUnit.MONTH,
    'y': DateTimeUnit.YEAR,
    'yr': DateTimeUnit.YEAR,
    'yrs': DateTimeUnit.YEAR
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


def parse_time_units(match_text: str) -> dict[DateTimeUnit, int]:
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
