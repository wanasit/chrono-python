import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.pt import constants
from chrono_python.types import Moment, ReferenceMoment


def compile_pattern() -> re.Pattern:
    return re.compile(
        rf"(?:há|ha)\s*({constants.TIME_UNITS_PATTERN})"
        rf"|({constants.TIME_UNITS_PATTERN})\s*(?:atrás|atras)"
        rf"(?=\W|$)",
        re.IGNORECASE,
    )


class PTTimeUnitAgoParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        timeunits = match.group(1) or match.group(2)
        if not timeunits:
            return None
        duration = constants.parse_duration(timeunits)
        if not duration:
            return None
        neg_duration = {k: -v for k, v in duration.items()}
        return ReferenceMoment.of(context.reference, neg_duration)
