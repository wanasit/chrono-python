import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.locales.zh.hans.constants import NUMBER, zh_string_to_number


class ZHHansTimeExpressionParser(chrono.Parser):
    def __init__(self):
        num_chars = "".join(NUMBER.keys())
        date_pattern = (
            rf"(?:"
            rf"(今|明|前|大前|后|大后|昨)(早|朝|晚)|"
            rf"(上(?:午)|早(?:上)|下(?:午)|晚(?:上)|夜(?:晚)?|中(?:午)|凌(?:晨))|"
            rf"(今|明|前|大前|后|大后|昨)(?:日|天)"
            rf"(?:[\s,，]*)"
            rf"(?:(上(?:午)|早(?:上)|下(?:午)|晚(?:上)|夜(?:晚)?|中(?:午)|凌(?:晨)))?"
            rf")?"
        )
        time_pattern = (
            rf"(?:(\d+|[{num_chars}]+)(?:\s*)(?:点|时|:|：)"
            rf"(?:\s*)"
            rf"(\d+|半|正|整|[{num_chars}]+)?(?:\s*)(?:分|:|：)?"
            rf"(?:\s*)"
            rf"(\d+|[{num_chars}]+)?(?:\s*)(?:秒)?)"
            rf"(?:\s*(A\.M\.|P\.M\.|AM?|PM?))?"
        )

        self._first_pattern = re.compile(
            rf"(?:从|自)?{date_pattern}(?:[\s,，]*){time_pattern}",
            re.IGNORECASE,
        )
        self._second_pattern = re.compile(
            rf"^(?:\s*(?:到|至|\-|\–|\~|\〜)\s*){date_pattern}(?:[\s,，]*){time_pattern}",
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._first_pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        start_index = match.start()
        text = match.group(0)

        # ASCII word boundary check preceding match (e.g. 112 AM vs 12 AM)
        if start_index > 0 and re.match(r"[a-zA-Z0-9]", context.text[start_index - 1]):
            return None

        ref_dt = context.reference.datetime()
        start_moment = ParsingCivilTimeMoment.of(context.reference)
        start_dt = datetime.datetime(ref_dt.year, ref_dt.month, ref_dt.day, ref_dt.hour, ref_dt.minute, ref_dt.second, ref_dt.microsecond, tzinfo=ref_dt.tzinfo)

        day_g1 = match.group(1)
        zh_ampm_g1 = match.group(2)
        zh_ampm_g2 = match.group(3)
        day_g3 = match.group(4)
        zh_ampm_g3 = match.group(5)
        hour_str = match.group(6)
        min_str = match.group(7)
        sec_str = match.group(8)
        ampm_str = match.group(9)

        # Handle Date Component for Start
        if day_g1:
            if day_g1 == "明":
                if ref_dt.hour > 1:
                    start_dt += datetime.timedelta(days=1)
            elif day_g1 == "昨":
                start_dt -= datetime.timedelta(days=1)
            elif day_g1 == "前":
                start_dt -= datetime.timedelta(days=2)
            elif day_g1 == "大前":
                start_dt -= datetime.timedelta(days=3)
            elif day_g1 == "后":
                start_dt += datetime.timedelta(days=2)
            elif day_g1 == "大后":
                start_dt += datetime.timedelta(days=3)
            start_moment.assign(CivilTimeComponent.DAY, start_dt.day)
            start_moment.assign(CivilTimeComponent.MONTH, start_dt.month)
            start_moment.assign(CivilTimeComponent.YEAR, start_dt.year)
        elif day_g3:
            if day_g3 == "明":
                start_dt += datetime.timedelta(days=1)
            elif day_g3 == "昨":
                start_dt -= datetime.timedelta(days=1)
            elif day_g3 == "前":
                start_dt -= datetime.timedelta(days=2)
            elif day_g3 == "大前":
                start_dt -= datetime.timedelta(days=3)
            elif day_g3 == "后":
                start_dt += datetime.timedelta(days=2)
            elif day_g3 == "大后":
                start_dt += datetime.timedelta(days=3)
            start_moment.assign(CivilTimeComponent.DAY, start_dt.day)
            start_moment.assign(CivilTimeComponent.MONTH, start_dt.month)
            start_moment.assign(CivilTimeComponent.YEAR, start_dt.year)
        else:
            start_moment.imply(CivilTimeComponent.DAY, start_dt.day)
            start_moment.imply(CivilTimeComponent.MONTH, start_dt.month)
            start_moment.imply(CivilTimeComponent.YEAR, start_dt.year)

        # Handle Seconds
        if sec_str:
            sec = int(sec_str) if sec_str.isdigit() else zh_string_to_number(sec_str)
            if sec >= 60:
                return None
            start_moment.assign(CivilTimeComponent.SECOND, sec)
        else:
            start_moment.imply(CivilTimeComponent.SECOND, 0)

        start_moment.imply(CivilTimeComponent.MILLI_SECOND, 0)

        # Handle Hour
        hour = int(hour_str) if hour_str.isdigit() else zh_string_to_number(hour_str)

        # Handle Minute
        minute = 0
        if min_str:
            if min_str == "半":
                minute = 30
            elif min_str in ("正", "整"):
                minute = 0
            else:
                minute = int(min_str) if min_str.isdigit() else zh_string_to_number(min_str)
        elif hour > 100:
            minute = hour % 100
            hour = hour // 100

        if minute >= 60 or hour > 24:
            return None

        meridiem = -1
        if hour >= 12:
            meridiem = 1

        # Handle AM / PM for Start
        if ampm_str:
            if hour > 12:
                return None
            ampm_char = ampm_str[0].lower()
            if ampm_char == "a":
                meridiem = 0
                if hour == 12:
                    hour = 0
            elif ampm_char == "p":
                meridiem = 1
                if hour != 12:
                    hour += 12
        elif zh_ampm_g1:
            zh_char = zh_ampm_g1[0]
            if zh_char in ("早", "朝"):
                meridiem = 0
                if hour == 12:
                    hour = 0
            elif zh_char == "晚":
                meridiem = 1
                if hour != 12:
                    hour += 12
        elif zh_ampm_g2:
            zh_char = zh_ampm_g2[0]
            if zh_char in ("上", "早", "凌"):
                meridiem = 0
                if hour == 12:
                    hour = 0
            elif zh_char in ("下", "晚"):
                meridiem = 1
                if hour != 12:
                    hour += 12
        elif zh_ampm_g3:
            zh_char = zh_ampm_g3[0]
            if zh_char in ("上", "早", "凌"):
                meridiem = 0
                if hour == 12:
                    hour = 0
            elif zh_char in ("下", "晚"):
                meridiem = 1
                if hour != 12:
                    hour += 12

        start_moment.assign(CivilTimeComponent.HOUR, hour)
        start_moment.assign(CivilTimeComponent.MINUTE, minute)

        if meridiem >= 0:
            start_moment.assign(CivilTimeComponent.MERIDIEM, meridiem)
        else:
            if hour < 12:
                start_moment.imply(CivilTimeComponent.MERIDIEM, 0)
            else:
                start_moment.imply(CivilTimeComponent.MERIDIEM, 1)

        # Check for range expression (SECOND_REG_PATTERN)
        remaining_text = context.text[start_index + len(text):]
        second_match = self._second_pattern.search(remaining_text)

        if not second_match:
            if text.isdigit():
                return None
            return context.create_parsed_result(start_index, start_index + len(text), start_moment)

        # Parse End Moment for range
        second_text = second_match.group(0)
        end_moment = ParsingCivilTimeMoment.of(context.reference)
        end_dt = datetime.datetime(start_dt.year, start_dt.month, start_dt.day, start_dt.hour, start_dt.minute, start_dt.second, start_dt.microsecond, tzinfo=start_dt.tzinfo)

        end_day_g1 = second_match.group(1)
        end_zh_ampm_g1 = second_match.group(2)
        end_zh_ampm_g2 = second_match.group(3)
        end_day_g3 = second_match.group(4)
        end_zh_ampm_g3 = second_match.group(5)
        end_hour_str = second_match.group(6)
        end_min_str = second_match.group(7)
        end_sec_str = second_match.group(8)
        end_ampm_str = second_match.group(9)

        if end_day_g1 or end_day_g3:
            end_dt = datetime.datetime(ref_dt.year, ref_dt.month, ref_dt.day, ref_dt.hour, ref_dt.minute, ref_dt.second, ref_dt.microsecond, tzinfo=ref_dt.tzinfo)

        if end_day_g1:
            if end_day_g1 == "明":
                if ref_dt.hour > 1:
                    end_dt += datetime.timedelta(days=1)
            elif end_day_g1 == "昨":
                end_dt -= datetime.timedelta(days=1)
            elif end_day_g1 == "前":
                end_dt -= datetime.timedelta(days=2)
            elif end_day_g1 == "大前":
                end_dt -= datetime.timedelta(days=3)
            elif end_day_g1 == "后":
                end_dt += datetime.timedelta(days=2)
            elif end_day_g1 == "大后":
                end_dt += datetime.timedelta(days=3)
            end_moment.assign(CivilTimeComponent.DAY, end_dt.day)
            end_moment.assign(CivilTimeComponent.MONTH, end_dt.month)
            end_moment.assign(CivilTimeComponent.YEAR, end_dt.year)
        elif end_day_g3:
            if end_day_g3 == "明":
                end_dt += datetime.timedelta(days=1)
            elif end_day_g3 == "昨":
                end_dt -= datetime.timedelta(days=1)
            elif end_day_g3 == "前":
                end_dt -= datetime.timedelta(days=2)
            elif end_day_g3 == "大前":
                end_dt -= datetime.timedelta(days=3)
            elif end_day_g3 == "后":
                end_dt += datetime.timedelta(days=2)
            elif end_day_g3 == "大后":
                end_dt += datetime.timedelta(days=3)
            end_moment.assign(CivilTimeComponent.DAY, end_dt.day)
            end_moment.assign(CivilTimeComponent.MONTH, end_dt.month)
            end_moment.assign(CivilTimeComponent.YEAR, end_dt.year)
        else:
            end_moment.imply(CivilTimeComponent.DAY, end_dt.day)
            end_moment.imply(CivilTimeComponent.MONTH, end_dt.month)
            end_moment.imply(CivilTimeComponent.YEAR, end_dt.year)

        if end_sec_str:
            end_sec = int(end_sec_str) if end_sec_str.isdigit() else zh_string_to_number(end_sec_str)
            if end_sec >= 60:
                return None
            end_moment.assign(CivilTimeComponent.SECOND, end_sec)
        else:
            end_moment.imply(CivilTimeComponent.SECOND, 0)

        end_moment.imply(CivilTimeComponent.MILLI_SECOND, 0)

        end_hour = int(end_hour_str) if end_hour_str.isdigit() else zh_string_to_number(end_hour_str)
        end_minute = 0
        if end_min_str:
            if end_min_str == "半":
                end_minute = 30
            elif end_min_str in ("正", "整"):
                end_minute = 0
            else:
                end_minute = int(end_min_str) if end_min_str.isdigit() else zh_string_to_number(end_min_str)
        elif end_hour > 100:
            end_minute = end_hour % 100
            end_hour = end_hour // 100

        if end_minute >= 60 or end_hour > 24:
            return None

        end_meridiem = -1
        if end_hour >= 12:
            end_meridiem = 1

        if end_ampm_str:
            if end_hour > 12:
                return None
            ampm_char = end_ampm_str[0].lower()
            if ampm_char == "a":
                end_meridiem = 0
                if end_hour == 12:
                    end_hour = 0
            elif ampm_char == "p":
                end_meridiem = 1
                if end_hour != 12:
                    end_hour += 12

            if not start_moment.is_certain(CivilTimeComponent.MERIDIEM):
                if end_meridiem == 0:
                    start_moment.imply(CivilTimeComponent.MERIDIEM, 0)
                    if start_moment.get(CivilTimeComponent.HOUR) == 12:
                        start_moment.assign(CivilTimeComponent.HOUR, 0)
                else:
                    start_moment.imply(CivilTimeComponent.MERIDIEM, 1)
                    if start_moment.get(CivilTimeComponent.HOUR) != 12:
                        start_moment.assign(CivilTimeComponent.HOUR, start_moment.get(CivilTimeComponent.HOUR) + 12)

        elif end_zh_ampm_g1:
            zh_char = end_zh_ampm_g1[0]
            if zh_char in ("早", "朝"):
                end_meridiem = 0
                if end_hour == 12:
                    end_hour = 0
            elif zh_char == "晚":
                end_meridiem = 1
                if end_hour != 12:
                    end_hour += 12
        elif end_zh_ampm_g2:
            zh_char = end_zh_ampm_g2[0]
            if zh_char in ("上", "早", "凌"):
                end_meridiem = 0
                if end_hour == 12:
                    end_hour = 0
            elif zh_char in ("下", "晚"):
                end_meridiem = 1
                if end_hour != 12:
                    end_hour += 12
        elif end_zh_ampm_g3:
            zh_char = end_zh_ampm_g3[0]
            if zh_char in ("上", "早", "凌"):
                end_meridiem = 0
                if end_hour == 12:
                    end_hour = 0
            elif zh_char in ("下", "晚"):
                end_meridiem = 1
                if end_hour != 12:
                    end_hour += 12

        end_moment.assign(CivilTimeComponent.HOUR, end_hour)
        end_moment.assign(CivilTimeComponent.MINUTE, end_minute)

        if end_meridiem >= 0:
            end_moment.assign(CivilTimeComponent.MERIDIEM, end_meridiem)
        else:
            start_at_pm = start_moment.is_certain(CivilTimeComponent.MERIDIEM) and start_moment.get(CivilTimeComponent.MERIDIEM) == 1
            if start_at_pm and start_moment.get(CivilTimeComponent.HOUR) > end_hour:
                end_moment.imply(CivilTimeComponent.MERIDIEM, 0)
            elif end_hour > 12:
                end_moment.imply(CivilTimeComponent.MERIDIEM, 1)

        start_dt_calc = start_moment.datetime()
        end_dt_calc = end_moment.datetime()
        if end_dt_calc < start_dt_calc:
            end_dt_calc += datetime.timedelta(days=1)
            end_moment.assign(CivilTimeComponent.DAY, end_dt_calc.day)
            end_moment.assign(CivilTimeComponent.MONTH, end_dt_calc.month)
            end_moment.assign(CivilTimeComponent.YEAR, end_dt_calc.year)

        full_text = text + second_text
        return context.create_parsed_result(start_index, start_index + len(full_text), start_moment, end_moment)
