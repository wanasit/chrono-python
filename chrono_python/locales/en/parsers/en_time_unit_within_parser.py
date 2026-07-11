import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

def compile_pattern(timeunit_pattern: str) -> re.Pattern:
    return re.compile(
        rf'(?:within|in|for)\s*(?:(?:about|around|roughly|approximately|just)\s*(?:~\s*)?)?'
        rf'({timeunit_pattern})'
        rf'(?=\W|$)',
        re.IGNORECASE
    )


class ENTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self._pattern = compile_pattern(
            constants.TIME_UNITS_PATTERN if allow_abbreviations else constants.TIME_UNITS_NO_ABBR_PATTERN
        )

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        if re.match(r'^for\s*the\s*\w+', match.group(0), re.IGNORECASE):
            return None
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None
        return ReferenceMoment(context.reference, time_units)
