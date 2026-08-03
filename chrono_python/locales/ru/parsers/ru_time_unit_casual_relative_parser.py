import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.ru import constants
from chrono_python.types import Moment, ReferenceMoment

PATTERN = re.compile(
    f"(эти|последние|прошлые|следующие|после|спустя|через|\\+|-)\\s*({constants.TIME_UNITS_PATTERN})",
    re.IGNORECASE,
)


class RUTimeUnitCasualRelativeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1).lower()
        time_units = constants.parse_duration(match.group(2))
        if not time_units:
            return None

        if prefix in ("последние", "прошлые", "-"):
            time_units = {k: -v for k, v in time_units.items()}

        return ReferenceMoment.of(context.reference, time_units)
