from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.locales.en.parsers.en_month_name_little_endian_parser import ENMonthNameLittleEndianParser
from chrono_python.locales.en.parsers.en_time_unit_ago_parser import ENTimeUnitAgoParser

configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        ENMonthNameLittleEndianParser(),
        ENTimeUnitAgoParser(),
    ],
    refiners=[])
casual = chrono.Chrono(configuration)
strict = chrono.Chrono(configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)
