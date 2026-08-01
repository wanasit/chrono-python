import re

from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY = {
    'sunday': 0,
    'sun': 0,
    'sun.': 0,
    'monday': 1,
    'mon': 1,
    'mon.': 1,
    'tuesday': 2,
    'tue': 2,
    'tue.': 2,
    'wednesday': 3,
    'wed': 3,
    'wed.': 3,
    'thursday': 4,
    'thurs': 4,
    'thurs.': 4,
    'thur': 4,
    'thur.': 4,
    'thu': 4,
    'thu.': 4,
    'friday': 5,
    'fri': 5,
    'fri.': 5,
    'saturday': 6,
    'sat': 6,
    'sat.': 6,
}


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
    'jan.': 1,
    'feb': 2,
    'feb.': 2,
    'mar': 3,
    'mar.': 3,
    'apr': 4,
    'apr.': 4,
    'may': 5,
    'jun': 6,
    'jun.': 6,
    'jul': 7,
    'jul.': 7,
    'aug': 8,
    'aug.': 8,
    'sep': 9,
    'sep.': 9,
    'sept': 9,
    'sept.': 9,
    'oct': 10,
    'oct.': 10,
    'nov': 11,
    'nov.': 11,
    'dec': 12,
    'dec.': 12
}

INTEGER_WORD_DICTIONARY = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
}

TIME_UNIT_DICTIONARY_NO_ABBR = {
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
    'quarter': Timeunit.QUARTER,
    'quarters': Timeunit.QUARTER,
    'year': Timeunit.YEAR,
    'years': Timeunit.YEAR,
}

TIME_UNIT_DICTIONARY = {
    's': Timeunit.SECOND,
    'sec': Timeunit.SECOND,
    'second': Timeunit.SECOND,
    'seconds': Timeunit.SECOND,
    'm': Timeunit.MINUTE,
    'min': Timeunit.MINUTE,
    'mins': Timeunit.MINUTE,
    'minute': Timeunit.MINUTE,
    'minutes': Timeunit.MINUTE,
    'h': Timeunit.HOUR,
    'hr': Timeunit.HOUR,
    'hrs': Timeunit.HOUR,
    'hour': Timeunit.HOUR,
    'hours': Timeunit.HOUR,
    'd': Timeunit.DAY,
    'day': Timeunit.DAY,
    'days': Timeunit.DAY,
    'w': Timeunit.WEEK,
    'wk': Timeunit.WEEK,
    'wks': Timeunit.WEEK,
    'week': Timeunit.WEEK,
    'weeks': Timeunit.WEEK,
    'mo': Timeunit.MONTH,
    'mon': Timeunit.MONTH,
    'mos': Timeunit.MONTH,
    'month': Timeunit.MONTH,
    'months': Timeunit.MONTH,
    'qtr': Timeunit.QUARTER,
    'quarter': Timeunit.QUARTER,
    'quarters': Timeunit.QUARTER,
    'y': Timeunit.YEAR,
    'yr': Timeunit.YEAR,
    'yrs': Timeunit.YEAR,
    'year': Timeunit.YEAR,
    'years': Timeunit.YEAR,
    **TIME_UNIT_DICTIONARY_NO_ABBR
}

PATTERN_ORDINAL_NUMBER = r'[0-9]{1,2}(?:st|nd|rd|th)?'
PATTERN_NUMBER = r'[0-9]+'

PATTERN_YEAR = r'(?:[1-9][0-9]{0,3}\s{0,2}(?:BE|AD|BC|BCE|CE)|[1-2][0-9]{3}|[5-9][0-9]|2[0-5])'

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|"
    r"half(?:\s{0,2}an?)?|an?\b(?:\s{0,2}few)?|few|several|the|a?\s{0,2}couple\s{0,2}(?:of)?)"
)

def parse_number_pattern(match_text: str) -> float:
    num = match_text.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num])
    elif num in ("a", "an", "the"):
        return 1.0
    elif 'few' in num:
        return 3.0
    elif 'half' in num:
        return 0.5
    elif 'couple' in num:
        return 2.0
    elif 'several' in num:
        return 7.0
    return float(num)

SINGLE_TIME_UNIT_PATTERN = f'({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY)})'
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

SINGLE_TIME_UNIT_NO_ABBR_PATTERN = f'({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY_NO_ABBR)})'

TIME_UNIT_CONNECTOR_PATTERN = r'\s{0,5},?(?:\s*and)?\s{0,5}'

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r'(?:(?:about|around)\s{0,3})?',
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN
)

TIME_UNITS_NO_ABBR_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_NO_ABBR_PATTERN,
    prefix=r'(?:(?:about|around)\s{0,3})?',
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN
)

def parse_ordinal_number(match_text: str) -> int:
    num = match_text.lower()
    num = num.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    return int(num)

def parse_year(match_text: str) -> int:
    # Buddhist Era
    if re.search(r'BE', match_text, re.IGNORECASE):
        year_num = re.sub(r'BE', '', match_text, flags=re.IGNORECASE).strip()
        return int(year_num) - 543

    # Before Christ / Before Common Era
    if re.search(r'BCE?', match_text, re.IGNORECASE):
        year_num = re.sub(r'BCE?', '', match_text, flags=re.IGNORECASE).strip()
        return -int(year_num)

    # Anno Domini / Common Era / normal years
    year_num = re.sub(r'(?:AD|CE)', '', match_text, flags=re.IGNORECASE).strip()
    raw_year = int(year_num)
    return calendars.find_most_likely_ad_year(raw_year)


def parse_duration(timeunit_text: str) -> dict[Timeunit, int] | None:
    fragments = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
        if re.match(r'^[a-zA-Z]+$', match.group(0)):
            remaining_text = remaining_text[match.end():]
            match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
            continue
            
        num = parse_number_pattern(match.group(1))
        unit_str = match.group(2).lower()
        unit = TIME_UNIT_DICTIONARY[unit_str]
        
        if unit in fragments:
            fragments[unit] += num
        else:
            fragments[unit] = num
            
        remaining_text = remaining_text[match.end():]
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
        
    if not fragments:
        return None
        
    return normalize_duration(fragments)

def parse_time_units(match_text: str) -> dict[Timeunit, int]:
    # Backward compatible helper
    duration = parse_duration(match_text)
    return duration if duration is not None else {}

