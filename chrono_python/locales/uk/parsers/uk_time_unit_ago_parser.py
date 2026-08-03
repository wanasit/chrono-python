import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.uk import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    rf"({constants.TIME_UNITS_PATTERN})\s{{0,5}}тому(?=\W|$)",
    re.IGNORECASE,
)


class UKTimeUnitAgoParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode

    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        duration = constants.parse_duration(match.group(1))
        if not duration:
            return None

        negated = {unit: -val for unit, val in duration.items()}
        return ReferenceMoment.of(context.reference, negated)
