import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.vi import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern() -> re.Pattern:
    return re.compile(
        rf"({constants.TIME_UNITS_PATTERN})\s{{0,5}}(?:sau|nữa|tới|tiếp)"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VITimeUnitLaterParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        duration = constants.parse_duration(match[1])
        if not duration:
            return None
        return ReferenceMoment.of(context.reference, duration)
