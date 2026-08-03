from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.pt.parsers import (
    PTCasualDateParser,
    PTCasualTimeParser,
    PTMonthNameAfterDate,
    PTTimeExprParser,
    PTTimeUnitAgoParser,
    PTTimeUnitLaterParser,
    PTTimeUnitWithinParser,
    PTWeekdayParser,
)
from chrono_python.locales.pt.refiners import (
    PTMergeDateRangeRefiner,
    PTMergeDateTimeRefiner,
)


def create_configuration(
    strict_mode: bool = True, little_endian: bool = True
) -> chrono.Configuration:
    parsers = [
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
        PTWeekdayParser(),
        PTTimeExprParser(),
        PTMonthNameAfterDate(),
        PTTimeUnitWithinParser(),
        PTTimeUnitAgoParser(),
        PTTimeUnitLaterParser(),
    ]
    refiners = [
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        PTMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        PTMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ]
    return chrono.Configuration(parsers, refiners)


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    config = create_configuration(strict_mode=False, little_endian=little_endian)
    config.parsers.insert(0, PTCasualDateParser())
    config.parsers.insert(1, PTCasualTimeParser())
    return config


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
