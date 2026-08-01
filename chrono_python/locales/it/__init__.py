from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.it.parsers import (
    ITCasualDateParser,
    ITCasualTimeParser,
    ITMonthNameAfterDate,
    ITMonthNameBeforeDate,
    ITMonthNameParser,
    ITRelativeDateFormatParser,
    ITTimeExprParser,
    ITTimeUnitAgoParser,
    ITTimeUnitCasualRelativeParser,
    ITTimeUnitLaterParser,
    ITTimeUnitWithinParser,
    ITWeekdayParser,
)
from chrono_python.locales.it.refiners import (
    ITExtractYearSuffixRefiner,
    ITMergeDateRangeRefiner,
    ITMergeDateTimeRefiner,
    ITMergeRelativeAfterDateRefiner,
    ITMergeRelativeFollowByDateRefiner,
    ITUnlikelyFormatFilter,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.SlashYearMonthDateParser(strict_month_date_order=True),
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        ITTimeUnitWithinParser(strict_mode=True),
        ITMonthNameAfterDate(),
        ITMonthNameBeforeDate(should_skip_year_like_date=True),
        ITWeekdayParser(),
        ITTimeExprParser(),
        ITTimeUnitAgoParser(strict_mode=True),
        ITTimeUnitLaterParser(strict_mode=True),
    ],
    refiners=[
        ITMergeRelativeAfterDateRefiner(),
        ITMergeRelativeFollowByDateRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        ITMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        ITMergeDateTimeRefiner(),
        ITExtractYearSuffixRefiner(),
        ITMergeDateRangeRefiner(),
        ITUnlikelyFormatFilter(strict_mode=True),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        ITCasualDateParser(),
        ITCasualTimeParser(),
        ITMonthNameParser(),
        ITRelativeDateFormatParser(),
        ITTimeUnitCasualRelativeParser(),
        common_parsers.SlashYearMonthDateParser(strict_month_date_order=False),
        common_parsers.SlashDateMonthYearParser(little_endian=True),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashMonthYearParser(),
        ITTimeUnitWithinParser(strict_mode=False),
        ITMonthNameAfterDate(),
        ITMonthNameBeforeDate(should_skip_year_like_date=True),
        ITWeekdayParser(),
        ITTimeExprParser(),
        ITTimeUnitAgoParser(strict_mode=False),
        ITTimeUnitLaterParser(strict_mode=False),
    ],
    refiners=[
        ITMergeRelativeAfterDateRefiner(),
        ITMergeRelativeFollowByDateRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        ITMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        ITMergeDateTimeRefiner(),
        ITExtractYearSuffixRefiner(),
        ITMergeDateRangeRefiner(),
        ITUnlikelyFormatFilter(strict_mode=False),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
