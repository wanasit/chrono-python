from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.locales.en.parsers.en_month_name_little_endian_parser import ENMonthNameLittleEndianParser

configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        ENMonthNameLittleEndianParser()
    ],
    refiners=[])
casual = chrono.Chrono(configuration)
strict = chrono.Chrono(configuration)


def parse(text: str, reference, options):
    return casual.parse(text, reference, options)
