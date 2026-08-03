from chrono_python import chrono
from chrono_python.common import parsers as common_parsers
from chrono_python.common import refiners as common_refiners
from chrono_python.locales.uk.parsers import (
    UKCasualDateParser,
    UKCasualTimeParser,
    UKMonthNameAfterDate,
    UKMonthNameParser,
    UKRelativeDateFormatParser,
    UKTimeExprParser,
    UKTimeUnitAgoParser,
    UKTimeUnitCasualRelativeParser,
    UKTimeUnitWithinParser,
    UKWeekdayParser,
)
from chrono_python.locales.uk.refiners import (
    UKMergeDateRangeRefiner,
    UKMergeDateTimeRefiner,
)


def create_configuration(strict_mode: bool = False) -> chrono.Configuration:
    return chrono.Configuration(
        parsers=[
            common_parsers.ISOFormatParser(),
            common_parsers.SlashDateMonthYearParser(little_endian=True),
            UKTimeUnitWithinParser(strict_mode=strict_mode),
            UKMonthNameAfterDate(),
            UKWeekdayParser(),
            UKTimeExprParser(strict_mode=strict_mode),
            UKTimeUnitAgoParser(strict_mode=strict_mode),
        ],
        refiners=[
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.ExtractTimezoneOffsetRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            common_refiners.MergeWeekdayComponentRefiner(),
            UKMergeDateTimeRefiner(),
            common_refiners.ExtractTimezoneAbbrRefiner(),
            common_refiners.RemoveOverlapRefiner(),
            UKMergeDateTimeRefiner(),
            UKMergeDateRangeRefiner(),
            common_refiners.InvalidDateFilter(),
        ],
    )


def create_casual_configuration() -> chrono.Configuration:
    option = create_configuration(strict_mode=False)
    option.parsers.insert(0, UKTimeUnitCasualRelativeParser())
    option.parsers.insert(0, UKRelativeDateFormatParser())
    option.parsers.insert(0, UKMonthNameParser())
    option.parsers.insert(0, UKCasualTimeParser())
    option.parsers.insert(0, UKCasualDateParser())
    return option


strict_configuration = create_configuration(strict_mode=True)
casual_configuration = create_casual_configuration()

casual = chrono.Chrono(casual_configuration)
strict = chrono.Chrono(strict_configuration)


def parse(*args, **kwargs) -> list[chrono.ParsedResult]:
    return casual.parse(*args, **kwargs)


def parse_date(*args, **kwargs):
    return casual.parse_date(*args, **kwargs)
