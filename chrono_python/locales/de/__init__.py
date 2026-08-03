from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.de.parsers import (
    DECasualDateParser,
    DECasualTimeParser,
    DEMonthNameAfterDate,
    DESpecificTimeExpressionParser,
    DETimeExprParser,
    DETimeUnitRelativeParser,
    DETimeUnitWithinParser,
    DEWeekdayParser,
)
from chrono_python.locales.de.refiners import (
    DEMergeDateRangeRefiner,
    DEMergeDateTimeRefiner,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        DEMonthNameAfterDate(),
        DESpecificTimeExpressionParser(),
        DETimeExprParser(),
        DETimeUnitWithinParser(),
        DEWeekdayParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        DEMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        DEMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        DECasualDateParser(),
        DECasualTimeParser(),
        DETimeUnitRelativeParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        DEMonthNameAfterDate(),
        DESpecificTimeExpressionParser(),
        DETimeExprParser(),
        DETimeUnitWithinParser(),
        DEWeekdayParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        DEMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        DEMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
