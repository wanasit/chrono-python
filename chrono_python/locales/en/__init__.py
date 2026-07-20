from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.en.parsers.en_month_name_after_date import ENMonthNameAfterDate
from chrono_python.locales.en.parsers.en_month_name_before_date import ENMonthNameBeforeDate
from chrono_python.locales.en.parsers.en_month_name_before_year import ENMonthNameBeforeYear
from chrono_python.locales.en.parsers.en_month_name_after_year import ENMonthNameAfterYear
from chrono_python.locales.en.parsers.en_time_unit_ago_parser import ENTimeUnitAgoParser
from chrono_python.locales.en.parsers.en_time_unit_casual_reference_parser import ENTimeUnitCasualReferenceParser
from chrono_python.locales.en.parsers.en_time_unit_later_parser import ENTimeUnitLaterParser
from chrono_python.locales.en.parsers.en_time_unit_within_parser import ENTimeUnitWithinParser
from chrono_python.locales.en.parsers.en_time_expr_parser import ENTimeExprParser
from chrono_python.locales.en.parsers.en_weekday_parser import ENWeekdayParser
from chrono_python.locales.en.parsers.en_casual_date_parser import ENCasualDateParser
from chrono_python.locales.en.parsers.en_casual_time_parser import ENCasualTimeParser
from chrono_python.locales.en.refiners import ENMergeDateRangeRefiner, ENMergeDateTimeRefiner, ENUnlikelyFormatFilter

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        ENTimeExprParser(),
        ENWeekdayParser(),
        ENMonthNameAfterDate(),
        ENMonthNameBeforeDate(),
        ENMonthNameBeforeYear(),
        ENMonthNameAfterYear(),
        ENTimeUnitWithinParser(allow_abbreviations=False),
        ENTimeUnitAgoParser(allow_abbreviations=False),
        ENTimeUnitLaterParser(allow_abbreviations=False, allow_casual_suffix=False),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        ENMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        ENMergeDateRangeRefiner(),
        ENUnlikelyFormatFilter(),
    ])

casual_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        ENTimeExprParser(),
        ENWeekdayParser(),
        ENMonthNameAfterDate(),
        ENMonthNameBeforeDate(),
        ENMonthNameBeforeYear(),
        ENMonthNameAfterYear(),
        ENTimeUnitWithinParser(allow_abbreviations=True),
        ENTimeUnitAgoParser(allow_abbreviations=True),
        ENTimeUnitLaterParser(allow_abbreviations=True, allow_casual_suffix=True),
        ENTimeUnitCasualReferenceParser(allow_abbreviations=True),
        ENCasualDateParser(),
        ENCasualTimeParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.ExtractTimezoneOffsetRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        common_refiners.MergeWeekdayComponentRefiner(),
        ENMergeDateTimeRefiner(),
        common_refiners.ExtractTimezoneAbbrRefiner(),
        common_refiners.RemoveOverlapRefiner(),
        ENMergeDateRangeRefiner(),
        ENUnlikelyFormatFilter(),
    ])

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)

