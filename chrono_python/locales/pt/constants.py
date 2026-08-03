import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "domingo": 0,
    "dom": 0,
    "dom.": 0,
    "segunda": 1,
    "segunda-feira": 1,
    "seg": 1,
    "seg.": 1,
    "terça": 2,
    "terca": 2,
    "terça-feira": 2,
    "terca-feira": 2,
    "ter": 2,
    "ter.": 2,
    "quarta": 3,
    "quarta-feira": 3,
    "qua": 3,
    "qua.": 3,
    "quinta": 4,
    "quinta-feira": 4,
    "qui": 4,
    "qui.": 4,
    "sexta": 5,
    "sexta-feira": 5,
    "sex": 5,
    "sex.": 5,
    "sábado": 6,
    "sabado": 6,
    "sab": 6,
    "sab.": 6,
    "sáb": 6,
    "sáb.": 6,
}


MONTH_DICTIONARY: dict[str, int] = {
    "janeiro": 1,
    "jan": 1,
    "jan.": 1,
    "fevereiro": 2,
    "fev": 2,
    "fev.": 2,
    "março": 3,
    "marco": 3,
    "mar": 3,
    "mar.": 3,
    "abril": 4,
    "abr": 4,
    "abr.": 4,
    "maio": 5,
    "mai": 5,
    "mai.": 5,
    "junho": 6,
    "jun": 6,
    "jun.": 6,
    "julho": 7,
    "jul": 7,
    "jul.": 7,
    "agosto": 8,
    "ago": 8,
    "ago.": 8,
    "setembro": 9,
    "set": 9,
    "set.": 9,
    "outubro": 10,
    "out": 10,
    "out.": 10,
    "novembro": 11,
    "nov": 11,
    "nov.": 11,
    "dezembro": 12,
    "dez": 12,
    "dez.": 12,
}


INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "um": 1,
    "uma": 1,
    "dois": 2,
    "duas": 2,
    "três": 3,
    "tres": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
    "onze": 11,
    "doze": 12,
}


TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "sec": Timeunit.SECOND,
    "seg": Timeunit.SECOND,
    "seg.": Timeunit.SECOND,
    "segundo": Timeunit.SECOND,
    "segundos": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "min.": Timeunit.MINUTE,
    "mins": Timeunit.MINUTE,
    "minuto": Timeunit.MINUTE,
    "minutos": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "hr": Timeunit.HOUR,
    "hrs": Timeunit.HOUR,
    "hora": Timeunit.HOUR,
    "horas": Timeunit.HOUR,
    "dia": Timeunit.DAY,
    "dias": Timeunit.DAY,
    "semana": Timeunit.WEEK,
    "semanas": Timeunit.WEEK,
    "mês": Timeunit.MONTH,
    "mes": Timeunit.MONTH,
    "meses": Timeunit.MONTH,
    "ano": Timeunit.YEAR,
    "anos": Timeunit.YEAR,
}


YEAR_PATTERN = (
    r"[0-9]{1,4}(?![^\s]\d)(?:\s*[a|d]\.?\s*c\.?|\s*a\.?\s*d\.)?"
)


def parse_year(match_str: str) -> int:
    match_str = match_str.strip()
    if re.match(r"^[0-9]{1,4}$", match_str):
        year_number = int(match_str)
        if year_number < 100:
            if year_number > 50:
                year_number += 1900
            else:
                year_number += 2000
        return year_number

    if re.search(r"a\.?\s*c\.?", match_str, re.IGNORECASE):
        cleaned = re.sub(r"a\.?\s*c\.?", "", match_str, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"[^\d]+", "", cleaned)
        return -int(cleaned)

    cleaned = re.sub(r"[^\d]+", "", match_str)
    return int(cleaned)


NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|uma?\\b|alguns?|algumas?|meio|meia)"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    elif num_str in ("um", "uma"):
        return 1.0
    elif re.match(r"alguns?|algumas?", num_str):
        return 3.0
    elif re.match(r"meio|meia", num_str):
        return 0.5
    return float(num_str)


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNIT_CONNECTOR_PATTERN = r"\s{0,5},?(?:\s*e)?\s{0,5}"

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
