from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.en.parsers.en_month_name_little_endian_parser import ENMonthNameLittleEndianParser
from chrono_python.locales.en.parsers.en_month_name_middle_endian_parser import ENMonthNameMiddleEndianParser
from chrono_python.locales.en.parsers.en_time_unit_ago_parser import ENTimeUnitAgoParser
from chrono_python.locales.en.parsers.en_time_expr_parser import ENTimeExprParser
from chrono_python.locales.en.refiners import ENMergeDateRangeRefiner

configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        ENTimeExprParser(),
        ENMonthNameLittleEndianParser(),
        ENMonthNameMiddleEndianParser(),
        ENTimeUnitAgoParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        ENMergeDateRangeRefiner(),
    ])
casual = chrono.Chrono(configuration)
strict = chrono.Chrono(configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)
