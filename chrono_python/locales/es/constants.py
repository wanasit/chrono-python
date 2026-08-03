import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "domingo": 0,
    "dom": 0,
    "lunes": 1,
    "lun": 1,
    "martes": 2,
    "mar": 2,
    "miércoles": 3,
    "miercoles": 3,
    "mié": 3,
    "mie": 3,
    "jueves": 4,
    "jue": 4,
    "viernes": 5,
    "vie": 5,
    "sábado": 6,
    "sabado": 6,
    "sáb": 6,
    "sab": 6,
}

MONTH_DICTIONARY: dict[str, int] = {
    "enero": 1,
    "ene": 1,
    "ene.": 1,
    "febrero": 2,
    "feb": 2,
    "feb.": 2,
    "marzo": 3,
    "mar": 3,
    "mar.": 3,
    "abril": 4,
    "abr": 4,
    "abr.": 4,
    "mayo": 5,
    "may": 5,
    "may.": 5,
    "junio": 6,
    "jun": 6,
    "jun.": 6,
    "julio": 7,
    "jul": 7,
    "jul.": 7,
    "agosto": 8,
    "ago": 8,
    "ago.": 8,
    "septiembre": 9,
    "setiembre": 9,
    "sep": 9,
    "sep.": 9,
    "octubre": 10,
    "oct": 10,
    "oct.": 10,
    "noviembre": 11,
    "nov": 11,
    "nov.": 11,
    "diciembre": 12,
    "dic": 12,
    "dic.": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "sec": Timeunit.SECOND,
    "segundo": Timeunit.SECOND,
    "segundos": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "mins": Timeunit.MINUTE,
    "minuto": Timeunit.MINUTE,
    "minutos": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "hr": Timeunit.HOUR,
    "hrs": Timeunit.HOUR,
    "hora": Timeunit.HOUR,
    "horas": Timeunit.HOUR,
    "día": Timeunit.DAY,
    "días": Timeunit.DAY,
    "semana": Timeunit.WEEK,
    "semanas": Timeunit.WEEK,
    "mes": Timeunit.MONTH,
    "meses": Timeunit.MONTH,
    "cuarto": Timeunit.QUARTER,
    "cuartos": Timeunit.QUARTER,
    "año": Timeunit.YEAR,
    "años": Timeunit.YEAR,
}

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|un?|uno?|una?|algunos?|unos?|demi-?)"
)


def parse_number_pattern(match_str: str) -> float:
    num = match_str.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num])
    elif num in ("un", "una", "uno"):
        return 1.0
    elif re.search(r"algunos?", num):
        return 3.0
    elif re.search(r"unos?", num):
        return 3.0
    elif re.search(r"media?", num):
        return 0.5
    return float(num)


YEAR_PATTERN = r"[0-9]{1,4}(?![^\s]\d)(?:\s*[a|d]\.?\s*c\.?|\s*a\.?\s*d\.)?"


def parse_year(match_str: str) -> int:
    if re.match(r"^[0-9]{1,4}$", match_str):
        year_number = int(match_str)
        if year_number < 100:
            if year_number > 50:
                year_number += 1900
            else:
                year_number += 2000
        return year_number

    if re.search(r"a\.?\s*c\.?", match_str, re.IGNORECASE):
        cleaned = re.sub(r"a\.?\s*c\.?", "", match_str, flags=re.IGNORECASE)
        return -int(cleaned.strip())

    cleaned = re.sub(r"[^\d]+", "", match_str)
    return int(cleaned)


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNITS_PATTERN = patterns.repeat(SINGLE_TIME_UNIT_PATTERN)


def parse_duration(timeunit_text: str) -> dict[Timeunit, int] | None:
    fragments: dict[Timeunit, float] = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
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
