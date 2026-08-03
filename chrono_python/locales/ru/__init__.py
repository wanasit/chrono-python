from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.ru.parsers import (
    RUCasualDateParser,
    RUCasualTimeParser,
    RUMonthNameAfterDate,
    RUMonthNameParser,
    RURelativeDateFormatParser,
    RUTimeExprParser,
    RUTimeUnitAgoParser,
    RUTimeUnitCasualRelativeParser,
    RUTimeUnitWithinParser,
    RUWeekdayParser,
)
from chrono_python.locales.ru.refiners import (
    RUMergeDateRangeRefiner,
    RUMergeDateTimeRefiner,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        RUTimeUnitWithinParser(),
        RUMonthNameAfterDate(),
        RUWeekdayParser(),
        RUTimeExprParser(strict_mode=True),
        RUTimeUnitAgoParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        RUMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        RUMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        RUCasualDateParser(),
        RUCasualTimeParser(),
        RUMonthNameParser(),
        RURelativeDateFormatParser(),
        RUTimeUnitCasualRelativeParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        RUTimeUnitWithinParser(),
        RUMonthNameAfterDate(),
        RUWeekdayParser(),
        RUTimeExprParser(strict_mode=False),
        RUTimeUnitAgoParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        RUMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        RUMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
