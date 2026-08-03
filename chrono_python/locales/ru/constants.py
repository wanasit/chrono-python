import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "воскресенье": 0,
    "воскресенья": 0,
    "вск": 0,
    "вск.": 0,
    "понедельник": 1,
    "понедельника": 1,
    "пн": 1,
    "пн.": 1,
    "вторник": 2,
    "вторника": 2,
    "вт": 2,
    "вт.": 2,
    "среда": 3,
    "среды": 3,
    "среду": 3,
    "ср": 3,
    "ср.": 3,
    "четверг": 4,
    "четверга": 4,
    "чт": 4,
    "чт.": 4,
    "пятница": 5,
    "пятницу": 5,
    "пятницы": 5,
    "пт": 5,
    "пт.": 5,
    "суббота": 6,
    "субботу": 6,
    "субботы": 6,
    "сб": 6,
    "сб.": 6,
}


FULL_MONTH_NAME_DICTIONARY: dict[str, int] = {
    "январь": 1,
    "января": 1,
    "январе": 1,
    "февраль": 2,
    "февраля": 2,
    "феврале": 2,
    "март": 3,
    "марта": 3,
    "марте": 3,
    "апрель": 4,
    "апреля": 4,
    "апреле": 4,
    "май": 5,
    "мая": 5,
    "мае": 5,
    "июнь": 6,
    "июня": 6,
    "июне": 6,
    "июль": 7,
    "июля": 7,
    "июле": 7,
    "август": 8,
    "августа": 8,
    "августе": 8,
    "сентябрь": 9,
    "сентября": 9,
    "сентябре": 9,
    "октябрь": 10,
    "октября": 10,
    "октябре": 10,
    "ноябрь": 11,
    "ноября": 11,
    "ноябре": 11,
    "декабрь": 12,
    "декабря": 12,
    "декабре": 12,
}


MONTH_DICTIONARY: dict[str, int] = {
    **FULL_MONTH_NAME_DICTIONARY,
    "янв": 1,
    "янв.": 1,
    "фев": 2,
    "фев.": 2,
    "мар": 3,
    "мар.": 3,
    "апр": 4,
    "апр.": 4,
    "авг": 8,
    "авг.": 8,
    "сен": 9,
    "сен.": 9,
    "окт": 10,
    "окт.": 10,
    "ноя": 11,
    "ноя.": 11,
    "дек": 12,
    "дек.": 12,
}


INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "один": 1,
    "одна": 1,
    "одной": 1,
    "одну": 1,
    "две": 2,
    "два": 2,
    "двух": 2,
    "три": 3,
    "трех": 3,
    "трёх": 3,
    "четыре": 4,
    "четырех": 4,
    "четырёх": 4,
    "пять": 5,
    "пяти": 5,
    "шесть": 6,
    "шести": 6,
    "семь": 7,
    "семи": 7,
    "восемь": 8,
    "восьми": 8,
    "девять": 9,
    "девяти": 9,
    "десять": 10,
    "десяти": 10,
    "одиннадцать": 11,
    "одиннадцати": 11,
    "двенадцать": 12,
    "двенадцати": 12,
}


ORDINAL_WORD_DICTIONARY: dict[str, int] = {
    "первое": 1,
    "первого": 1,
    "второе": 2,
    "второго": 2,
    "третье": 3,
    "третьего": 3,
    "четвертое": 4,
    "четвертого": 4,
    "пятое": 5,
    "пятого": 5,
    "шестое": 6,
    "шестого": 6,
    "седьмое": 7,
    "седьмого": 7,
    "восьмое": 8,
    "восьмого": 8,
    "девятое": 9,
    "девятого": 9,
    "десятое": 10,
    "десятого": 10,
    "одиннадцатое": 11,
    "одиннадцатого": 11,
    "двенадцатое": 12,
    "двенадцатого": 12,
    "тринадцатое": 13,
    "тринадцатого": 13,
    "четырнадцатое": 14,
    "четырнадцатого": 14,
    "пятнадцатое": 15,
    "пятнадцатого": 15,
    "шестнадцатое": 16,
    "шестнадцатого": 16,
    "семнадцатое": 17,
    "семнадцатого": 17,
    "восемнадцатое": 18,
    "восемнадцатого": 18,
    "девятнадцатое": 19,
    "девятнадцатого": 19,
    "двадцатое": 20,
    "двадцатого": 20,
    "двадцать первое": 21,
    "двадцать первого": 21,
    "двадцать второе": 22,
    "двадцать второго": 22,
    "двадцать третье": 23,
    "двадцать третьего": 23,
    "двадцать четвертое": 24,
    "двадцать четвертого": 24,
    "двадцать пятое": 25,
    "двадцать пятого": 25,
    "двадцать шестое": 26,
    "двадцать шестого": 26,
    "двадцать седьмое": 27,
    "двадцать седьмого": 27,
    "двадцать восьмое": 28,
    "двадцать восьмого": 28,
    "двадцать девятое": 29,
    "двадцать девятого": 29,
    "тридцатое": 30,
    "тридцатого": 30,
    "тридцать первое": 31,
    "тридцать первого": 31,
}


TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "сек": Timeunit.SECOND,
    "секунда": Timeunit.SECOND,
    "секунд": Timeunit.SECOND,
    "секунды": Timeunit.SECOND,
    "секунду": Timeunit.SECOND,
    "секундочка": Timeunit.SECOND,
    "секундочки": Timeunit.SECOND,
    "секундочек": Timeunit.SECOND,
    "секундочку": Timeunit.SECOND,
    "мин": Timeunit.MINUTE,
    "минута": Timeunit.MINUTE,
    "минут": Timeunit.MINUTE,
    "минуты": Timeunit.MINUTE,
    "минуту": Timeunit.MINUTE,
    "минуток": Timeunit.MINUTE,
    "минутки": Timeunit.MINUTE,
    "минутку": Timeunit.MINUTE,
    "минуточек": Timeunit.MINUTE,
    "минуточки": Timeunit.MINUTE,
    "минуточку": Timeunit.MINUTE,
    "час": Timeunit.HOUR,
    "часов": Timeunit.HOUR,
    "часа": Timeunit.HOUR,
    "часу": Timeunit.HOUR,
    "часиков": Timeunit.HOUR,
    "часика": Timeunit.HOUR,
    "часике": Timeunit.HOUR,
    "часик": Timeunit.HOUR,
    "день": Timeunit.DAY,
    "дня": Timeunit.DAY,
    "дней": Timeunit.DAY,
    "суток": Timeunit.DAY,
    "сутки": Timeunit.DAY,
    "неделя": Timeunit.WEEK,
    "неделе": Timeunit.WEEK,
    "недели": Timeunit.WEEK,
    "неделю": Timeunit.WEEK,
    "недель": Timeunit.WEEK,
    "недельке": Timeunit.WEEK,
    "недельки": Timeunit.WEEK,
    "неделек": Timeunit.WEEK,
    "месяц": Timeunit.MONTH,
    "месяце": Timeunit.MONTH,
    "месяцев": Timeunit.MONTH,
    "месяца": Timeunit.MONTH,
    "квартал": Timeunit.QUARTER,
    "квартале": Timeunit.QUARTER,
    "кварталов": Timeunit.QUARTER,
    "год": Timeunit.YEAR,
    "года": Timeunit.YEAR,
    "году": Timeunit.YEAR,
    "годов": Timeunit.YEAR,
    "лет": Timeunit.YEAR,
    "годик": Timeunit.YEAR,
    "годика": Timeunit.YEAR,
    "годиков": Timeunit.YEAR,
}


NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|пол|несколько|пар(?:ы|у)|\\s{{0,3}})"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    if "несколько" in num_str:
        return 3.0
    elif "пол" in num_str:
        return 0.5
    elif "пар" in num_str:
        return 2.0
    elif num_str == "":
        return 1.0
    return float(num_str)


ORDINAL_NUMBER_PATTERN = (
    f"(?:{patterns.match_any(ORDINAL_WORD_DICTIONARY)}|[0-9]{{1,2}}(?:го|ого|е|ое)?)"
)


def parse_ordinal_number_pattern(match_str: str) -> int:
    num_str = match_str.lower()
    if num_str in ORDINAL_WORD_DICTIONARY:
        return ORDINAL_WORD_DICTIONARY[num_str]
    num_str = re.sub(r"(?:го|ого|е|ое)$", "", num_str, flags=re.IGNORECASE)
    return int(num_str)


YEAR_PATTERN = (
    r"(?:[1-9][0-9]{0,3}(?:\s+(?:году|года|год|г|г\.))?\s*(?:н\.э\.|до н\.э\.|н\. э\.|до н\. э\.)"
    r"|[1-2][0-9]{3}(?:\s+(?:году|года|год|г|г\.))?|[5-9][0-9](?:\s+(?:году|года|год|г|г\.))?)"
)


def parse_year(match_str: str) -> int:
    cleaned = match_str
    if re.search(r"(?:года|годе|году|годом|годов|год|г\.|г\b)", cleaned, re.IGNORECASE):
        cleaned = re.sub(r"(?:года|годе|году|годом|годов|год|г\.|г\b)", "", cleaned, flags=re.IGNORECASE).strip()

    if re.search(r"(до н\.э\.|до н\. э\.)", cleaned, re.IGNORECASE):
        cleaned = re.sub(r"(до н\.э\.|до н\. э\.)", "", cleaned, flags=re.IGNORECASE).strip()
        return -int(cleaned)

    if re.search(r"(н\. э\.|н\.э\.)", cleaned, re.IGNORECASE):
        cleaned = re.sub(r"(н\. э\.|н\.э\.)", "", cleaned, flags=re.IGNORECASE).strip()
        return int(cleaned)

    raw_year_number = int(cleaned)
    return calendars.find_most_likely_ad_year(raw_year_number)


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY)})"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r"(?:(?:около|примерно)\s{0,3})?",
    pattern_connector=r"\s{0,5},?\s{0,5}"
)


def parse_duration(timeunit_text: str) -> dict[Timeunit, float] | None:
    fragments: dict[Timeunit, float] = {}
    remaining_text = timeunit_text
    match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)
    while match:
        num = parse_number_pattern(match.group(1))
        unit_str = match.group(2).lower()
        unit = TIME_UNIT_DICTIONARY[unit_str]
        fragments[unit] = fragments.get(unit, 0.0) + num

        remaining_text = remaining_text[match.end():].strip()
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)

    if not fragments:
        return None

    return normalize_duration(fragments)
