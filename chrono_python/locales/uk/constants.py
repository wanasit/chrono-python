import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "неділя": 0,
    "неділі": 0,
    "неділю": 0,
    "нд": 0,
    "нд.": 0,
    "понеділок": 1,
    "понеділка": 1,
    "пн": 1,
    "пн.": 1,
    "вівторок": 2,
    "вівторка": 2,
    "вт": 2,
    "вт.": 2,
    "середа": 3,
    "середи": 3,
    "середу": 3,
    "ср": 3,
    "ср.": 3,
    "четвер": 4,
    "четверга": 4,
    "четвергу": 4,
    "чт": 4,
    "чт.": 4,
    "п'ятниця": 5,
    "п'ятниці": 5,
    "п'ятницю": 5,
    "пт": 5,
    "пт.": 5,
    "субота": 6,
    "суботи": 6,
    "суботу": 6,
    "сб": 6,
    "сб.": 6,
}

FULL_MONTH_NAME_DICTIONARY: dict[str, int] = {
    "січень": 1,
    "січня": 1,
    "січні": 1,
    "лютий": 2,
    "лютого": 2,
    "лютому": 2,
    "березень": 3,
    "березня": 3,
    "березні": 3,
    "квітень": 4,
    "квітня": 4,
    "квітні": 4,
    "травень": 5,
    "травня": 5,
    "травні": 5,
    "червень": 6,
    "червня": 6,
    "червні": 6,
    "липень": 7,
    "липня": 7,
    "липні": 7,
    "серпень": 8,
    "серпня": 8,
    "серпні": 8,
    "вересень": 9,
    "вересня": 9,
    "вересні": 9,
    "жовтень": 10,
    "жовтня": 10,
    "жовтні": 10,
    "листопад": 11,
    "листопада": 11,
    "листопаду": 11,
    "грудень": 12,
    "грудня": 12,
    "грудні": 12,
}

MONTH_DICTIONARY: dict[str, int] = {
    **FULL_MONTH_NAME_DICTIONARY,
    "січ": 1,
    "січ.": 1,
    "лют": 2,
    "лют.": 2,
    "бер": 3,
    "бер.": 3,
    "квіт": 4,
    "квіт.": 4,
    "трав": 5,
    "трав.": 5,
    "черв": 6,
    "черв.": 6,
    "лип": 7,
    "лип.": 7,
    "серп": 8,
    "серп.": 8,
    "сер": 8,
    "cер.": 8,
    "вер": 9,
    "вер.": 9,
    "верес": 9,
    "верес.": 9,
    "жовт": 10,
    "жовт.": 10,
    "листоп": 11,
    "листоп.": 11,
    "груд": 12,
    "груд.": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "один": 1,
    "одна": 1,
    "одної": 1,
    "одну": 1,
    "дві": 2,
    "два": 2,
    "двох": 2,
    "три": 3,
    "трьох": 3,
    "чотири": 4,
    "чотирьох": 4,
    "п'ять": 5,
    "п'яти": 5,
    "шість": 6,
    "шести": 6,
    "сім": 7,
    "семи": 7,
    "вісім": 8,
    "восьми": 8,
    "дев'ять": 9,
    "дев'яти": 9,
    "десять": 10,
    "десяти": 10,
    "одинадцять": 11,
    "одинадцяти": 11,
    "дванадцять": 12,
    "дванадцяти": 12,
}

ORDINAL_WORD_DICTIONARY: dict[str, int] = {
    "перше": 1,
    "першого": 1,
    "друге": 2,
    "другого": 2,
    "третє": 3,
    "третього": 3,
    "четверте": 4,
    "четвертого": 4,
    "п'яте": 5,
    "п'ятого": 5,
    "шосте": 6,
    "шостого": 6,
    "сьоме": 7,
    "сьомого": 7,
    "восьме": 8,
    "восьмого": 8,
    "дев'яте": 9,
    "дев'ятого": 9,
    "десяте": 10,
    "десятого": 10,
    "одинадцяте": 11,
    "одинадцятого": 11,
    "дванадцяте": 12,
    "дванадцятого": 12,
    "тринадцяте": 13,
    "тринадцятого": 13,
    "чотирнадцяте": 14,
    "чотинрнадцятого": 14,
    "п'ятнадцяте": 15,
    "п'ятнадцятого": 15,
    "шістнадцяте": 16,
    "шістнадцятого": 16,
    "сімнадцяте": 17,
    "сімнадцятого": 17,
    "вісімнадцяте": 18,
    "вісімнадцятого": 18,
    "дев'ятнадцяте": 19,
    "дев'ятнадцятого": 19,
    "двадцяте": 20,
    "двадцятого": 20,
    "двадцять перше": 21,
    "двадцять першого": 21,
    "двадцять друге": 22,
    "двадцять другого": 22,
    "двадцять третє": 23,
    "двадцять третього": 23,
    "двадцять четверте": 24,
    "двадцять четвертого": 24,
    "двадцять п'яте": 25,
    "двадцять п'ятого": 25,
    "двадцять шосте": 26,
    "двадцять шостого": 26,
    "двадцять сьоме": 27,
    "двадцять сьомого": 27,
    "двадцять восьме": 28,
    "двадцять восьмого": 28,
    "двадцять дев'яте": 29,
    "двадцять дев'ятого": 29,
    "тридцяте": 30,
    "тридцятого": 30,
    "тридцять перше": 31,
    "тридцять першого": 31,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "сек": Timeunit.SECOND,
    "секунда": Timeunit.SECOND,
    "секунд": Timeunit.SECOND,
    "секунди": Timeunit.SECOND,
    "секунду": Timeunit.SECOND,
    "секундочок": Timeunit.SECOND,
    "секундочки": Timeunit.SECOND,
    "секундочку": Timeunit.SECOND,
    "хв": Timeunit.MINUTE,
    "хвилина": Timeunit.MINUTE,
    "хвилин": Timeunit.MINUTE,
    "хвилини": Timeunit.MINUTE,
    "хвилину": Timeunit.MINUTE,
    "хвилинок": Timeunit.MINUTE,
    "хвилинки": Timeunit.MINUTE,
    "хвилинку": Timeunit.MINUTE,
    "хвилиночок": Timeunit.MINUTE,
    "хвилиночки": Timeunit.MINUTE,
    "хвилиночку": Timeunit.MINUTE,
    "год": Timeunit.HOUR,
    "година": Timeunit.HOUR,
    "годин": Timeunit.HOUR,
    "години": Timeunit.HOUR,
    "годину": Timeunit.HOUR,
    "годинка": Timeunit.HOUR,
    "годинок": Timeunit.HOUR,
    "годинки": Timeunit.HOUR,
    "годинку": Timeunit.HOUR,
    "день": Timeunit.DAY,
    "дня": Timeunit.DAY,
    "днів": Timeunit.DAY,
    "дні": Timeunit.DAY,
    "доба": Timeunit.DAY,
    "добу": Timeunit.DAY,
    "тиждень": Timeunit.WEEK,
    "тижню": Timeunit.WEEK,
    "тижня": Timeunit.WEEK,
    "тижні": Timeunit.WEEK,
    "тижнів": Timeunit.WEEK,
    "місяць": Timeunit.MONTH,
    "місяців": Timeunit.MONTH,
    "місяці": Timeunit.MONTH,
    "місяця": Timeunit.MONTH,
    "квартал": Timeunit.QUARTER,
    "кварталу": Timeunit.QUARTER,
    "квартала": Timeunit.QUARTER,
    "кварталів": Timeunit.QUARTER,
    "кварталі": Timeunit.QUARTER,
    "рік": Timeunit.YEAR,
    "року": Timeunit.YEAR,
    "році": Timeunit.YEAR,
    "років": Timeunit.YEAR,
    "роки": Timeunit.YEAR,
}

NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+|пів|декілька|пар(?:у)?|\\s{{0,3}})"
)


def parse_number_pattern(match_str: str) -> float:
    num = match_str.lower()
    if num in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num])
    if "декілька" in num:
        return 2.0
    elif "пів" in num:
        return 0.5
    elif "пар" in num:
        return 2.0
    elif num == "":
        return 1.0
    return float(num)


ORDINAL_NUMBER_PATTERN = f"(?:{patterns.match_any(ORDINAL_WORD_DICTIONARY)}|[0-9]{{1,2}}(?:го|ого|е)?)"


def parse_ordinal_number_pattern(match_str: str) -> int:
    num = match_str.lower()
    if num in ORDINAL_WORD_DICTIONARY:
        return ORDINAL_WORD_DICTIONARY[num]
    num = re.sub(r"(?:го|ого|е)$", "", num, flags=re.IGNORECASE)
    return int(num)


YEAR_SUFFIX = r"(?:\s+(?:року|рік|р|р\.))?"
YEAR_PATTERN = rf"(?:[1-9][0-9]{{0,3}}{YEAR_SUFFIX}\s*(?:н\.е\.|до н\.е\.|н\. е\.|до н\. е\.)|[1-2][0-9]{{3}}{YEAR_SUFFIX}|[5-9][0-9]{YEAR_SUFFIX})"


def parse_year_pattern(match_str: str) -> int:
    if re.search(r"(рік|року|р|р\.)", match_str, re.IGNORECASE):
        match_str = re.sub(r"(рік|року|р|р\.)", "", match_str, flags=re.IGNORECASE)

    if re.search(r"(до н\.е\.|до н\. е\.)", match_str, re.IGNORECASE):
        match_str = re.sub(r"(до н\.е\.|до н\. е\.)", "", match_str, flags=re.IGNORECASE)
        return -int(match_str.strip())

    if re.search(r"(н\. е\.|н\.е\.)", match_str, re.IGNORECASE):
        match_str = re.sub(r"(н\. е\.|н\.е\.)", "", match_str, flags=re.IGNORECASE)
        return int(match_str.strip())

    raw_year = int(match_str.strip())
    return calendars.find_most_likely_ad_year(raw_year)


SINGLE_TIME_UNIT_PATTERN = f"({NUMBER_PATTERN})\\s{{0,3}}({patterns.match_any(TIME_UNIT_DICTIONARY)})"
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNITS_PATTERN = patterns.repeat(
    SINGLE_TIME_UNIT_PATTERN,
    prefix=r"(?:(?:близько|приблизно)\s{0,3})?",
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
        remaining_text = remaining_text[match.end():].strip()
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)

    if not fragments:
        return None

    return normalize_duration(fragments)
