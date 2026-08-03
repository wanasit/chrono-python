import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "chủ nhật": 0,
    "cn": 0,
    "thứ hai": 1,
    "t2": 1,
    "thứ ba": 2,
    "t3": 2,
    "thứ tư": 3,
    "t4": 3,
    "thứ năm": 4,
    "t5": 4,
    "thứ sáu": 5,
    "t6": 5,
    "thứ bảy": 6,
    "t7": 6,
}


MONTH_DICTIONARY: dict[str, int] = {
    "tháng 1": 1,
    "tháng một": 1,
    "tháng giêng": 1,
    "tháng 2": 2,
    "tháng hai": 2,
    "tháng 3": 3,
    "tháng ba": 3,
    "tháng 4": 4,
    "tháng tư": 4,
    "tháng 5": 5,
    "tháng năm": 5,
    "tháng 6": 6,
    "tháng sáu": 6,
    "tháng 7": 7,
    "tháng bảy": 7,
    "tháng 8": 8,
    "tháng tám": 8,
    "tháng 9": 9,
    "tháng chín": 9,
    "tháng 10": 10,
    "tháng mười": 10,
    "tháng 11": 11,
    "tháng mười một": 11,
    "tháng 12": 12,
    "tháng mười hai": 12,
    "tháng chạp": 12,
}


INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "một": 1,
    "hai": 2,
    "ba": 3,
    "bốn": 4,
    "năm": 5,
    "sáu": 6,
    "bảy": 7,
    "tám": 8,
    "chín": 9,
    "mười": 10,
    "mười một": 11,
    "mười hai": 12,
}


TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "giây": Timeunit.SECOND,
    "phút": Timeunit.MINUTE,
    "giờ": Timeunit.HOUR,
    "ngày": Timeunit.DAY,
    "tuần": Timeunit.WEEK,
    "tháng": Timeunit.MONTH,
    "năm": Timeunit.YEAR,
}


NUMBER_PATTERN = (
    f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|[0-9]+|[0-9]+\\.[0-9]+)"
)


def parse_number_pattern(match_str: str) -> float:
    num_str = match_str.lower()
    if num_str in INTEGER_WORD_DICTIONARY:
        return float(INTEGER_WORD_DICTIONARY[num_str])
    return float(num_str)


YEAR_PATTERN = r"(?:[0-9]{1,4}(?:\s*TCN)?)"


def parse_year(match_str: str) -> int:
    upper = match_str.upper()
    cleaned = re.sub(r"[^0-9]+", "", match_str)
    num = int(cleaned)
    if "TCN" in upper:
        return -num
    return calendars.find_most_likely_ad_year(num)


SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
SINGLE_TIME_UNIT_REGEX = re.compile(SINGLE_TIME_UNIT_PATTERN, re.IGNORECASE)

TIME_UNITS_PATTERN = patterns.repeat(SINGLE_TIME_UNIT_PATTERN, prefix="")


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
