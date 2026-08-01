from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.zh.hans.parsers import (
    ZHHansCasualDateParser,
    ZHHansDateParser,
    ZHHansDeadlineFormatParser,
    ZHHansAgoFormatParser,
    ZHHansRelationWeekdayParser,
    ZHHansTimeExpressionParser,
    ZHHansWeekdayParser,
)
from chrono_python.locales.zh.hans.refiners import (
    ZHHansMergeDateRangeRefiner,
    ZHHansMergeDateTimeRefiner,
)

strict_configuration = chrono.Configuration(
    parsers=[
        common_parsers.ISOFormatParser(),
        ZHHansDateParser(),
        ZHHansRelationWeekdayParser(),
        ZHHansWeekdayParser(),
        ZHHansTimeExpressionParser(),
        ZHHansDeadlineFormatParser(),
        ZHHansAgoFormatParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        ZHHansMergeDateTimeRefiner(),
        ZHHansMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual_configuration = chrono.Configuration(
    parsers=[
        ZHHansCasualDateParser(),
        common_parsers.ISOFormatParser(),
        ZHHansDateParser(),
        ZHHansRelationWeekdayParser(),
        ZHHansWeekdayParser(),
        ZHHansTimeExpressionParser(),
        ZHHansDeadlineFormatParser(),
        ZHHansAgoFormatParser(),
    ],
    refiners=[
        common_refiners.RemoveOverlapRefiner(),
        ZHHansMergeDateTimeRefiner(),
        ZHHansMergeDateRangeRefiner(),
        common_refiners.InvalidDateFilter(),
    ],
)

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
