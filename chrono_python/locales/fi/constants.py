import re
from chrono_python.types import Timeunit
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.common.durations import normalize_duration


WEEKDAY_DICTIONARY: dict[str, int] = {
    "sunnuntai": 0,
    "sunnuntaina": 0,
    "su": 0,
    "maanantai": 1,
    "maanantaina": 1,
    "ma": 1,
    "tiistai": 2,
    "tiistaina": 2,
    "ti": 2,
    "keskiviikko": 3,
    "keskiviikkona": 3,
    "ke": 3,
    "torstai": 4,
    "torstaina": 4,
    "to": 4,
    "perjantai": 5,
    "perjantaina": 5,
    "pe": 5,
    "lauantai": 6,
    "lauantaina": 6,
    "la": 6,
}

MONTH_DICTIONARY: dict[str, int] = {
    "tammikuu": 1,
    "tammikuuta": 1,
    "tammikuun": 1,
    "tammi": 1,
    "helmikuu": 2,
    "helmikuuta": 2,
    "helmikuun": 2,
    "helmi": 2,
    "maaliskuu": 3,
    "maaliskuuta": 3,
    "maaliskuun": 3,
    "maalis": 3,
    "huhtikuu": 4,
    "huhtikuuta": 4,
    "huhtikuun": 4,
    "huhti": 4,
    "toukokuu": 5,
    "toukokuuta": 5,
    "toukokuun": 5,
    "touko": 5,
    "kesäkuu": 6,
    "kesäkuuta": 6,
    "kesäkuun": 6,
    "kesä": 6,
    "heinäkuu": 7,
    "heinäkuuta": 7,
    "heinäkuun": 7,
    "heinä": 7,
    "elokuu": 8,
    "elokuuta": 8,
    "elokuun": 8,
    "elo": 8,
    "syyskuu": 9,
    "syyskuuta": 9,
    "syyskuun": 9,
    "syys": 9,
    "lokakuu": 10,
    "lokakuuta": 10,
    "lokakuun": 10,
    "loka": 10,
    "marraskuu": 11,
    "marraskuuta": 11,
    "marraskuun": 11,
    "marras": 11,
    "joulukuu": 12,
    "joulukuuta": 12,
    "joulukuun": 12,
    "joulu": 12,
}

INTEGER_WORD_DICTIONARY: dict[str, int] = {
    "yksi": 1,
    "yhden": 1,
    "kaksi": 2,
    "kahden": 2,
    "kolme": 3,
    "kolmen": 3,
    "neljä": 4,
    "neljän": 4,
    "viisi": 5,
    "viiden": 5,
    "kuusi": 6,
    "kuuden": 6,
    "seitsemän": 7,
    "kahdeksan": 8,
    "yhdeksän": 9,
    "kymmenen": 10,
}

TIME_UNIT_DICTIONARY: dict[str, Timeunit] = {
    "s": Timeunit.SECOND,
    "sek": Timeunit.SECOND,
    "sekunti": Timeunit.SECOND,
    "sekuntia": Timeunit.SECOND,
    "sekunnin": Timeunit.SECOND,
    "min": Timeunit.MINUTE,
    "minuutti": Timeunit.MINUTE,
    "minuuttia": Timeunit.MINUTE,
    "minuutin": Timeunit.MINUTE,
    "t": Timeunit.HOUR,
    "tunti": Timeunit.HOUR,
    "tuntia": Timeunit.HOUR,
    "tunnin": Timeunit.HOUR,
    "pv": Timeunit.DAY,
    "päivä": Timeunit.DAY,
    "päivää": Timeunit.DAY,
    "päivän": Timeunit.DAY,
    "vk": Timeunit.WEEK,
    "viikko": Timeunit.WEEK,
    "viikkoa": Timeunit.WEEK,
    "viikon": Timeunit.WEEK,
    "kk": Timeunit.MONTH,
    "kuukausi": Timeunit.MONTH,
    "kuukautta": Timeunit.MONTH,
    "kuukauden": Timeunit.MONTH,
    "vuosi": Timeunit.YEAR,
    "vuotta": Timeunit.YEAR,
    "vuoden": Timeunit.YEAR,
}

TIME_UNIT_NO_ABBR_DICTIONARY: dict[str, Timeunit] = {
    "sekunti": Timeunit.SECOND,
    "sekuntia": Timeunit.SECOND,
    "sekunnin": Timeunit.SECOND,
    "minuutti": Timeunit.MINUTE,
    "minuuttia": Timeunit.MINUTE,
    "minuutin": Timeunit.MINUTE,
    "tunti": Timeunit.HOUR,
    "tuntia": Timeunit.HOUR,
    "tunnin": Timeunit.HOUR,
    "päivä": Timeunit.DAY,
    "päivää": Timeunit.DAY,
    "päivän": Timeunit.DAY,
    "viikko": Timeunit.WEEK,
    "viikkoa": Timeunit.WEEK,
    "viikon": Timeunit.WEEK,
    "kuukausi": Timeunit.MONTH,
    "kuukautta": Timeunit.MONTH,
    "kuukauden": Timeunit.MONTH,
    "vuosi": Timeunit.YEAR,
    "vuotta": Timeunit.YEAR,
    "vuoden": Timeunit.YEAR,
}

NUMBER_PATTERN = f"(?:{patterns.match_any(INTEGER_WORD_DICTIONARY)}|\\d+)"
TIME_UNIT_PATTERN = f"(?:{patterns.match_any(TIME_UNIT_DICTIONARY)})"

SINGLE_TIME_UNIT_PATTERN = (
    f"({NUMBER_PATTERN})\\s{{0,5}}({patterns.match_any(TIME_UNIT_DICTIONARY)})\\s{{0,5}}"
)
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
        unit_str = match.group(2).lower()
        unit = TIME_UNIT_DICTIONARY[unit_str]
        fragments[unit] = fragments.get(unit, 0.0) + num
        remaining_text = remaining_text[match.end():]
        match = SINGLE_TIME_UNIT_REGEX.search(remaining_text)

    if not fragments:
        return None

    return normalize_duration(fragments)
