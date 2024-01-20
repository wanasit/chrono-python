import re

from chrono_python import chrono
from chrono_python.locales.en import constants
from chrono_python.types import DateTimeComponent, Moment
from chrono_python.utils import patterns, calendars

PATTERN = re.compile(
    f'({constants.PATTERN_ORDINAL_NUMBER})' +
    f'(?:\\s{{0,3}}(?:to|-|–|until|through|till)?\\s{{0,3}}({constants.PATTERN_ORDINAL_NUMBER}))?' +
    f'(?:-|/|\\s{{0,3}}(?:of)?\\s{{0,3}})' +
    f'({patterns.match_any(constants.FULL_MONTH_NAME_DICTIONARY)})' +
    f'(?:(?:-|/|,?\\s{{0,3}})({constants.PATTERN_YEAR}(?!\\S\\d)))?' +
    f'(?=\\W|$)',
    re.IGNORECASE
)


class ENMonthNameLittleEndianParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        month = constants.FULL_MONTH_NAME_DICTIONARY[match.group(3).lower()]
        day = constants.parse_ordinal_number(match.group(1))
        if day > 31:
            return None

        moment = chrono.ParsingMoment(context.reference, {})
        moment.assign(DateTimeComponent.DAY, day)
        moment.assign(DateTimeComponent.MONTH, month)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            moment.assign(DateTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(DateTimeComponent.YEAR, year)

        if not match.group(2):
            return moment

        end_day = constants.parse_ordinal_number(match.group(2))
        end_moment = moment.clone().assign(DateTimeComponent.DAY, end_day)
        return context.create_parsed_result(match.start(), match.end(), start=moment, end=end_moment)
