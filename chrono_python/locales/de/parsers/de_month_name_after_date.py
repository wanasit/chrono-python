import re
from chrono_python import chrono
from chrono_python.locales.de import constants
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.utils import patterns
from chrono_python.common import calendars

PATTERN = re.compile(
    r"(?:^|[^\d０-９])"
    r"(?:am\s*?)?"
    f"({constants.ORDINAL_NUMBER_PATTERN})"
    f"(?:\\s*(?:bis\\s*zum|bis\\s*zu|bis|\\-|\\–|\\~)\\s*({constants.ORDINAL_NUMBER_PATTERN}))?"
    r"(?:-|\.|\s*(?:von)?\s*)"
    f"({patterns.match_any(constants.MONTH_DICTIONARY)})"
    f"(?:(?:-|/|\\.|,\\s*|\\s+)({constants.YEAR_PATTERN}(?![^\\s]\\d)))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class DEMonthNameAfterDate(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        full_text = match.group(0)
        day_str = match.group(1)

        start_idx = match.start()
        boundary_len = 0
        if not full_text.lower().startswith("am") and not full_text.lower().startswith(day_str.lower()):
            boundary_len = 1

        day = constants.parse_ordinal_number(day_str)
        if day > 31:
            return None

        month = constants.MONTH_DICTIONARY[match.group(3).lower()]

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.DAY, day)
        moment.assign(CivilTimeComponent.MONTH, month)

        if match.group(4):
            year = constants.parse_year(match.group(4))
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        real_start = start_idx + boundary_len
        real_end = match.end()

        if not match.group(2):
            return context.create_parsed_result(real_start, real_end, moment)

        end_day = constants.parse_ordinal_number(match.group(2))
        end_moment = moment.clone().assign(CivilTimeComponent.DAY, end_day)
        return context.create_parsed_result(
            real_start, real_end, start=moment, end=end_moment
        )
