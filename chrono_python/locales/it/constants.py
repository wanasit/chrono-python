import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "domenica": 0,
    "dom": 0,
    "dom.": 0,
    "lunedì": 1,
    "lunedi": 1,
    "lun": 1,
    "lun.": 1,
    "martedì": 2,
    "martedi": 2,
    "mar": 2,
    "mar.": 2,
    "mercoledì": 3,
    "mercoledi": 3,
    "mer": 3,
    "mer.": 3,
    "giovedì": 4,
    "giovedi": 4,
    "gio": 4,
    "gio.": 4,
    "venerdì": 5,
    "venerdi": 5,
    "ven": 5,
    "ven.": 5,
    "sabato": 6,
    "sab": 6,
    "sab.": 6,
}

FULL_MONTH_NAME_DICTIONARY: dict[str, int] = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}

MONTH_DICTIONARY: dict[str, int] = {
    **FULL_MONTH_NAME_DICTIONARY,
    "gen": 1,
    "gen.": 1,
    "feb": 2,
    "feb.": 2,
    "mar": 3,
    "mar.": 3,
    "apr": 4,
    "apr.": 4,
    "mag": 5,
    "mag.": 5,
    "giu": 6,
    "giu.": 6,
    "lug": 7,
    "lug.": 7,
    "ago": 8,
    "ago.": 8,
    "set": 9,
    "set.": 9,
    "sett": 9,
    "sett.": 9,
    "ott": 10,
    "ott.": 10,
    "nov": 11,
    "nov.": 11,
    "dic": 12,
    "dic.": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "uno": 1,
    "una": 1,
    "un": 1,
    "due": 2,
    "tre": 3,
    "quattro": 4,
    "cinque": 5,
    "sei": 6,
    "sette": 7,
    "otto": 8,
    "nove": 9,
    "dieci": 10,
    "undici": 11,
    "dodici": 12,
}

ORDINAL_WORD_DICTIONARY: dict[str, int] = {
    "primo": 1,
    "prima": 1,
    "1°": 1,
    "1ª": 1,
    "secondo": 2,
    "seconda": 2,
    "2°": 2,
    "2ª": 2,
    "terzo": 3,
    "terza": 3,
    "3°": 3,
    "3ª": 3,
    "quarto": 4,
    "quarta": 4,
    "4°": 4,
    "4ª": 4,
    "quinto": 5,
    "quinta": 5,
    "5°": 5,
    "5ª": 5,
    "sesto": 6,
    "sesta": 6,
    "6°": 6,
    "6ª": 6,
    "settimo": 7,
    "settima": 7,
    "7°": 7,
    "7ª": 7,
    "ottavo": 8,
    "ottava": 8,
    "8°": 8,
    "8ª": 8,
    "nono": 9,
    "nona": 9,
    "9°": 9,
    "9ª": 9,
    "decimo": 10,
    "decima": 10,
    "10°": 10,
    "10ª": 10,
    "undicesimo": 11,
    "undicesima": 11,
    "11°": 11,
    "11ª": 11,
    "dodicesimo": 12,
    "dodicesima": 12,
    "12°": 12,
    "12ª": 12,
    "tredicesimo": 13,
    "tredicesima": 13,
    "13°": 13,
    "13ª": 13,
    "quattordicesimo": 14,
    "quattordicesima": 14,
    "14°": 14,
    "14ª": 14,
    "quindicesimo": 15,
    "quindicesima": 15,
    "15°": 15,
    "15ª": 15,
    "sedicesimo": 16,
    "sedicesima": 16,
    "16°": 16,
    "16ª": 16,
    "diciassettesimo": 17,
    "diciassettesima": 17,
    "17°": 17,
    "17ª": 17,
    "diciottesimo": 18,
    "diciottesima": 18,
    "18°": 18,
    "18ª": 18,
    "diciannovesimo": 19,
    "diciannovesima": 19,
    "19°": 19,
    "19ª": 19,
    "ventesimo": 20,
    "ventesima": 20,
    "20°": 20,
    "20ª": 20,
    "ventunesimo": 21,
    "ventunesima": 21,
    "21°": 21,
    "21ª": 21,
    "ventiduesimo": 22,
    "ventiduesima": 22,
    "22°": 22,
    "22ª": 22,
    "ventitreesimo": 23,
    "ventitreesima": 23,
    "23°": 23,
    "23ª": 23,
    "ventiquattresimo": 24,
    "ventiquattresima": 24,
    "24°": 24,
    "24ª": 24,
    "venticinquesimo": 25,
    "venticinquesima": 25,
    "25°": 25,
    "25ª": 25,
    "ventiseiesimo": 26,
    "ventiseiesima": 26,
    "26°": 26,
    "26ª": 26,
    "ventisettesimo": 27,
    "ventisettesima": 27,
    "27°": 27,
    "27ª": 27,
    "ventottesimo": 28,
    "ventottesima": 28,
    "28°": 28,
    "28ª": 28,
    "ventinovesimo": 29,
    "ventinovesima": 29,
    "29°": 29,
    "29ª": 29,
    "trentesimo": 30,
    "trentesima": 30,
    "30°": 30,
    "30ª": 30,
    "trentunesimo": 31,
    "trentunesima": 31,
    "31°": 31,
    "31ª": 31,
}

TIME_UNIT_DICTIONARY_NO_ABBR: dict[str, Timeunit] = {
    "secondo": Timeunit.SECOND,
    "secondi": Timeunit.SECOND,
    "minuto": Timeunit.MINUTE,
    "minuti": Timeunit.MINUTE,
    "ora": Timeunit.HOUR,
    "ore": Timeunit.HOUR,
    "giorno": Timeunit.DAY,
    "giorni": Timeunit.DAY,
    "settimana": Timeunit.WEEK,
    "settimane": Timeunit.WEEK,
    "mese": Timeunit.MONTH,
    "mesi": Timeunit.MONTH,
    "trimestre": Timeunit.QUARTER,
    "trimestri": Timeunit.QUARTER,
    "anno": Timeunit.YEAR,
    "anni": Timeunit.YEAR,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "s": Timeunit.SECOND,
    "sec": Timeunit.SECOND,
    "m": Timeunit.MINUTE,
    "min": Timeunit.MINUTE,
    "h": Timeunit.HOUR,
    "g": Timeunit.DAY,
    "gg": Timeunit.DAY,
    "sett": Timeunit.WEEK,
    "trim": Timeunit.QUARTER,
    **TIME_UNIT_DICTIONARY_NO_ABBR,
}

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|mezz[oa]?(?:\\s{{0,2}})?|un(?:'|\\s{{0,2}})?|qualche|alcuni|paio\\s{{0,2}}(?:di)?)"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    elif num_str in ("un", "un'", "una", "uno"):
        return 1.0
    elif "qualche" in num_str:
        return 3.0
    elif "mezz" in num_str:
        return 0.5
    elif "paio" in num_str:
        return 2.0
    elif "alcuni" in num_str:
        return 7.0
    return float(num_str)


ORDINAL_NUMBER_PATTERN = f"(?:{patterns.match_any(ORDINAL_WORD_DICTIONARY)}|[0-9]{{1,2}}(?:°|ª|º)?)"


def parse_ordinal_number_pattern(match_str: str) -> int:
    num_str = match_str.lower()
    if num_str in ORDINAL_WORD_DICTIONARY:
        return ORDINAL_WORD_DICTIONARY[num_str]
    num_str = re.sub(r"(?:°|ª|º)$", "", num_str, flags=re.IGNORECASE)
    return int(num_str)


YEAR_PATTERN = r"(?:[1-9][0-9]{0,3}\s*(?:BE|AD|BC|BCE|CE)|[1-2][0-9]{3}|[0-9]{2})"


def parse_year(match_str: str) -> int:
    if re.search(r"BE", match_str, re.IGNORECASE):
        cleaned = re.sub(r"BE", "", match_str, flags=re.IGNORECASE)
        return int(cleaned) - 543
    if re.search(r"BCE?", match_str, re.IGNORECASE):
        cleaned = re.sub(r"BCE?", "", match_str, flags=re.IGNORECASE)
        return -int(cleaned)
    if re.search(r"AD|CE", match_str, re.IGNORECASE):
        cleaned = re.sub(r"AD|CE", "", match_str, flags=re.IGNORECASE)
        return int(cleaned)
    raw_year = int(match_str)
    return calendars.find_most_likely_ad_year(raw_year)


SINGLE_TIME_UNIT_PATTERN = f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY)})"
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

SINGLE_TIME_UNIT_NO_ABBR_PATTERN = f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY_NO_ABBR)})"

TIME_UNIT_CONNECTOR_PATTERN = r"\s{0,5},?(?:\s*e)?\s{0,5}"

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r"(?:(?:circa|approssimativamente)\s{0,3})?",
    pattern_connector=TIME_UNIT_CONNECTOR_PATTERN,
)

TIME_UNITS_NO_ABBR_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_NO_ABBR_PATTERN,
    prefix=r"(?:(?:circa|approssimativamente)\s{0,3})?",
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
