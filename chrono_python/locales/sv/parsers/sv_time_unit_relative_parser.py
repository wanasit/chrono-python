import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.sv import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern(allow_abbreviations: bool) -> re.Pattern:
    time_units_pat = (
        constants.TIME_UNITS_PATTERN
        if allow_abbreviations
        else constants.TIME_UNITS_NO_ABBR_PATTERN
    )
    return re.compile(
        rf"(denna|den här|förra|passerade|nästa|kommande|efter|\+|-)\s*({time_units_pat})(?=\W|$)",
        re.IGNORECASE,
    )


class SVTimeUnitRelativeParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self.allow_abbreviations = allow_abbreviations
        self._pattern = compile_pattern(allow_abbreviations)

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1).lower()
        duration = constants.parse_duration(match.group(2))
        if not duration:
            return None

        if prefix in ("förra", "passerade", "-"):
            duration = {k: -v for k, v in duration.items()}

        return ReferenceMoment.of(context.reference, duration)
