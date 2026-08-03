import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.common import calendars
from chrono_python.locales.vi import constants
from chrono_python.types import Moment


def compile_pattern() -> re.Pattern:
    return re.compile(
        r"(?:ngày\s*)?"
        r"([0-9]{1,2})"
        r"\s*tháng\s*"
        r"([0-9]{1,2})"
        rf"(?:\s*năm\s*({constants.YEAR_PATTERN}))?"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VIStandardParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        day = int(match[1])
        month = int(match[2])
        if day > 31 or day <= 0 or month > 12 or month <= 0:
            return None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.DAY, day)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match[3]:
            moment.assign(CivilTimeComponent.YEAR, constants.parse_year(match[3]))
        else:
            moment.imply(
                CivilTimeComponent.YEAR,
                calendars.find_year_closest_to_ref(context.reference, month, day),
            )

        return moment


class VIMonthNameAfterDate(VIStandardParser):
    pass
