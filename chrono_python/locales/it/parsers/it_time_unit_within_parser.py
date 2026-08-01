import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.it import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern(strict_mode: bool = False) -> re.Pattern:
    time_units_pat = constants.TIME_UNITS_NO_ABBR_PATTERN if strict_mode else constants.TIME_UNITS_PATTERN
    return re.compile(
        r"(?:entro|tra|fra|in|per)\s*"
        r"(?:(?:circa|approssimativamente)\s*(?:~\s*)?)?"
        rf"({time_units_pat})(?=\W|$)",
        re.IGNORECASE,
    )


class ITTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode
        self._pattern = compile_pattern(strict_mode)

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        if re.match(r"^per\s*(il|la|l')\s*\w+", match.group(0), re.IGNORECASE):
            return None

        duration = constants.parse_duration(match.group(1))
        if not duration:
            return None

        return ReferenceMoment.of(context.reference, duration)
