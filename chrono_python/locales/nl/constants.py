import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    # Zondag
    "zondag": 0,
    "zon": 0,
    "zon.": 0,
    "zo": 0,
    "zo.": 0,
    # Maandag
    "maandag": 1,
    "ma": 1,
    "ma.": 1,
    # Dinsdag
    "dinsdag": 2,
    "din": 2,
    "din.": 2,
    "di": 2,
    "di.": 2,
    # Woensdag
    "woensdag": 3,
    "woe": 3,
    "woe.": 3,
    "wo": 3,
    "wo.": 3,
    # Donderdag
    "donderdag": 4,
    "dond": 4,
    "dond.": 4,
    "do": 4,
    "do.": 4,
    # Vrijdag
    "vrijdag": 5,
    "vrij": 5,
    "vrij.": 5,
    "vr": 5,
    "vr.": 5,
    # Zaterdag
    "zaterdag": 6,
    "zat": 6,
    "zat.": 6,
    "za": 6,
    "za.": 6,
}

MONTH_DICTIONARY: dict[str, int] = {
    "januari": 1,
    "jan": 1,
    "jan.": 1,
    "februari": 2,
    "feb": 2,
    "feb.": 2,
    "maart": 3,
    "mar": 3,
    "mar.": 3,
    "mrt": 3,
    "mrt.": 3,
    "april": 4,
    "apr": 4,
    "apr.": 4,
    "mei": 5,
    "juni": 6,
    "jun": 6,
    "jun.": 6,
    "juli": 7,
    "jul": 7,
    "jul.": 7,
    "augustus": 8,
    "aug": 8,
    "aug.": 8,
    "september": 9,
    "sep": 9,
    "sep.": 9,
    "sept": 9,
    "sept.": 9,
    "oktober": 10,
    "okt": 10,
    "okt.": 10,
    "november": 11,
    "nov": 11,
    "nov.": 11,
    "december": 12,
    "dec": 12,
    "dec.": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "een": 1,
    "twee": 2,
    "drie": 3,
    "vier": 4,
    "vijf": 5,
    "zes": 6,
    "zeven": 7,
    "acht": 8,
    "negen": 9,
    "tien": 10,
    "elf": 11,
    "twaalf": 12,
}

ORDINAL_WORD_DICTIONARY: dict[str, int] = {
    "eerste": 1,
    "tweede": 2,
    "derde": 3,
    "vierde": 4,
    "vijfde": 5,
    "zesde": 6,
    "zevende": 7,
    "achtste": 8,
    "negende": 9,
    "tiende": 10,
    "elfde": 11,
    "twaalfde": 12,
    "dertiende": 13,
    "veertiende": 14,
    "vijftiende": 15,
    "zestiende": 16,
    "zeventiende": 17,
    "achttiende": 18,
    "negentiende": 19,
    "twintigste": 20,
    "eenentwintigste": 21,
    "tweeëntwintigste": 22,
    "drieentwintigste": 23,
    "vierentwintigste": 24,
    "vijfentwintigste": 25,
    "zesentwintigste": 26,
    "zevenentwintigste": 27,
    "achtentwintig": 28,
    "negenentwintig": 29,
    "dertigste": 30,
    "eenendertigste": 31,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "sec": Timeunit.SECOND,
    "second": Timeunit.SECOND,
    "seconden": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "mins": Timeunit.MINUTE,
    "minute": Timeunit.MINUTE,
    "minuut": Timeunit.MINUTE,
    "minuten": Timeunit.MINUTE,
    "minuutje": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "hr": Timeunit.HOUR,
    "hrs": Timeunit.HOUR,
    "uur": Timeunit.HOUR,
    "u": Timeunit.HOUR,
    "uren": Timeunit.HOUR,
    "dag": Timeunit.DAY,
    "dagen": Timeunit.DAY,
    "week": Timeunit.WEEK,
    "weken": Timeunit.WEEK,
    "maand": Timeunit.MONTH,
    "maanden": Timeunit.MONTH,
    "jaar": Timeunit.YEAR,
    "jr": Timeunit.YEAR,
    "jaren": Timeunit.YEAR,
}

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+[\\.,][0-9]+|halve?|half|paar)"
)


def parse_number_pattern(match_str: str) -> float:
    num = match_str.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num])
    elif num == "paar":
        return 2.0
    elif num == "half" or re.match(r"halve?", num):
        return 0.5
    return float(num.replace(",", "."))


ORDINAL_NUMBER_PATTERN = f"(?:{patterns.match_any(ORDINAL_WORD_DICTIONARY)}|[0-9]{{1,2}}(?:ste|de)?)"


def parse_ordinal_number_pattern(match_str: str) -> int:
    num = match_str.lower()
    if num in ORDINAL_WORD_DICTIONARY:
        return ORDINAL_WORD_DICTIONARY[num]
    num = re.sub(r"(?:ste|de)$", "", num, flags=re.IGNORECASE)
    return int(num)


YEAR_PATTERN = r"(?:[1-9][0-9]{0,3}\s*(?:voor Christus|na Christus)|[1-2][0-9]{3}|[5-9][0-9])"


def parse_year(match_str: str) -> int:
    if re.search(r"voor Christus", match_str, re.IGNORECASE):
        cleaned = re.sub(r"voor Christus", "", match_str, flags=re.IGNORECASE).strip()
        return -int(cleaned)
    if re.search(r"na Christus", match_str, re.IGNORECASE):
        cleaned = re.sub(r"na Christus", "", match_str, flags=re.IGNORECASE).strip()
        return int(cleaned)
    raw_year_number = int(match_str)
    return calendars.find_most_likely_ad_year(raw_year_number)


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r"(?:(?:binnen|in)\s*)?",
)


def parse_duration(timeunit_text: str) -> dict[Timeunit, float] | None:
    fragments: dict[Timeunit, float] = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
        num = parse_number_pattern(match.group(1))
        unit = TIME_UNIT_DICTIONARY[match.group(2).lower()]
        if unit in fragments:
            fragments[unit] += num
        else:
            fragments[unit] = num
        remaining_text = remaining_text[match.end():]
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)

    if not fragments:
        return None
    return normalize_duration(fragments)
