import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN_WITH_PREFIX = re.compile(
    rf'(?:within|in|for)\s*(?:(?:about|around|roughly|approximately|just)\s*(?:~\s*)?)?({constants.TIME_UNITS_PATTERN})(?=\W|$)',
    re.IGNORECASE
)
PATTERN_WITH_PREFIX_STRICT = re.compile(
    rf'(?:within|in|for)\s*(?:(?:about|around|roughly|approximately|just)\s*(?:~\s*)?)?({constants.TIME_UNITS_NO_ABBR_PATTERN})(?=\W|$)',
    re.IGNORECASE
)


class ENTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self.allow_abbreviations = allow_abbreviations

    def inner_pattern(self) -> re.Pattern:
        if self.allow_abbreviations:
            return PATTERN_WITH_PREFIX
        return PATTERN_WITH_PREFIX_STRICT

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        if re.match(r'^for\s*the\s*\w+', match.group(0), re.IGNORECASE):
            return None
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None
        return ReferenceMoment(context.reference, time_units)
