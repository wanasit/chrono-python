import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment
from chrono_python.utils.re import Match

FIRST_REG_PATTERN = re.compile(
    r"(^|\s|T)"
    r"(?:(?:[àa]|de)\s*)?"
    r"(\d{1,4})"
    r"(?:h|:|min|m|\.)?"
    r"(?:\s*(\d{1,2})(?:m|min|:|s|\.)?)?"
    r"(?:\s*(\d{1,2})s?)?"
    r"(?:\s*(a\.m\.|p\.m\.|am?|pm?|mp))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)

SECOND_REG_PATTERN = re.compile(
    r"^\s*(\-|\–|\~|\〜|[àa]|\?)\s*"
    r"(\d{1,4})"
    r"(?:h|:|min|m|\.)?"
    r"(?:\s*(\d{1,2})(?:m|min|:|s|\.)?)?"
    r"(?:\s*(\d{1,2})s?)?"
    r"(?:\s*(a\.m\.|p\.m\.|am?|pm?|mp))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class FRTimeExprParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return FIRST_REG_PATTERN

    def extract(
        self, context: chrono.ParsingContext, match: Match
    ) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1) or ""
        match_text = match.group(0)[len(prefix):]

        # Ignore 4-digit numbers like "2020" without time indicators
        if re.match(r"^\s*\d{4}\s*$", match_text) and not re.search(r"[hH]", match_text):
            return None

        start_moment = self._extract_time_component(context, match, is_following=False)
        if start_moment is None:
            return None

        index = match.start() + len(prefix)
        end_index = match.end()

        remaining_text = context.text[end_index:]
        second_match = SECOND_REG_PATTERN.search(remaining_text)

        if second_match and second_match.start() == 0:
            following_match_obj = Match.from_re_match(second_match)
            end_moment = self._extract_time_component(
                context, following_match_obj, is_following=True, start_moment=start_moment
            )
            if end_moment is not None:
                # Handle range meridiem adjustment (e.g. "1-3pm")
                start_ampm = match.group(5)
                end_ampm = following_match_obj.group(5)
                if not start_ampm and end_ampm:
                    if "p" in end_ampm.lower() or "m" in end_ampm.lower():
                        start_h = start_moment.get(CivilTimeComponent.HOUR)
                        if start_h is not None and start_h < 12:
                            start_moment.assign(CivilTimeComponent.HOUR, start_h + 12)
                            start_moment.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)

                full_end_index = end_index + len(second_match.group(0))
                return context.create_parsed_result(
                    index, full_end_index, start=start_moment, end=end_moment
                )

        return context.create_parsed_result(index, end_index, start_moment)

    def _extract_time_component(
        self,
        context: chrono.ParsingContext,
        match: Match,
        is_following: bool = False,
        start_moment: ParsingCivilTimeMoment | None = None,
    ) -> ParsingCivilTimeMoment | None:
        hour_str = match.group(2)
        if hour_str is None:
            return None

        minute_str = match.group(3)
        second_str = match.group(4)
        ampm_str = match.group(5)
        raw_match_text = match.group(0)

        has_h = bool(re.search(r"[hH]", raw_match_text))

        hour = int(hour_str)
        minute = 0
        has_minute = False

        if minute_str is not None:
            minute = int(minute_str)
            has_minute = True
        elif len(hour_str) in (3, 4) and not has_h:
            minute = hour % 100
            hour = hour // 100
            has_minute = True
        elif has_h:
            minute = 0
            has_minute = True

        if minute >= 60 or hour > 24:
            return None

        # Check impossibility like "13.12 PM"
        if hour > 12 and ampm_str is not None:
            return None

        meridiem = None

        if ampm_str is not None:
            ampm_lower = ampm_str.lower()
            if "p" in ampm_lower or ampm_lower in ("pm", "mp", "p.m."):
                meridiem = Meridiem.PM
                if hour != 12:
                    hour += 12
            elif "a" in ampm_lower or ampm_lower in ("am", "a.m."):
                meridiem = Meridiem.AM
                if hour == 12:
                    hour = 0
        else:
            if hour >= 12:
                meridiem = Meridiem.PM
            else:
                meridiem = None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.HOUR, hour)

        if has_minute:
            moment.assign(CivilTimeComponent.MINUTE, minute)
        else:
            moment.imply(CivilTimeComponent.MINUTE, 0)

        if second_str is not None:
            second = int(second_str)
            if second >= 60:
                return None
            moment.assign(CivilTimeComponent.SECOND, second)
        else:
            moment.imply(CivilTimeComponent.SECOND, 0)

        moment.imply(CivilTimeComponent.MILLI_SECOND, 0)

        if meridiem is not None:
            moment.assign(CivilTimeComponent.MERIDIEM, meridiem)
        else:
            if hour < 12:
                moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            else:
                moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

        # Handle following moment relative to start_moment (e.g. 11pm-2 -> 2am next day)
        if is_following and start_moment is not None:
            start_dt = start_moment.datetime()
            fol_dt = moment.datetime()
            if fol_dt < start_dt:
                ref_dt = context.reference.datetime()
                try:
                    next_day = ref_dt.date() + datetime.timedelta(days=1)
                    moment.imply(CivilTimeComponent.DAY, next_day.day)
                    moment.imply(CivilTimeComponent.MONTH, next_day.month)
                    moment.imply(CivilTimeComponent.YEAR, next_day.year)
                except ValueError:
                    pass

        return moment
