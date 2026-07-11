from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.ja.parsers.jp_standard_parser import JPStandardParser
from chrono_python.locales.ja.parsers.jp_time_expr_parser import JPTimeExprParser
from chrono_python.locales.ja.parsers.jp_weekday_parser import JPWeekdayParser
from chrono_python.locales.ja.parsers.jp_casual_date_parser import JPCasualDateParser
from chrono_python.locales.ja.parsers.jp_weekday_with_parentheses_parser import JPWeekdayWithParenthesesParser
from chrono_python.locales.ja.refiners.jp_merge_weekday_component_refiner import JPMergeWeekdayComponentRefiner
from chrono_python.locales.ja.refiners import JPMergeDateRangeRefiner, JPMergeDateTimeRefiner, JPUnlikelyFormatFilter

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        JPTimeExprParser(),
        JPWeekdayParser(),
        JPWeekdayWithParenthesesParser(),
        JPStandardParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        JPMergeWeekdayComponentRefiner(),
        JPMergeDateTimeRefiner(),
        JPMergeDateRangeRefiner(),
        JPUnlikelyFormatFilter(),
    ])

casual_configuration = chrono.Configuration(
    parsers=[
        JPCasualDateParser(),
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        JPTimeExprParser(),
        JPWeekdayParser(),
        JPWeekdayWithParenthesesParser(),
        JPStandardParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        JPMergeWeekdayComponentRefiner(),
        JPMergeDateTimeRefiner(),
        JPMergeDateRangeRefiner(),
        JPUnlikelyFormatFilter(),
    ])

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)
