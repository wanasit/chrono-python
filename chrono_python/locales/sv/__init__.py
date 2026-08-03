from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.sv.parsers import (
    SVCasualDateParser,
    SVMonthNameAfterDate,
    SVTimeExprParser,
    SVTimeUnitAgoParser,
    SVTimeUnitRelativeParser,
    SVTimeUnitWithinParser,
    SVWeekdayParser,
)
from chrono_python.locales.sv.refiners import (
    SVMergeDateRangeRefiner,
    SVMergeDateTimeRefiner,
)


def create_configuration(strict_mode: bool = True, little_endian: bool = True) -> chrono.Configuration:
    parsers = [
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
        common_parsers.SlashMonthYearParser(),
        SVMonthNameAfterDate(),
        SVWeekdayParser(),
        SVTimeUnitRelativeParser(),
        SVTimeExprParser(),
        SVTimeUnitAgoParser(),
        SVTimeUnitWithinParser(),
    ]
    refiners = [
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        SVMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        SVMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ]
    return chrono.Configuration(parsers=parsers, refiners=refiners)


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    config = create_configuration(strict_mode=False, little_endian=little_endian)
    config.parsers.insert(0, SVCasualDateParser())
    return config


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(text: str, reference=None, option=None) -> list[chrono.ParsedResult]:
    return casual.parse(text, reference)


def parse_date(text: str, reference=None, option=None):
    return casual.parse_date(text, reference)
