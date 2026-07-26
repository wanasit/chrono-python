import re
import datetime
from abc import ABC, abstractmethod

from chrono_python import chrono
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.common.types import CivilTimeMoment, ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import ParsedResult, ParsedRangeResult


def assign_similar_date(component: ParsingCivilTimeMoment, target: datetime.datetime):
    component.assign_similar_date(target)


def imply_similar_date(component: ParsingCivilTimeMoment, target: datetime.datetime):
    component.imply_similar_date(target)


def merge_date_time_component(
    date_component: ParsingCivilTimeMoment,
    time_component: ParsingCivilTimeMoment
) -> ParsingCivilTimeMoment:
    dateTimeComponent = date_component.clone()

    if time_component.is_certain(CivilTimeComponent.HOUR):
        dateTimeComponent.assign(CivilTimeComponent.HOUR, time_component.get(CivilTimeComponent.HOUR))
        dateTimeComponent.assign(CivilTimeComponent.MINUTE, time_component.get(CivilTimeComponent.MINUTE))

        if time_component.is_certain(CivilTimeComponent.SECOND):
            dateTimeComponent.assign(CivilTimeComponent.SECOND, time_component.get(CivilTimeComponent.SECOND))

            if time_component.is_certain(CivilTimeComponent.MILLI_SECOND):
                dateTimeComponent.assign(CivilTimeComponent.MILLI_SECOND, time_component.get(CivilTimeComponent.MILLI_SECOND))
            else:
                val = time_component.get(CivilTimeComponent.MILLI_SECOND)
                dateTimeComponent.imply(CivilTimeComponent.MILLI_SECOND, val if val is not None else 0)
        else:
            val_sec = time_component.get(CivilTimeComponent.SECOND)
            dateTimeComponent.imply(CivilTimeComponent.SECOND, val_sec if val_sec is not None else 0)
            val_ms = time_component.get(CivilTimeComponent.MILLI_SECOND)
            dateTimeComponent.imply(CivilTimeComponent.MILLI_SECOND, val_ms if val_ms is not None else 0)
    else:
        val_hr = time_component.get(CivilTimeComponent.HOUR)
        dateTimeComponent.imply(CivilTimeComponent.HOUR, val_hr if val_hr is not None else 0)
        val_min = time_component.get(CivilTimeComponent.MINUTE)
        dateTimeComponent.imply(CivilTimeComponent.MINUTE, val_min if val_min is not None else 0)
        val_sec = time_component.get(CivilTimeComponent.SECOND)
        dateTimeComponent.imply(CivilTimeComponent.SECOND, val_sec if val_sec is not None else 0)
        val_ms = time_component.get(CivilTimeComponent.MILLI_SECOND)
        dateTimeComponent.imply(CivilTimeComponent.MILLI_SECOND, val_ms if val_ms is not None else 0)

    if time_component.is_certain(CivilTimeComponent.TIMEZONE_OFFSET):
        dateTimeComponent.assign(CivilTimeComponent.TIMEZONE_OFFSET, time_component.get(CivilTimeComponent.TIMEZONE_OFFSET))

    date_has_meaningful_meridiem = date_component.get(CivilTimeComponent.MERIDIEM) is not None

    if time_component.is_certain(CivilTimeComponent.MERIDIEM):
        dateTimeComponent.assign(CivilTimeComponent.MERIDIEM, time_component.get(CivilTimeComponent.MERIDIEM))
    elif time_component.get(CivilTimeComponent.MERIDIEM) is not None and not date_has_meaningful_meridiem:
        dateTimeComponent.imply(CivilTimeComponent.MERIDIEM, time_component.get(CivilTimeComponent.MERIDIEM))

    if dateTimeComponent.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM and dateTimeComponent.get(CivilTimeComponent.HOUR) < 12:
        if time_component.is_certain(CivilTimeComponent.HOUR):
            dateTimeComponent.assign(CivilTimeComponent.HOUR, dateTimeComponent.get(CivilTimeComponent.HOUR) + 12)
        else:
            dateTimeComponent.imply(CivilTimeComponent.HOUR, dateTimeComponent.get(CivilTimeComponent.HOUR) + 12)

    return dateTimeComponent


def merge_date_time_result(date_result: ParsedResult, time_result: ParsedResult) -> ParsedResult:
    start_date = date_result.moment
    start_time = time_result.moment

    if isinstance(start_date, CivilTimeMoment) and isinstance(start_time, CivilTimeMoment):
        merged_start = merge_date_time_component(start_date, start_time)
    else:
        merged_start = start_date

    merged_end = None
    if isinstance(date_result, ParsedRangeResult) or isinstance(time_result, ParsedRangeResult):
        end_date = date_result.end if isinstance(date_result, ParsedRangeResult) else date_result.moment
        end_time = time_result.end if isinstance(time_result, ParsedRangeResult) else time_result.moment

        if isinstance(end_date, CivilTimeMoment) and isinstance(end_time, CivilTimeMoment):
            merged_end = merge_date_time_component(end_date, end_time)

            if not isinstance(date_result, ParsedRangeResult) and merged_end.datetime() < merged_start.datetime():
                next_day = merged_end.datetime() + datetime.timedelta(days=1)
                if merged_end.is_certain(CivilTimeComponent.DAY):
                    assign_similar_date(merged_end, next_day)
                else:
                    imply_similar_date(merged_end, next_day)
        else:
            merged_end = end_date

    if merged_end is not None:
        return ParsedRangeResult(index=date_result.index, text=date_result.text, moment=merged_start, end=merged_end)
    return ParsedResult(index=date_result.index, text=date_result.text, moment=merged_start)


class AbstractMergeDateTimeRefiner(AbstractMergingRefiner, ABC):
    """
    An abstract base class for merging a parsed date result and a parsed time result
    separated by a configured pattern (e.g., "at", "on", ",", etc.).
    """

    @abstractmethod
    def pattern_between(self) -> re.Pattern:
        raise NotImplementedError()

    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        curr_moment = current_result.moment
        next_moment = next_result.moment
        if not isinstance(curr_moment, CivilTimeMoment) or not isinstance(next_moment, CivilTimeMoment):
            return False

        has_date_time = (curr_moment.is_only_date() and next_moment.is_only_time()) or (next_moment.is_only_date() and curr_moment.is_only_time())
        return has_date_time and self.pattern_between().search(text_between) is not None

    def merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        curr_moment = current_result.moment

        if curr_moment.is_only_date():
            result = merge_date_time_result(current_result, next_result)
        else:
            result = merge_date_time_result(next_result, current_result)

        new_text = current_result.text + text_between + next_result.text
        if isinstance(result, ParsedRangeResult):
            return ParsedRangeResult(index=current_result.index, text=new_text, moment=result.moment, end=result.end)
        return ParsedResult(index=current_result.index, text=new_text, moment=result.moment)
