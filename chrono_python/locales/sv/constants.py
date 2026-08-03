import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "söndag": 0,
    "sön": 0,
    "so": 0,
    "måndag": 1,
    "mån": 1,
    "må": 1,
    "tisdag": 2,
    "tis": 2,
    "ti": 2,
    "onsdag": 3,
    "ons": 3,
    "on": 3,
    "torsdag": 4,
    "tors": 4,
    "to": 4,
    "fredag": 5,
    "fre": 5,
    "fr": 5,
    "lördag": 6,
    "lör": 6,
    "lö": 6,
}

MONTH_DICTIONARY: dict[str, int] = {
    "januari": 1,
    "jan": 1,
    "jan.": 1,
    "februari": 2,
    "feb": 2,
    "feb.": 2,
    "mars": 3,
    "mar": 3,
    "mar.": 3,
    "april": 4,
    "apr": 4,
    "apr.": 4,
    "maj": 5,
    "juni": 6,
    "jun": 6,
    "jun.": 6,
    "juli": 7,
    "jul": 7,
    "jul.": 7,
    "augusti": 8,
    "aug": 8,
    "aug.": 8,
    "september": 9,
    "sep": 9,
    "sep.": 9,
    "sept": 9,
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

ORDINAL_NUMBER_DICTIONARY: dict[str, int] = {
    "första": 1,
    "andra": 2,
    "tredje": 3,
    "fjärde": 4,
    "femte": 5,
    "sjätte": 6,
    "sjunde": 7,
    "åttonde": 8,
    "nionde": 9,
    "tionde": 10,
    "elfte": 11,
    "tolfte": 12,
    "trettonde": 13,
    "fjortonde": 14,
    "femtonde": 15,
    "sextonde": 16,
    "sjuttonde": 17,
    "artonde": 18,
    "nittonde": 19,
    "tjugonde": 20,
    "tjugoförsta": 21,
    "tjugoandra": 22,
    "tjugotredje": 23,
    "tjugofjärde": 24,
    "tjugofemte": 25,
    "tjugosjätte": 26,
    "tjugosjunde": 27,
    "tjugoåttonde": 28,
    "tjugonionde": 29,
    "trettionde": 30,
    "trettioförsta": 31,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "en": 1,
    "ett": 1,
    "två": 2,
    "tre": 3,
    "fyra": 4,
    "fem": 5,
    "sex": 6,
    "sju": 7,
    "åtta": 8,
    "nio": 9,
    "tio": 10,
    "elva": 11,
    "tolv": 12,
    "tretton": 13,
    "fjorton": 14,
    "femton": 15,
    "sexton": 16,
    "sjutton": 17,
    "arton": 18,
    "nitton": 19,
    "tjugo": 20,
    "trettio": 30,
    "trettiо": 30,
    "fyrtio": 40,
    "femtio": 50,
    "sextio": 60,
    "sjuttio": 70,
    "åttio": 80,
    "nittio": 90,
    "hundra": 100,
    "tusen": 1000,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "sek": Timeunit.SECOND,
    "sekund": Timeunit.SECOND,
    "sekunder": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "minut": Timeunit.MINUTE,
    "minuter": Timeunit.MINUTE,
    "tim": Timeunit.HOUR,
    "timme": Timeunit.HOUR,
    "timmar": Timeunit.HOUR,
    "dag": Timeunit.DAY,
    "dagar": Timeunit.DAY,
    "vecka": Timeunit.WEEK,
    "veckor": Timeunit.WEEK,
    "mån": Timeunit.MONTH,
    "månad": Timeunit.MONTH,
    "månader": Timeunit.MONTH,
    "år": Timeunit.YEAR,
    "kvartаl": Timeunit.QUARTER,
    "kvartal": Timeunit.QUARTER,
}

TIME_UNIT_NO_ABBR_DICTIONARY: dict[str, Timeunit] = {
    "sekund": Timeunit.SECOND,
    "sekunder": Timeunit.SECOND,
    "minut": Timeunit.MINUTE,
    "minuter": Timeunit.MINUTE,
    "timme": Timeunit.HOUR,
    "timmar": Timeunit.HOUR,
    "dag": Timeunit.DAY,
    "dagar": Timeunit.DAY,
    "vecka": Timeunit.WEEK,
    "veckor": Timeunit.WEEK,
    "månad": Timeunit.MONTH,
    "månader": Timeunit.MONTH,
    "år": Timeunit.YEAR,
    "kvartal": Timeunit.QUARTER,
}

NUMBER_PATTERN = f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|\\d+)"
ORDINAL_NUMBER_PATTERN = f"(?:{patterns.match_any(ORDINAL_NUMBER_DICTIONARY)}|\\d{{1,2}}(?:e|:e))"
TIME_UNIT_PATTERN = f"(?:{patterns.match_any(TIME_UNIT_DICTIONARY)})"

SINGLE_TIME_UNIT_PATTERN = f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

SINGLE_TIME_UNIT_NO_ABBR_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_NO_ABBR_DICTIONARY)})\\s{{0,5}}"
)

TIME_UNITS_PATTERN = patterns.repeat(SINGLE_TIME_UNIT_PATTERN, prefix="")
TIME_UNITS_NO_ABBR_PATTERN = patterns.repeat(SINGLE_TIME_UNIT_NO_ABBR_PATTERN, prefix="")


def parse_number_pattern(match_str: str) -> int:
    num = match_str.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return INTEGER_WORD_DICTIONARY[num]
    return int(num)


def parse_ordinal_number_pattern(match_str: str) -> int:
    num = match_str.lower()
    if num in ORDINAL_NUMBER_DICTIONARY:
        return ORDINAL_NUMBER_DICTIONARY[num]
    cleaned = re.sub(r"(?:e|:e)$", "", num, flags=re.IGNORECASE)
    return int(cleaned)


def parse_year(match_str: str) -> int:
    if re.search(r"\d+", match_str):
        year_number = int(match_str)
        if year_number < 100:
            year_number = calendars.find_most_likely_ad_year(year_number)
        return year_number

    num = match_str.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return INTEGER_WORD_DICTIONARY[num]

    return int(match_str)


def parse_duration(timeunit_text: str) -> dict[Timeunit, int] | None:
    fragments: dict[Timeunit, float] = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
        num = parse_number_pattern(match.group(1))
        unit = TIME_UNIT_DICTIONARY[match.group(2).lower()]
        fragments[unit] = fragments.get(unit, 0) + num
        remaining_text = remaining_text[match.end():]
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)

    if not fragments:
        return None

    return normalize_duration(fragments)
