import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem


class ZHHansCasualDateParser(chrono.Parser):
    def __init__(self):
        self._pattern = re.compile(
            r"(现在|立(?:刻|即)|即刻)|"
            r"(今|明|前|大前|后|大后|昨)(早|晚)|"
            r"(上(?:午)|早(?:上)|下(?:午)|晚(?:上)|夜(?:晚)?|中(?:午)|凌(?:晨))|"
            r"(今|明|前|大前|后|大后|昨)(?:日|天)"
            r"(?:[\s|,|，]*)"
            r"(?:(上(?:午)|早(?:上)|下(?:午)|晚(?:上)|夜(?:晚)?|中(?:午)|凌(?:晨)))?",
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        ref_dt = context.reference.datetime()
        target_date = datetime.datetime(ref_dt.year, ref_dt.month, ref_dt.day, ref_dt.hour, ref_dt.minute, ref_dt.second, ref_dt.microsecond, tzinfo=ref_dt.tzinfo)

        result = ParsingCivilTimeMoment.of(context.reference)

        now_group = match.group(1)
        day_group_1 = match.group(2)
        time_group_1 = match.group(3)
        time_group_2 = match.group(4)
        day_group_3 = match.group(5)
        time_group_3 = match.group(6)

        if now_group:
            result.imply(CivilTimeComponent.HOUR, ref_dt.hour)
            result.imply(CivilTimeComponent.MINUTE, ref_dt.minute)
            result.imply(CivilTimeComponent.SECOND, ref_dt.second)
            result.imply(CivilTimeComponent.MILLI_SECOND, ref_dt.microsecond // 1000)
        elif day_group_1:
            day1 = day_group_1
            time1 = time_group_1

            if day1 == "明":
                if ref_dt.hour > 1:
                    target_date += datetime.timedelta(days=1)
            elif day1 == "昨":
                target_date -= datetime.timedelta(days=1)
            elif day1 == "前":
                target_date -= datetime.timedelta(days=2)
            elif day1 == "大前":
                target_date -= datetime.timedelta(days=3)
            elif day1 == "后":
                target_date += datetime.timedelta(days=2)
            elif day1 == "大后":
                target_date += datetime.timedelta(days=3)

            if time1 == "早":
                result.imply(CivilTimeComponent.HOUR, 6)
            elif time1 == "晚":
                result.imply(CivilTimeComponent.HOUR, 22)
                result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
        elif time_group_2:
            time2_str = time_group_2
            time2 = time2_str[0]
            if time2 in ("早", "上"):
                result.imply(CivilTimeComponent.HOUR, 6)
            elif time2 == "下":
                result.imply(CivilTimeComponent.HOUR, 15)
                result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
            elif time2 == "中":
                result.imply(CivilTimeComponent.HOUR, 12)
                result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
            elif time2 in ("夜", "晚"):
                result.imply(CivilTimeComponent.HOUR, 22)
                result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
            elif time2 == "凌":
                result.imply(CivilTimeComponent.HOUR, 0)
        elif day_group_3:
            day3 = day_group_3
            if day3 == "明":
                if ref_dt.hour > 1:
                    target_date += datetime.timedelta(days=1)
            elif day3 == "昨":
                target_date -= datetime.timedelta(days=1)
            elif day3 == "前":
                target_date -= datetime.timedelta(days=2)
            elif day3 == "大前":
                target_date -= datetime.timedelta(days=3)
            elif day3 == "后":
                target_date += datetime.timedelta(days=2)
            elif day3 == "大后":
                target_date += datetime.timedelta(days=3)

            if time_group_3:
                time3_str = time_group_3
                time3 = time3_str[0]
                if time3 in ("早", "上"):
                    result.imply(CivilTimeComponent.HOUR, 6)
                elif time3 == "下":
                    result.imply(CivilTimeComponent.HOUR, 15)
                    result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
                elif time3 == "中":
                    result.imply(CivilTimeComponent.HOUR, 12)
                    result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
                elif time3 in ("夜", "晚"):
                    result.imply(CivilTimeComponent.HOUR, 22)
                    result.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM.value)
                elif time3 == "凌":
                    result.imply(CivilTimeComponent.HOUR, 0)

        result.assign(CivilTimeComponent.DAY, target_date.day)
        result.assign(CivilTimeComponent.MONTH, target_date.month)
        result.assign(CivilTimeComponent.YEAR, target_date.year)

        return result
