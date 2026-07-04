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
    year = match_text.lower()
    year = year.replace('be', '').replace('ad', '').replace('bc', '').replace('bce', '').replace('ce', '')
    return int(year)

def normalize_duration(fragments: dict[Timeunit | str, float]) -> dict[Timeunit, int]:
    import math
    
    quarter_val = fragments.get(Timeunit.QUARTER, 0.0) + fragments.get('quarter', 0.0)
    
    years = fragments.get(Timeunit.YEAR, 0.0)
    months = fragments.get(Timeunit.MONTH, 0.0) + quarter_val * 3.0
    weeks = fragments.get(Timeunit.WEEK, 0.0)
    days = fragments.get(Timeunit.DAY, 0.0)
    hours = fragments.get(Timeunit.HOUR, 0.0)
    minutes = fragments.get(Timeunit.MINUTE, 0.0)
    seconds = fragments.get(Timeunit.SECOND, 0.0)
    milliseconds = fragments.get(Timeunit.MILLI_SECOND, 0.0)
    
    # YEAR -> MONTH
    floor_years = math.floor(years)
    rem_years = years - floor_years
    if rem_years > 0:
        months += rem_years * 12.0
        
    # MONTH -> WEEK
    floor_months = math.floor(months)
    rem_months = months - floor_months
    if rem_months > 0:
        weeks += rem_months * 4.0
        
    # WEEK -> DAY
    floor_weeks = math.floor(weeks)
    rem_weeks = weeks - floor_weeks
    if rem_weeks > 0:
        days += rem_weeks * 7.0
        
    # DAY -> HOUR
    floor_days = math.floor(days)
    rem_days = days - floor_days
    if rem_days > 0:
        hours += rem_days * 24.0
        
    # HOUR -> MINUTE
    floor_hours = math.floor(hours)
    rem_hours = hours - floor_hours
    if rem_hours > 0:
        minutes += rem_hours * 60.0
        
    # MINUTE -> SECOND
    floor_minutes = math.floor(minutes)
    rem_minutes = minutes - floor_minutes
    if rem_minutes > 0:
        seconds += rem_minutes * 60.0
        
    # SECOND -> MILLISECOND
    floor_seconds = math.floor(seconds)
    rem_seconds = seconds - floor_seconds
    if rem_seconds > 0:
        milliseconds += rem_seconds * 1000.0
        
    floor_milliseconds = math.floor(milliseconds)
    
    result = {}
    if floor_years != 0:
        result[Timeunit.YEAR] = int(floor_years)
    if floor_months != 0:
        result[Timeunit.MONTH] = int(floor_months)
    if floor_weeks != 0:
        result[Timeunit.WEEK] = int(floor_weeks)
    if floor_days != 0:
        result[Timeunit.DAY] = int(floor_days)
    if floor_hours != 0:
        result[Timeunit.HOUR] = int(floor_hours)
    if floor_minutes != 0:
        result[Timeunit.MINUTE] = int(floor_minutes)
    if floor_seconds != 0:
        result[Timeunit.SECOND] = int(floor_seconds)
    if floor_milliseconds != 0:
        result[Timeunit.MILLI_SECOND] = int(floor_milliseconds)
        
    return result

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

