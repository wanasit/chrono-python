import re

from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.common import calendars
from chrono_python.locales.ja.constants import to_hankaku

# Regex matching Japanese standard date format (e.g. 令和元年5月1日, 2012年3月31日, 7月27日)
PATTERN = re.compile(
    r'(?:(?:([同今本])|((昭和|平成|令和)?([0-9０-９]{1,4}|元)))年\s*)?'
    r'([0-9０-９]{1,2})月\s*'
    r'([0-9０-９]{1,2})日',
    re.IGNORECASE
)

SPECIAL_YEAR_GROUP = 1
TYPICAL_YEAR_GROUP = 2
ERA_GROUP = 3
YEAR_NUMBER_GROUP = 4
MONTH_GROUP = 5
DAY_GROUP = 6


class JPYearMonthDateParser(chrono.Parser):
    """Parser for Japanese standard date formats."""

    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        month = int(to_hankaku(match.group(MONTH_GROUP)))
        day = int(to_hankaku(match.group(DAY_GROUP)))

        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.assign(CivilTimeComponent.MONTH, month)
        moment.assign(CivilTimeComponent.DAY, day)

        special_year = match.group(SPECIAL_YEAR_GROUP)
        typical_year = match.group(TYPICAL_YEAR_GROUP)

        if special_year and special_year in ("同", "今", "本"):
            moment.assign(CivilTimeComponent.YEAR, context.reference.datetime().year)
        elif typical_year:
            year_num_text = match.group(YEAR_NUMBER_GROUP)
            year = 1 if year_num_text == "元" else int(to_hankaku(year_num_text))
            
            era = match.group(ERA_GROUP)
            if era == "令和":
                year += 2018
            elif era == "平成":
                year += 1988
            elif era == "昭和":
                year += 1925
                
            moment.assign(CivilTimeComponent.YEAR, year)
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, day)
            moment.imply(CivilTimeComponent.YEAR, year)

        return moment
