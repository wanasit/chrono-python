import re

from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

# Numeric date pattern starting with year: YYYY/MM/DD, YYYY-MM-DD, YYYY.MM.DD, YYYY/MM
PATTERN = re.compile(
    r'([0-9]{4})[-\.\/\s]'
    r'([0-9]{1,2})'
    r'(?:[-\.\/\s]([0-9]{1,2}))?'
    r'(?=\W|$)',
    re.IGNORECASE
)


class SlashYearMonthDateParser(AbstractParserWithWordBoundary):
    """
    Parser for numeric date patterns starting with year: YYYY/MM/DD, YYYY-MM-DD, YYYY.MM.DD.
    The day/date part is optional (e.g. YYYY/MM is supported).
    """

    def __init__(self, strict_month_date_order: bool = False):
        super().__init__()
        self.strict_month_date_order = strict_month_date_order

    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> ParsingCivilTimeMoment | None:
        year = int(match.group(1))
        month = int(match.group(2))
        day_match = match.group(3)

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.YEAR, year)

        if day_match is not None:
            day = int(day_match)
            if month < 1 or month > 12:
                if self.strict_month_date_order:
                    return None
                if 1 <= day <= 12 and month <= 31:
                    day, month = month, day
                else:
                    return None

            if day < 1 or day > 31:
                return None

            moment.assign(CivilTimeComponent.MONTH, month)
            moment.assign(CivilTimeComponent.DAY, day)
        else:
            if month < 1 or month > 12:
                return None
            moment.assign(CivilTimeComponent.MONTH, month)
            moment.imply(CivilTimeComponent.DAY, 1)

        return moment
