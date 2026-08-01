import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.zh.hant.constants import WEEKDAY_OFFSET


class ZHHantRelationWeekdayParser(chrono.Parser):
    def __init__(self):
        weekday_keys = "|".join(WEEKDAY_OFFSET.keys())
        self._pattern = re.compile(
            rf"(?P<prefix>上|下|這)(?:個)?(?:星期|禮拜|週|周)(?P<weekday>{weekday_keys})",
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        day_of_week = match.group("weekday")
        offset = WEEKDAY_OFFSET.get(day_of_week)
        if offset is None:
            return None

        prefix = match.group("prefix")
        modifier = None
        if prefix == "上":
            modifier = "last"
        elif prefix == "下":
            modifier = "next"
        elif prefix == "這":
            modifier = "this"

        ref_dt = context.reference.datetime()
        ref_offset = (ref_dt.weekday() + 1) % 7
        start_moment_fixed = False

        if modifier == "last":
            diff = offset - 7 - ref_offset
            start_moment_fixed = True
        elif modifier == "next":
            diff = offset + 7 - ref_offset
            start_moment_fixed = True
        elif modifier == "this":
            diff = offset - ref_offset
        else:
            diff = offset - ref_offset
            if abs(diff - 7) < abs(diff):
                diff -= 7
            if abs(diff + 7) < abs(diff):
                diff += 7

        target_date = ref_dt + datetime.timedelta(days=diff)
        result = ParsingCivilTimeMoment.of(context.reference)
        result.assign(CivilTimeComponent.WEEKDAY, offset)

        if start_moment_fixed:
            result.assign(CivilTimeComponent.DAY, target_date.day)
            result.assign(CivilTimeComponent.MONTH, target_date.month)
            result.assign(CivilTimeComponent.YEAR, target_date.year)
        else:
            result.imply(CivilTimeComponent.DAY, target_date.day)
            result.imply(CivilTimeComponent.MONTH, target_date.month)
            result.imply(CivilTimeComponent.YEAR, target_date.year)

        return result
