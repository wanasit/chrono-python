import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment

PATTERN = re.compile(
    r"([0-9]|0[1-9]|1[012])/([0-9]{4})",
    re.IGNORECASE,
)


class NLSlashMonthFormatParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        year = int(match.group(2))
        month = int(match.group(1))

        components = ParsingCivilTimeMoment.of(context.reference)
        components.imply(CivilTimeComponent.DAY, 1)
        components.assign(CivilTimeComponent.MONTH, month)
        components.assign(CivilTimeComponent.YEAR, year)
        return components
