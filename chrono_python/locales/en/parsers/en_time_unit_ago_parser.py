import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.types import ReferenceMoment, Moment


class ENTimeUnitAgoParser(chrono.Parser):
    PATTERN = re.compile(
        f'({constants.PATTERN_TIME_UNITS})\\s{{0,5}}(?:ago|before|earlier)',
        re.IGNORECASE
    )

    def pattern(self) -> re.Pattern:
        return self.PATTERN

    def extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        time_units = constants.parse_time_units(match.group(1))
        time_units = {k: -v for k, v in time_units.items()}
        moment = ReferenceMoment(context.reference, time_units)
        return moment
