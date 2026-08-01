import re
import datetime
import calendar
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.zh.hans.constants import NUMBER, zh_string_to_number


def _add_months(dt: datetime.datetime, months: int) -> datetime.datetime:
    total_months = dt.year * 12 + (dt.month - 1) + months
    new_year = total_months // 12
    new_month = total_months % 12 + 1
    max_days = calendar.monthrange(new_year, new_month)[1]
    new_day = min(dt.day, max_days)
    return dt.replace(year=new_year, month=new_month, day=new_day)


def _add_years(dt: datetime.datetime, years: int) -> datetime.datetime:
    new_year = dt.year + years
    max_days = calendar.monthrange(new_year, dt.month)[1]
    new_day = min(dt.day, max_days)
    return dt.replace(year=new_year, day=new_day)


class ZHHansDeadlineFormatParser(chrono.Parser):
    def __init__(self):
        num_chars = "".join(NUMBER.keys())
        self._pattern = re.compile(
            rf"(\d+|[{num_chars}]+|半|几)(?:\s*)"
            rf"(?:个)?"
            rf"(秒(?:钟)?|分钟|小时|钟|日|天|星期|礼拜|月|年)"
            rf"(?:(?:之|过)?后|(?:之)?内)",
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        num_str = match.group(1)
        unit = match.group(2)

        if num_str.isdigit():
            number = float(int(num_str))
        else:
            try:
                number = float(zh_string_to_number(num_str))
            except Exception:
                number = None

        if number is None or number == 0:
            if num_str == "几":
                number = 3.0
            elif num_str == "半":
                number = 0.5
            else:
                return None

        result = ParsingCivilTimeMoment.of(context.reference)
        ref_dt = context.reference.datetime()
        unit_abbr = unit[0]

        if unit_abbr in "日天星礼月年":
            if unit_abbr in ("日", "天"):
                target_dt = ref_dt + datetime.timedelta(days=number)
            elif unit_abbr in ("星", "礼"):
                target_dt = ref_dt + datetime.timedelta(weeks=number)
            elif unit_abbr == "月":
                target_dt = _add_months(ref_dt, int(number))
            elif unit_abbr == "年":
                target_dt = _add_years(ref_dt, int(number))
            else:
                return None

            result.assign(CivilTimeComponent.YEAR, target_dt.year)
            result.assign(CivilTimeComponent.MONTH, target_dt.month)
            result.assign(CivilTimeComponent.DAY, target_dt.day)
            return result

        if unit_abbr == "秒":
            target_dt = ref_dt + datetime.timedelta(seconds=number)
        elif unit_abbr == "分":
            target_dt = ref_dt + datetime.timedelta(minutes=number)
        elif unit_abbr in ("小", "钟"):
            target_dt = ref_dt + datetime.timedelta(hours=number)
        else:
            return None

        result.imply(CivilTimeComponent.YEAR, target_dt.year)
        result.imply(CivilTimeComponent.MONTH, target_dt.month)
        result.imply(CivilTimeComponent.DAY, target_dt.day)
        result.assign(CivilTimeComponent.HOUR, target_dt.hour)
        result.assign(CivilTimeComponent.MINUTE, target_dt.minute)
        result.assign(CivilTimeComponent.SECOND, target_dt.second)
        return result
