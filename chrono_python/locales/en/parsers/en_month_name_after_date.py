import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    f'({constants.PATTERN_ORDINAL_NUMBER})' +
    f'(?:\\s{{0,3}}(?:to|-|–|until|through|till)?\\s{{0,3}}({constants.PATTERN_ORDINAL_NUMBER}))?' +
    f'(?:-|/|\\s{{0,3}}(?:of)?\\s{{0,3}})' +
    f'({patterns.match_any(constants.MONTH_NAME_DICTIONARY)})' +
    f'(?:(?:-|/|,?\\s{{0,3}})({constants.PATTERN_YEAR}(?!\\S\\d)))?' +
    f'(?=\\W|$)',
    re.IGNORECASE
)


class ENMonthNameAfterDate(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        month = constants.MONTH_NAME_DICTIONARY[match.group(3).lower()]
        day = constants.parse_ordinal_number(match.group(1))
        if day > 31:
            return None

        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.assign(CivilTimeComponent.DAY, day)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        if not match.group(2):
            return moment

        end_day = constants.parse_ordinal_number(match.group(2))
        end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
        return context.create_parsed_result(match.start(), match.end(), start=moment, end=end_moment)
