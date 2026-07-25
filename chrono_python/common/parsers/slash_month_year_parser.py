import re

from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

# Month/Year date format with slash "/" between numbers
# e.g., 04/2016, 06/2004
PATTERN = re.compile(
    r'([0-9]|0[1-9]|1[012])/([0-9]{4})',
    re.IGNORECASE
)


class SlashMonthYearParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> ParsingCivilTimeMoment | None:
        month = int(match.group(1))
        year = int(match.group(2))

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.imply(CivilTimeComponent.DAY, 1)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.YEAR, year)

        return moment
