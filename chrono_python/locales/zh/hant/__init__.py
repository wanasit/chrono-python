from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.zh.hant.parsers import (
    ZHHantCasualDateParser,
    ZHHantDateParser,
    ZHHantDeadlineFormatParser,
    ZHHantAgoFormatParser,
    ZHHantRelationWeekdayParser,
    ZHHantTimeExpressionParser,
    ZHHantWeekdayParser,
)
from chrono_python.locales.zh.hant.refiners import (
    ZHHantMergeDateRangeRefiner,
    ZHHantMergeDateTimeRefiner,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        ZHHantDateParser(),
        ZHHantRelationWeekdayParser(),
        ZHHantWeekdayParser(),
        ZHHantTimeExpressionParser(),
        ZHHantDeadlineFormatParser(),
        ZHHantAgoFormatParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        ZHHantMergeDateTimeRefiner(),
        ZHHantMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        ZHHantCasualDateParser(),
        common_parsers.ISOFormatParser(),
        ZHHantDateParser(),
        ZHHantRelationWeekdayParser(),
        ZHHantWeekdayParser(),
        ZHHantTimeExpressionParser(),
        ZHHantDeadlineFormatParser(),
        ZHHantAgoFormatParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        ZHHantMergeDateTimeRefiner(),
        ZHHantMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
