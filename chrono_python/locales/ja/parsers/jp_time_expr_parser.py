import re
import datetime

from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.locales.ja.constants import NUMBER, ja_string_to_number, to_hankaku

KJS = "".join(NUMBER.keys())

FIRST_REG_PATTERN = re.compile(
    r"(?:"
    r"(午前|午後|A.M\.|P\.M\.|AM|PM)"
    r")?"
    r"(?:[\s,，、]*)"
    r"(?:"
    r"([0-9０-９]+|[" + KJS + r"]+)(?:\s*)(?:時(?!間)|:|：)"
    r"(?:\s*)"
    r"([0-9０-９]+|半|[" + KJS + r"]+)?(?:\s*)(?:分|:|：)?"
    r"(?:\s*)"
    r"([0-9０-９]+|[" + KJS + r"]+)?(?:\s*)(?:秒)?)"
    r"(?:\s*(A\.M\.|P\.M\.|AM?|PM?))?",
    re.IGNORECASE
)

SECOND_REG_PATTERN = re.compile(
    r"(?:^\s*(?:から|\-|–|－|~|〜)\s*)"
    r"(?:"
    r"(午前|午後|A.M\.|P\.M\.|AM|PM)"
    r")?"
    r"(?:[\s,，、]*)"
    r"(?:"
    r"([0-9０-９]+|[" + KJS + r"]+)(?:\s*)(?:時|:|：)"
    r"(?:\s*)"
    r"([0-9０-９]+|半|[" + KJS + r"]+)?(?:\s*)(?:分|:|：)?"
    r"(?:\s*)"
    r"([0-9０-９]+|[" + KJS + r"]+)?(?:\s*)(?:秒)?)"
    r"(?:\s*(A\.M\.|P\.M\.|AM?|PM?))?",
    re.IGNORECASE
)

AM_PM_HOUR_GROUP_1 = 1
HOUR_GROUP = 2
MINUTE_GROUP = 3
SECOND_GROUP = 4
AM_PM_HOUR_GROUP_2 = 5


class JPTimeExprParser(AbstractParserWithWordBoundary):
    """Japanese time expression parser."""

    def left_word_boundary(self) -> str:
        # Override to match empty group so we don't consume any Japanese characters
        # as word boundaries. The ASCII boundary check is done inside inner_extract.
        return '()'

    def inner_pattern(self) -> re.Pattern:
        return FIRST_REG_PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        start_idx = match.start()
        if start_idx > 0 and re.match(r'[a-zA-Z0-9_]', context.text[start_idx - 1]):
            return None

        start_moment = create_time_components(
            context,
            match.group(HOUR_GROUP),
            match.group(MINUTE_GROUP),
            match.group(SECOND_GROUP),
            match.group(AM_PM_HOUR_GROUP_1) or match.group(AM_PM_HOUR_GROUP_2)
        )
        if start_moment is None:
            return None

        # Check for range parsing
        remaining_idx = start_idx + len(match.group(0))
        remaining_text = context.text[remaining_idx:]

        second_match = SECOND_REG_PATTERN.match(remaining_text)
        if not second_match:
            return context.create_parsed_result(start_idx, remaining_idx, start_moment)

        end_moment = create_time_components(
            context,
            second_match.group(HOUR_GROUP),
            second_match.group(MINUTE_GROUP),
            second_match.group(SECOND_GROUP),
            second_match.group(AM_PM_HOUR_GROUP_1) or second_match.group(AM_PM_HOUR_GROUP_2)
        )
        if end_moment is None:
            return None

        # Propagate meridiem
        if not end_moment.is_certain(CivilTimeComponent.MERIDIEM) and start_moment.is_certain(CivilTimeComponent.MERIDIEM):
            start_meridiem = start_moment.get(CivilTimeComponent.MERIDIEM)
            end_moment.imply(CivilTimeComponent.MERIDIEM, start_meridiem)
            if start_meridiem == Meridiem.PM:
                start_hour = start_moment.get(CivilTimeComponent.HOUR)
                end_hour = end_moment.get(CivilTimeComponent.HOUR)
                if start_hour - 12 > end_hour:
                    end_moment.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
                elif end_hour < 12:
                    end_moment.assign(CivilTimeComponent.HOUR, end_hour + 12)

        if end_moment.datetime() < start_moment.datetime():
            next_day = end_moment.datetime() + datetime.timedelta(days=1)
            end_moment.imply(CivilTimeComponent.DAY, next_day.day)
            end_moment.imply(CivilTimeComponent.MONTH, next_day.month)
            end_moment.imply(CivilTimeComponent.YEAR, next_day.year)

        total_text = match.group(0) + second_match.group(0)
        return context.create_parsed_result(start_idx, start_idx + len(total_text), start_moment, end_moment)


def create_time_components(
    context: chrono.ParsingContext,
    match_hour: str | None,
    match_minute: str | None,
    match_second: str | None,
    match_am_pm: str | None
) -> ParsingCivilTimeMoment | None:
    if match_hour is None:
        return None

    try:
        hour = int(to_hankaku(match_hour))
    except ValueError:
        hour = ja_string_to_number(match_hour)

    if hour > 24:
        return None

    target_components = ParsingCivilTimeMoment.of(context.reference)

    if match_minute is not None:
        if match_minute == "半":
            minute = 30
        else:
            try:
                minute = int(to_hankaku(match_minute))
            except ValueError:
                minute = ja_string_to_number(match_minute)
        if minute >= 60:
            return None
        target_components.assign(CivilTimeComponent.MINUTE, minute)

    if match_second is not None:
        try:
            second = int(to_hankaku(match_second))
        except ValueError:
            second = ja_string_to_number(match_second)
        if second >= 60:
            return None
        target_components.assign(CivilTimeComponent.SECOND, second)

    meridiem = None
    if match_am_pm is not None:
        if hour > 12:
            return None
        ampm_string = match_am_pm
        if ampm_string == "午前" or ampm_string[0].lower() == "a":
            meridiem = Meridiem.AM
            if hour == 12:
                hour = 0
        elif ampm_string == "午後" or ampm_string[0].lower() == "p":
            meridiem = Meridiem.PM
            if hour != 12:
                hour += 12

    target_components.assign(CivilTimeComponent.HOUR, hour)

    if meridiem is not None:
        target_components.assign(CivilTimeComponent.MERIDIEM, meridiem)
    else:
        if hour < 12:
            target_components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            target_components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)

    return target_components
