import re
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import ParsedResult, ParsedRangeResult


class MergeWeekdayComponentRefiner(AbstractMergingRefiner):
    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        current_moment = current_result.moment
        next_moment = next_result.moment

        if not (isinstance(current_moment, ParsingCivilTimeMoment) and isinstance(next_moment, ParsingCivilTimeMoment)):
            return False

        weekday_then_normal_date = (
            current_moment.is_only_weekday_component()
            and not current_moment.is_certain(CivilTimeComponent.HOUR)
            and next_moment.is_certain(CivilTimeComponent.DAY)
        )

        return weekday_then_normal_date and re.match(r"^,?\s*$", text_between) is not None

    def merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        new_start = next_result.moment.clone()
        new_start.assign(CivilTimeComponent.WEEKDAY, current_result.moment.get(CivilTimeComponent.WEEKDAY))

        new_end = None
        if isinstance(next_result, ParsedRangeResult):
            new_end = next_result.end.clone()
            new_end.assign(CivilTimeComponent.WEEKDAY, current_result.moment.get(CivilTimeComponent.WEEKDAY))

        text = current_result.text + text_between + next_result.text

        if new_end is not None:
            return ParsedRangeResult(index=current_result.index, text=text, moment=new_start, end=new_end)
        return ParsedResult(index=current_result.index, text=text, moment=new_start)
