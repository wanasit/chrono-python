import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars
from chrono_python.locales.pt import constants


def compile_pattern() -> re.Pattern:
    return re.compile(
        r"([0-9]{1,2})(?:º|ª|°)?"
        r"(?:\s*(?:desde|de|\-|\–|ao?|\s)\s*([0-9]{1,2})(?:º|ª|°)?)?\s*(?:de)?\s*"
        r"(?:-|/|\s*(?:de|,)?\s*)"
        f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
        f"(?:\s*(?:de|,)?\s*({constants.YEAR_PATTERN}))?"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class PTMonthNameAfterDate(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        month_str = match.group(3).lower()
        if month_str not in constants.MONTH_DICTIONARY:
            return None
        month = constants.MONTH_DICTIONARY[month_str]

        day = int(match.group(1))
        if day > 31:
            return None

        component = ParsingCivilTimeMoment.of(context.reference)
        component.assign(CivilTimeComponent.MONTH, month)
        component.assign(CivilTimeComponent.DAY, day)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            component.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            component.imply(CivilTimeComponent.YEAR, year)

        if match.group(2):
            end_day = int(match.group(2))
            end_component = component.clone()
            end_component.assign(CivilTimeComponent.DAY, end_day)
            return context.create_parsed_result(
                match.start(), match.end(), component, end_component
            )

        return context.create_parsed_result(match.start(), match.end(), component)
