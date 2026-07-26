from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.fr.parsers.fr_casual_date_parser import FRCasualDateParser
from chrono_python.locales.fr.parsers.fr_casual_time_parser import FRCasualTimeParser
from chrono_python.locales.fr.parsers.fr_month_name_after_date import FRMonthNameAfterDate
from chrono_python.locales.fr.parsers.fr_time_expr_parser import FRTimeExprParser
from chrono_python.locales.fr.parsers.fr_time_unit_ago_parser import FRTimeUnitAgoParser
from chrono_python.locales.fr.parsers.fr_time_unit_within_parser import FRTimeUnitWithinParser
from chrono_python.locales.fr.parsers.fr_time_unit_relative_parser import FRTimeUnitRelativeParser
from chrono_python.locales.fr.parsers.fr_weekday_parser import FRWeekdayParser
from chrono_python.locales.fr.refiners import (
    FRMergeDateRangeRefiner,
    FRMergeDateTimeRefiner,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        FRMonthNameAfterDate(),
        FRTimeExprParser(),
        FRTimeUnitAgoParser(),
        FRTimeUnitWithinParser(),
        FRWeekdayParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        FRMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        FRMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        FRCasualDateParser(),
        FRCasualTimeParser(),
        FRTimeUnitRelativeParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        FRMonthNameAfterDate(),
        FRTimeExprParser(),
        FRTimeUnitAgoParser(),
        FRTimeUnitWithinParser(),
        FRWeekdayParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        FRMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        FRMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
