import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "sonntag": 0,
    "so": 0,
    "so.": 0,
    "montag": 1,
    "mo": 1,
    "mo.": 1,
    "dienstag": 2,
    "di": 2,
    "di.": 2,
    "mittwoch": 3,
    "mi": 3,
    "mi.": 3,
    "donnerstag": 4,
    "do": 4,
    "do.": 4,
    "freitag": 5,
    "fr": 5,
    "fr.": 5,
    "samstag": 6,
    "sa": 6,
    "sa.": 6,
    "sonnabend": 6,
}

FULL_MONTH_NAME_DICTIONARY: dict[str, int] = {
    "januar": 1,
    "jänner": 1,
    "janner": 1,
    "februar": 2,
    "märz": 3,
    "maerz": 3,
    "marz": 3,
    "april": 4,
    "mai": 5,
    "juni": 6,
    "juli": 7,
    "august": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "dezember": 12,
}

MONTH_DICTIONARY: dict[str, int] = {
    **FULL_MONTH_NAME_DICTIONARY,
    "jan": 1,
    "jan.": 1,
    "feb": 2,
    "feb.": 2,
    "mär": 3,
    "mär.": 3,
    "mar": 3,
    "mar.": 3,
    "apr": 4,
    "apr.": 4,
    "jun": 6,
    "jun.": 6,
    "jul": 7,
    "jul.": 7,
    "aug": 8,
    "aug.": 8,
    "sep": 9,
    "sep.": 9,
    "sept": 9,
    "sept.": 9,
    "okt": 10,
    "okt.": 10,
    "nov": 11,
    "nov.": 11,
    "dez": 12,
    "dez.": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "eins": 1,
    "ein": 1,
    "eine": 1,
    "einen": 1,
    "einer": 1,
    "einem": 1,
    "eines": 1,
    "zwei": 2,
    "zwo": 2,
    "drei": 3,
    "vier": 4,
    "fünf": 5,
    "fuenf": 5,
    "sechs": 6,
    "sieben": 7,
    "acht": 8,
    "neun": 9,
    "zehn": 10,
    "elf": 11,
    "zwölf": 12,
    "zwoelf": 12,
}

ORDINAL_WORD_DICTIONARY: dict[str, int] = {
    "erste": 1,
    "ersten": 1,
    "erster": 1,
    "erstes": 1,
    "erstem": 1,
    "zweite": 2,
    "zweiten": 2,
    "zweiter": 2,
    "zweites": 2,
    "dritte": 3,
    "dritten": 3,
    "dritter": 3,
    "drittes": 3,
    "vierte": 4,
    "vierten": 4,
    "fünfte": 5,
    "fuenfte": 5,
    "sechste": 6,
    "siebte": 7,
    "achtte": 8,
    "achte": 8,
    "neunte": 9,
    "zehnte": 10,
    "elfte": 11,
    "zwölfte": 12,
    "zwoelfte": 12,
}

TIME_UNIT_DICTIONARY_NO_ABBR: dict[str, Timeunit] = {
    "sekunde": Timeunit.SECOND,
    "sekunden": Timeunit.SECOND,
    "minute": Timeunit.MINUTE,
    "minuten": Timeunit.MINUTE,
    "stunde": Timeunit.HOUR,
    "stunden": Timeunit.HOUR,
    "tag": Timeunit.DAY,
    "tage": Timeunit.DAY,
    "tagen": Timeunit.DAY,
    "woche": Timeunit.WEEK,
    "wochen": Timeunit.WEEK,
    "monat": Timeunit.MONTH,
    "monate": Timeunit.MONTH,
    "monaten": Timeunit.MONTH,
    "quartal": Timeunit.QUARTER,
    "quartale": Timeunit.QUARTER,
    "quartalen": Timeunit.QUARTER,
    "jahr": Timeunit.YEAR,
    "jahre": Timeunit.YEAR,
    "jahren": Timeunit.YEAR,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "s": Timeunit.SECOND,
    "sek": Timeunit.SECOND,
    "sek.": Timeunit.SECOND,
    "m": Timeunit.MINUTE,
    "min": Timeunit.MINUTE,
    "min.": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "std": Timeunit.HOUR,
    "std.": Timeunit.HOUR,
    "st": Timeunit.HOUR,
    "st.": Timeunit.HOUR,
    "t": Timeunit.DAY,
    "w": Timeunit.WEEK,
    "j": Timeunit.YEAR,
    **TIME_UNIT_DICTIONARY_NO_ABBR,
}

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|einige[nr]?|einigen|ein paar|paar|halbe[nr]?|halb)"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower().strip()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    elif "einige" in num_str:
        return 3.0
    elif "halb" in num_str:
        return 0.5
    elif "paar" in num_str:
        return 2.0
    return float(num_str)


# Alias parseNumberPattern for compatibility
parseNumberPattern = parse_number_pattern


ORDINAL_NUMBER_PATTERN = r"(?:[0-9]{1,2}(?:\.)?)"


def parse_ordinal_number(match_str: str) -> int:
    num_str = match_str.rstrip(".")
    return int(num_str)


YEAR_PATTERN = r"(?:[1-9][0-9]{0,3}\s*(?:v\.?\s*Chr\.?|n\.?\s*Chr\.?|v\.?\s*u\.?\s*Z\.?|n\.?\s*u\.?\s*Z\.?)|[1-2][0-9]{3}|[0-9]{2})"


def parse_year(match_str: str) -> int:
    if re.search(r"v\.?\s*Chr\.?|v\.?\s*u\.?\s*Z\.?", match_str, re.IGNORECASE):
        cleaned = re.sub(r"[^\d]+", "", match_str)
        return -int(cleaned)
    if re.search(r"n\.?\s*Chr\.?|n\.?\s*u\.?\s*Z\.?", match_str, re.IGNORECASE):
        cleaned = re.sub(r"[^\d]+", "", match_str)
        return int(cleaned)
    raw_year = int(match_str)
    return calendars.find_most_likely_ad_year(raw_year)


# Alias parseYear for compatibility
parseYear = parse_year


SINGLE_TIME_UNIT_PATTERN = f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY)})"
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

SINGLE_TIME_UNIT_NO_ABBR_PATTERN = f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY_NO_ABBR)})"

TIME_UNIT_CONNECTOR_PATTERN = r"\s{0,5},?(?:\s*und)?\s{0,5}"

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r"(?:(?:etwa|ca\.?|ungefähr|rund)\s{0,3})?",
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN,
)

TIME_UNITS_NO_ABBR_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_NO_ABBR_PATTERN,
    prefix=r"(?:(?:etwa|ca\.?|ungefähr|rund)\s{0,3})?",
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN,
)


def parse_duration(timeunit_text: str) -> dict[Timeunit, int] | None:
    fragments: dict[Timeunit, float] = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
        if re.match(r"^[a-zA-Z]+$", match.group(0)):
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


# Alias parseDuration for compatibility
parseDuration = parse_duration
