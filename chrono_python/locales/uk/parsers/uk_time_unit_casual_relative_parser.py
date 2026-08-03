import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.uk import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    rf"(ці|останні|минулі|майбутні|наступні|після|через|\+|-)\s*({constants.TIME_UNITS_PATTERN})(?=\W|$)",
    re.IGNORECASE,
)


class UKTimeUnitCasualRelativeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1).lower()
        duration = constants.parse_duration(match.group(2))
        if not duration:
            return None

        if prefix in ("останні", "минулі", "-"):
            duration = {unit: -val for unit, val in duration.items()}

        return ReferenceMoment.of(context.reference, duration)
