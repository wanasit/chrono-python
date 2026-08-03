from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.nl.parsers import (
    NLCasualDateParser,
    NLCasualDateTimeParser,
    NLCasualTimeParser,
    NLCasualYearMonthDayParser,
    NLMonthNameAfterDate,
    NLMonthNameParser,
    NLRelativeDateFormatParser,
    NLSlashMonthFormatParser,
    NLTimeExprParser,
    NLTimeUnitAgoParser,
    NLTimeUnitCasualRelativeParser,
    NLTimeUnitLaterParser,
    NLTimeUnitWithinParser,
    NLWeekdayParser,
)
from chrono_python.locales.nl.refiners import (
    NLMergeDateRangeRefiner,
    NLMergeDateTimeRefiner,
)


def create_configuration(strict_mode: bool = True, little_endian: bool = True) -> chrono.Configuration:
    return chrono.Configuration(
        parsers=[
            common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
            common_parsers.ISOFormatParser(),
            NLTimeUnitWithinParser(),
            NLMonthNameAfterDate(),
            NLMonthNameParser(),
            NLWeekdayParser(),
            NLCasualYearMonthDayParser(),
            NLSlashMonthFormatParser(),
            NLTimeExprParser(strict_mode=strict_mode),
            NLTimeUnitAgoParser(strict_mode=strict_mode),
            NLTimeUnitLaterParser(strict_mode=strict_mode),
        ],
        refiners=[
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.ExtractTimezoneOffsetRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.MergeWeekdayComponentRefiner(),
            NLMergeDateTimeRefiner(),
            common_refiners.ExtractTimezoneAbbrRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            NLMergeDateRangeRefiner(),
            common_refiners.InvalidDateFilter(),
        ],
    )


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    option = create_configuration(strict_mode=False, little_endian=little_endian)
    option.parsers.insert(0, NLCasualDateParser())
    option.parsers.insert(0, NLCasualTimeParser())
    option.parsers.insert(0, NLCasualDateTimeParser())
    option.parsers.insert(0, NLMonthNameParser())
    option.parsers.insert(0, NLRelativeDateFormatParser())
    option.parsers.insert(0, NLTimeUnitCasualRelativeParser())
    return option


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
