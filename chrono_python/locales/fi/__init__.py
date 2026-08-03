from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.fi.parsers import (
    FICasualDateParser,
    FICasualTimeParser,
    FIMonthNameAfterDate,
    FITimeExprParser,
    FITimeUnitAgoParser,
    FITimeUnitRelativeParser,
    FITimeUnitWithinParser,
    FIWeekdayParser,
)
from chrono_python.locales.fi.refiners import (
    FIMergeDateRangeRefiner,
    FIMergeDateTimeRefiner,
)


def create_configuration(strict_mode: bool = True, little_endian: bool = True) -> chrono.Configuration:
    return chrono.Configuration(
        parsers=[
            common_parsers.ISOFormatParser(),
            common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
            common_parsers.SlashMonthYearParser(),
            FITimeExprParser(strict_mode=strict_mode),
            FIMonthNameAfterDate(),
            FIWeekdayParser(),
            FITimeUnitWithinParser(),
            FITimeUnitAgoParser(),
        ],
        refiners=[
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.ExtractTimezoneOffsetRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.MergeWeekdayComponentRefiner(),
            FIMergeDateTimeRefiner(),
            common_refiners.ExtractTimezoneAbbrRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            FIMergeDateRangeRefiner(),
            common_refiners.InvalidDateFilter(),
        ],
    )


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    config = create_configuration(strict_mode=False, little_endian=little_endian)
    config.parsers.insert(0, FITimeUnitRelativeParser())
    config.parsers.insert(0, FICasualDateParser())
    config.parsers.insert(0, FICasualTimeParser())
    return config


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
