import re
import calendar

from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.common import calendars
from chrono_python.utils.patterns import to_hankaku

# Regex matching Japanese year/month date format (e.g. 2026年4月, 2026年4月上旬・中旬)
PATTERN = re.compile(
    r'(?:(?:([同今本])|((昭和|平成|令和)?([0-9０-９]{1,4}|元)))年\s*)?'
    r'([0-9０-９]{1,2})月\s*'
    r'(?:の\s*)?'
    r'(?:(上旬|中旬|下旬)(?:\s*(?:[・〜~-]|from|to|・|〜|~|-|から)\s*(上旬|中旬|下旬))?)?',
    re.IGNORECASE
)

_SPECIAL_YEAR_GROUP = 1
_TYPICAL_YEAR_GROUP = 2
_ERA_GROUP = 3
_YEAR_NUMBER_GROUP = 4
_MONTH_GROUP = 5
_FIRST_SECTION_GROUP = 6
_SECOND_SECTION_GROUP = 7


def _last_day_of_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


class JPYearMonthParser(chrono.Parser):
    """Parser for Japanese year and month formats, including month sections (上旬, 中旬, 下旬)."""

    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        month = int(to_hankaku(match.group(_MONTH_GROUP)))

        special_year = match.group(_SPECIAL_YEAR_GROUP)
        typical_year = match.group(_TYPICAL_YEAR_GROUP)

        year = None
        year_certain = False
        if special_year and special_year in ("同", "今", "本"):
            year = context.reference.datetime().year
            year_certain = True
        elif typical_year:
            year_num_text = match.group(_YEAR_NUMBER_GROUP)
            year = 1 if year_num_text == "元" else int(to_hankaku(year_num_text))
            
            era = match.group(_ERA_GROUP)
            if era == "令和":
                year += 2018
            elif era == "平成":
                year += 1988
            elif era == "昭和":
                year += 1925
            year_certain = True
        else:
            year = calendars.find_year_closest_to_ref(context.reference, month, 1)
            year_certain = False

        start_moment = ParsingCivilTimeMoment.of(context.reference)
        if year_certain:
            start_moment.assign(CivilTimeComponent.YEAR, year)
        else:
            start_moment.imply(CivilTimeComponent.YEAR, year)
        start_moment.assign(CivilTimeComponent.MONTH, month)

        first_section = match.group(_FIRST_SECTION_GROUP)
        second_section = match.group(_SECOND_SECTION_GROUP)

        if not first_section:
            # Just year/month
            start_moment.imply(CivilTimeComponent.DAY, 1)
            return context.create_parsed_result(match.start(), match.end(), start_moment)

        # Section days lookup
        section_days = {
            "上旬": (1, 10),
            "中旬": (11, 20),
            "下旬": (21, _last_day_of_month(year, month))
        }

        start_day = section_days[first_section][0]
        end_day = section_days[second_section or first_section][1]

        start_moment.imply(CivilTimeComponent.DAY, start_day)

        end_moment = start_moment.clone()
        end_moment.imply(CivilTimeComponent.DAY, end_day)

        return context.create_parsed_result(match.start(), match.end(), start_moment, end_moment)
