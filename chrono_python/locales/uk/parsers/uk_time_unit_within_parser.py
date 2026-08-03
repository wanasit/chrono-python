import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.uk import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern(strict_mode: bool = False) -> re.Pattern:
    time_units_pat = constants.TIME_UNITS_PATTERN
    prefix = r"(?:протягом|на протязі|упродовж|впродовж)\s*" if strict_mode else r"(?:(?:протягом|на протязі|упродовж|впродовж)\s*)?"
    return re.compile(
        rf"{prefix}(?:(?:приблизно|орієнтовно)\s*(?:~\s*)?)?({time_units_pat})(?=\W|$)",
        re.IGNORECASE,
    )


class UKTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode
        self._pattern = compile_pattern(strict_mode)

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        duration = constants.parse_duration(match.group(1))
        if not duration:
            return None

        return ReferenceMoment.of(context.reference, duration)
