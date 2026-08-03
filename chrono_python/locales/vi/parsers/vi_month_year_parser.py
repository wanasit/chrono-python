import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.vi import constants
from chrono_python.types import Moment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    return re.compile(
        f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
        rf"(?:\s*(?:năm|/)\s*({constants.YEAR_PATTERN}))?"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VIMonthYearParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month_str = match[1].lower()
        month = constants.MONTH_DICTIONARY.get(month_str)
        if not month:
            return None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.imply(CivilTimeComponent.DAY, 1)

        if match[2]:
            moment.assign(CivilTimeComponent.YEAR, constants.parse_year(match[2]))
        else:
            ref_dt = context.reference.datetime()
            moment.imply(CivilTimeComponent.YEAR, ref_dt.year)

        return moment


class VIMonthNameBeforeDate(VIMonthYearParser):
    pass
