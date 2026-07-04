import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    rf'({constants.TIME_UNITS_PATTERN})\s{{0,5}}(?:later|after|from now|henceforth|forward|out)(?=\W|$)',
    re.IGNORECASE
)
STRICT_PATTERN = re.compile(
    rf'({constants.TIME_UNITS_NO_ABBR_PATTERN})\s{{0,5}}(?:later|after|from now)(?=\W|$)',
    re.IGNORECASE
)


class ENTimeUnitLaterParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self.allow_abbreviations = allow_abbreviations

    def inner_pattern(self) -> re.Pattern:
        return PATTERN if self.allow_abbreviations else STRICT_PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None
        return ReferenceMoment(context.reference, time_units)
