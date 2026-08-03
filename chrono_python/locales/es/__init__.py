from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.es.parsers.es_casual_date_parser import ESCasualDateParser
from chrono_python.locales.es.parsers.es_casual_time_parser import ESCasualTimeParser
from chrono_python.locales.es.parsers.es_month_name_after_date import ESMonthNameAfterDate
from chrono_python.locales.es.parsers.es_time_expr_parser import ESTimeExprParser
from chrono_python.locales.es.parsers.es_time_unit_within_parser import ESTimeUnitWithinParser
from chrono_python.locales.es.parsers.es_weekday_parser import ESWeekdayParser
from chrono_python.locales.es.refiners.es_merge_date_range_refiner import ESMergeDateRangeRefiner
from chrono_python.locales.es.refiners.es_merge_date_time_refiner import ESMergeDateTimeRefiner


def create_casual_configuration(little_endian: bool = True) -> chrono.Configuration:
    option = create_configuration(strict_mode=False, little_endian=little_endian)
    option.parsers.insert(0, ESCasualDateParser())
    option.parsers.insert(1, ESCasualTimeParser())
    return option


def create_configuration(strict_mode: bool = True, little_endian: bool = True) -> chrono.Configuration:
    return chrono.Configuration(
        parsers=[
            common_parsers.SlashDateMonthYearParser(little_endian=little_endian),
            common_parsers.ISOFormatParser(),
            common_parsers.SlashMonthYearParser(),
            ESWeekdayParser(),
            ESTimeExprParser(),
            ESMonthNameAfterDate(),
            ESTimeUnitWithinParser(),
        ],
        refiners=[
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.ExtractTimezoneOffsetRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.MergeWeekdayComponentRefiner(),
            ESMergeDateTimeRefiner(),
            common_refiners.ExtractTimezoneAbbrRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            ESMergeDateRangeRefiner(),
            common_refiners.InvalidDateFilter(),
        ],
    )


casual_configuration = create_casual_configuration()
strict_configuration = create_configuration(strict_mode=True)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
