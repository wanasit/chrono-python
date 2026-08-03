import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.nl import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern() -> re.Pattern:
    return re.compile(
        rf"(dit|deze|vorig|afgelopen|(?:aan)?komend|over|\+|-)e?\s*({constants.TIME_UNITS_PATTERN})(?=\W|$)",
        re.IGNORECASE,
    )


PREFIX_WORD_GROUP = 1
TIME_UNIT_WORD_GROUP = 2


class NLTimeUnitCasualRelativeParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(PREFIX_WORD_GROUP).lower()
        time_units = constants.parse_duration(match.group(TIME_UNIT_WORD_GROUP))
        if not time_units:
            return None
        if prefix in ("vorig", "afgelopen", "-"):
            time_units = {k: -v for k, v in time_units.items()}

        return ReferenceMoment.of(context.reference, time_units)
