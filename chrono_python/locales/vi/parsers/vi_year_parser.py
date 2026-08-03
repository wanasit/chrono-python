import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.vi import constants
from chrono_python.types import Moment


def compile_pattern() -> re.Pattern:
    return re.compile(
        rf"(?:\bnăm\s*({constants.YEAR_PATTERN})|\b([0-9]{{1,4}})\s*(TCN))"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VIYearParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        if match[1]:
            year_text = match[1]
        else:
            year_text = f"{match[2]} {match[3]}"

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.YEAR, constants.parse_year(year_text))
        moment.imply(CivilTimeComponent.MONTH, 1)
        moment.imply(CivilTimeComponent.DAY, 1)
        return moment
