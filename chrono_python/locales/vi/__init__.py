from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.vi.parsers import (
    VICasualDateParser,
    VICasualTimeParser,
    VIMonthYearParser,
    VIMonthNameBeforeDate,
    VIStandardParser,
    VIMonthNameAfterDate,
    VITimeExprParser,
    VITimeUnitAgoParser,
    VITimeUnitLaterParser,
    VITimeUnitWithinParser,
    VITimeUnitCasualRelativeParser,
    VITimeUnitRelativeParser,
    VIWeekdayParser,
    VIYearParser,
)
from chrono_python.locales.vi.refiners import (
    VIMergeDateRangeRefiner,
    VIMergeDateTimeRefiner,
    VIMergeWeekdayComponentRefiner,
)


def create_configuration(strict_mode: bool = True, little_endian: bool = True) -> chrono.Configuration:
    return chrono.Configuration(
        parsers=[
            common_parsers.ISOFormatParser(),
            common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
            VIStandardParser(),
            VIMonthYearParser(),
            VIYearParser(),
            VIWeekdayParser(strict_mode=strict_mode),
            VITimeExprParser(),
            VITimeUnitAgoParser(strict_mode=strict_mode),
            VITimeUnitLaterParser(strict_mode=strict_mode),
            VITimeUnitWithinParser(strict_mode=strict_mode),
        ],
        refiners=[
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.ExtractTimezoneOffsetRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            VIMergeWeekdayComponentRefiner(),
            VIMergeDateTimeRefiner(),
            common_refiners.ExtractTimezoneAbbrRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            VIMergeDateRangeRefiner(),
            common_refiners.InvalidDateFilter(),
        ],
    )


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    config = create_configuration(strict_mode=False, little_endian=little_endian)
    config.parsers.insert(0, VITimeUnitCasualRelativeParser())
    config.parsers.insert(0, VICasualTimeParser())
    config.parsers.insert(0, VICasualDateParser())
    return config


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
