from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.ja.parsers.ja_year_month_date_parser import JAYearMonthDateParser
from chrono_python.locales.ja.parsers.ja_year_month_parser import JAYearMonthParser
from chrono_python.locales.ja.parsers.ja_time_expr_parser import JATimeExprParser
from chrono_python.locales.ja.parsers.ja_weekday_parser import JAWeekdayParser
from chrono_python.locales.ja.parsers.ja_casual_date_parser import JACasualDateParser
from chrono_python.locales.ja.parsers.ja_casual_time_parser import JACasualTimeParser
from chrono_python.locales.ja.parsers.ja_weekday_with_parentheses_parser import JAWeekdayWithParenthesesParser
from chrono_python.locales.ja.refiners.ja_merge_weekday_component_refiner import JAMergeWeekdayComponentRefiner
from chrono_python.locales.ja.refiners import JAMergeDateRangeRefiner, JAMergeDateTimeRefiner, JAUnlikelyFormatFilter

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=False),
        common_parsers.SlashMonthYearParser(),
        common_parsers.SlashYearMonthDateParser(strict_month_date_order=True),
        JATimeExprParser(),
        JAWeekdayParser(),
        JAWeekdayWithParenthesesParser(),
        JAYearMonthDateParser(),
        JAYearMonthParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        JAMergeWeekdayComponentRefiner(),
        JAMergeDateTimeRefiner(),
        JAMergeDateRangeRefiner(),
        JAUnlikelyFormatFilter(),
        common_refiners.InvalidDateFilter(),
    ])

casual_configuration = chrono.Configuration(
    parsers=[
        JACasualDateParser(),
        JACasualTimeParser(),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateMonthYearParser(little_endian=False),
        common_parsers.SlashMonthYearParser(),
        common_parsers.SlashYearMonthDateParser(strict_month_date_order=True),
        JATimeExprParser(),
        JAWeekdayParser(),
        JAWeekdayWithParenthesesParser(),
        JAYearMonthDateParser(),
        JAYearMonthParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        JAMergeWeekdayComponentRefiner(),
        JAMergeDateTimeRefiner(),
        JAMergeDateRangeRefiner(),
        JAUnlikelyFormatFilter(),
        common_refiners.InvalidDateFilter(),
    ])

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)
