import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    rf'(this|last|past|next|after|\+|-)\s*({constants.TIME_UNITS_PATTERN})(?=\W|$)',
    re.IGNORECASE
)
PATTERN_NO_ABBR = re.compile(
    rf'(this|last|past|next|after|\+|-)\s*({constants.TIME_UNITS_NO_ABBR_PATTERN})(?=\W|$)',
    re.IGNORECASE
)


class ENTimeUnitCasualReferenceParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self.allow_abbreviations = allow_abbreviations

    def inner_pattern(self) -> re.Pattern:
        return PATTERN if self.allow_abbreviations else PATTERN_NO_ABBR

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1).lower()
        duration = constants.parse_duration(match.group(2))
        if not duration:
            return None
        if prefix in ('last', 'past', '-'):
            duration = {k: -v for k, v in duration.items()}
        return ReferenceMoment(context.reference, duration)
