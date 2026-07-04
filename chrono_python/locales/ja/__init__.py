from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.ja.parsers.jp_standard_parser import JPStandardParser
from chrono_python.locales.ja.refiners import JPMergeDateRangeRefiner

configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        common_parsers.SlashDateFormatParser(little_endian=False),
        common_parsers.TimeExprParser(),
        JPStandardParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        JPMergeDateRangeRefiner(),
    ])

casual = chrono.Chrono(configuration)
strict = chrono.Chrono(configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)
