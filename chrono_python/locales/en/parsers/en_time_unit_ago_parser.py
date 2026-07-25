import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

def compile_pattern(timeunit_pattern: str) -> re.Pattern:
    return re.compile(
        rf'({timeunit_pattern})\s{{0,5}}'
        rf'(?:ago|before|earlier)'
        rf'(?=\W|$)',
        re.IGNORECASE
    )


class ENTimeUnitAgoParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self._pattern = compile_pattern(
            constants.TIME_UNITS_PATTERN if allow_abbreviations else constants.TIME_UNITS_NO_ABBR_PATTERN
        )

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        duration = constants.parse_duration(match.group(1))
        if not duration:
            return None
        reversed_duration = {k: -v for k, v in duration.items()}
        return ReferenceMoment.of(context.reference, reversed_duration)
