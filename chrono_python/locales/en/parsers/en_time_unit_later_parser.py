import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment

def compile_pattern(allow_abbreviations: bool, allow_casual_suffix: bool) -> re.Pattern:
    timeunit_pattern = constants.TIME_UNITS_PATTERN if allow_abbreviations else constants.TIME_UNITS_NO_ABBR_PATTERN
    if not allow_casual_suffix:
        return re.compile(
            rf'({timeunit_pattern})\s{{0,5}}(?:later|after|from now)(?=\W|$)',
            re.IGNORECASE
        )
    else:
        return re.compile(rf'({timeunit_pattern})\s{{0,5}}(?:later|after|from now|henceforth|forward|out)(?=\W|$)', re.IGNORECASE)


class ENTimeUnitLaterParser(AbstractParserWithWordBoundary):
    def __init__(self, 
                allow_abbreviations: bool = True, 
                allow_casual_suffix: bool = True
    ):  
        super().__init__()
        self._pattern = compile_pattern(
            allow_abbreviations=allow_abbreviations, 
            allow_casual_suffix=allow_casual_suffix
        )

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None
        return ReferenceMoment.of(context.reference, time_units)
