import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.nl import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern(strict_mode: bool) -> re.Pattern:
    suffix = r"geleden" if strict_mode else r"(?:geleden|voor|eerder)"
    return re.compile(
        rf"({constants.TIME_UNITS_PATTERN}){suffix}(?=\W|$)",
        re.IGNORECASE,
    )


class NLTimeUnitAgoParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self._pattern = compile_pattern(strict_mode)

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        time_units = constants.parse_duration(match.group(1))
        if not time_units:
            return None
        output_time_units = {k: -v for k, v in time_units.items()}
        return ReferenceMoment.of(context.reference, output_time_units)
