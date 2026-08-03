import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    r"(?:в течение|в течении)\s*"
    r"(?:(?:около|примерно)\s*(?:~\s*)?)?"
    f"({constants.TIME_UNITS_PATTERN})"
    r"(?=[^\w]|$)",
    re.IGNORECASE,
)


class RUTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None

        return ReferenceMoment.of(context.reference, time_units)
