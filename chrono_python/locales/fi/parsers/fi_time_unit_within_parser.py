import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.fi import constants
from chrono_python.types import Moment, ReferenceMoment


class FITimeUnitWithinParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return re.compile(
            rf"({constants.TIME_UNITS_PATTERN})\s*(?:sisällä|kuluessa|päästä)(?=\W|$)",
            re.IGNORECASE,
        )

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        duration = constants.parse_duration(match.group(1))
        if not duration:
            return None
        return ReferenceMoment.of(context.reference, duration)
