import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.zh.hans.constants import WEEKDAY_OFFSET


class ZHHansWeekdayParser(chrono.Parser):
    def __init__(self):
        weekday_keys = "|".join(WEEKDAY_OFFSET.keys())
        self._pattern = re.compile(
            rf"(?:星期|礼拜|周)(?P<weekday>{weekday_keys})",
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        day_of_week = match.group("weekday")
        offset = WEEKDAY_OFFSET.get(day_of_week)
        if offset is None:
            return None

        ref_dt = context.reference.datetime()
        ref_offset = (ref_dt.weekday() + 1) % 7

        diff = offset - ref_offset
        if abs(diff - 7) < abs(diff):
            diff -= 7
        if abs(diff + 7) < abs(diff):
            diff += 7

        target_date = ref_dt + datetime.timedelta(days=diff)
        result = ParsingCivilTimeMoment.of(context.reference)
        result.assign(CivilTimeComponent.WEEKDAY, offset)
        result.imply(CivilTimeComponent.DAY, target_date.day)
        result.imply(CivilTimeComponent.MONTH, target_date.month)
        result.imply(CivilTimeComponent.YEAR, target_date.year)

        return result
