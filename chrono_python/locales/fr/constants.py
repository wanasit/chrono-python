import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "dimanche": 0,
    "dim": 0,
    "dim.": 0,
    "lundi": 1,
    "lun": 1,
    "lun.": 1,
    "mardi": 2,
    "mar": 2,
    "mar.": 2,
    "mercredi": 3,
    "mer": 3,
    "mer.": 3,
    "jeudi": 4,
    "jeu": 4,
    "jeu.": 4,
    "vendredi": 5,
    "ven": 5,
    "ven.": 5,
    "samedi": 6,
    "sam": 6,
    "sam.": 6,
}


MONTH_DICTIONARY: dict[str, int] = {
    "janvier": 1,
    "jan": 1,
    "jan.": 1,
    "janv": 1,
    "janv.": 1,
    "février": 2,
    "fév": 2,
    "fév.": 2,
    "févr": 2,
    "févr.": 2,
    "fevrier": 2,
    "fev": 2,
    "fev.": 2,
    "fevr": 2,
    "fevr.": 2,
    "mars": 3,
    "mar": 3,
    "mar.": 3,
    "avril": 4,
    "avr": 4,
    "avr.": 4,
    "mai": 5,
    "juin": 6,
    "juin.": 6,
    "jun": 6,
    "jun.": 6,
    "juillet": 7,
    "juil": 7,
    "juil.": 7,
    "jul": 7,
    "jul.": 7,
    "août": 8,
    "août.": 8,
    "aout": 8,
    "aout.": 8,
    "septembre": 9,
    "sep": 9,
    "sep.": 9,
    "sept": 9,
    "sept.": 9,
    "octobre": 10,
    "oct": 10,
    "oct.": 10,
    "novembre": 11,
    "nov": 11,
    "nov.": 11,
    "décembre": 12,
    "decembre": 12,
    "dec": 12,
    "dec.": 12,
    "déc": 12,
    "déc.": 12,
}


INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "un": 1,
    "une": 1,
    "deux": 2,
    "trois": 3,
    "quatre": 4,
    "cinq": 5,
    "six": 6,
    "sept": 7,
    "huit": 8,
    "neuf": 9,
    "dix": 10,
    "onze": 11,
    "douze": 12,
    "treize": 13,
}


TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "sec": Timeunit.SECOND,
    "seconde": Timeunit.SECOND,
    "secondes": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "mins": Timeunit.MINUTE,
    "minute": Timeunit.MINUTE,
    "minutes": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "hr": Timeunit.HOUR,
    "hrs": Timeunit.HOUR,
    "heure": Timeunit.HOUR,
    "heures": Timeunit.HOUR,
    "jour": Timeunit.DAY,
    "jours": Timeunit.DAY,
    "semaine": Timeunit.WEEK,
    "semaines": Timeunit.WEEK,
    "mois": Timeunit.MONTH,
    "trimestre": Timeunit.QUARTER,
    "trimestres": Timeunit.QUARTER,
    "ans": Timeunit.YEAR,
    "année": Timeunit.YEAR,
    "années": Timeunit.YEAR,
}


NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|une?\\b|quelques?|demi-?)"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    elif num_str in ("une", "un"):
        return 1.0
    elif re.match(r"quelques?", num_str):
        return 3.0
    elif re.match(r"demi-?", num_str):
        return 0.5
    return float(num_str)


ORDINAL_NUMBER_PATTERN = r"(?:[0-9]{1,2}(?:er)?)"


def parse_ordinal_number(match_str: str) -> int:
    num_str = re.sub(r"(?:er)$", "", match_str, flags=re.IGNORECASE)
    return int(num_str)


YEAR_PATTERN = (
    r"(?:[1-9][0-9]{0,3}\s*(?:AC|AD|p\.\s*C(?:hr?)?\.\s*n\.)|[1-2][0-9]{3}|[5-9][0-9])"
)


def parse_year(match_str: str) -> int:
    if re.search(r"AC", match_str, re.IGNORECASE):
        cleaned = re.sub(r"[^\d]+", "", match_str)
        return -int(cleaned)
    if re.search(r"AD|C", match_str, re.IGNORECASE):
        cleaned = re.sub(r"[^\d]+", "", match_str)
        return int(cleaned)
    year_num = int(match_str)
    if year_num < 100:
        if year_num > 50:
            year_num += 1900
        else:
            year_num += 2000
    return year_num


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNIT_CONNECTOR_PATTERN = r"\s{0,5},?(?:\s*et)?\s{0,5}"

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix="",
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN
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
