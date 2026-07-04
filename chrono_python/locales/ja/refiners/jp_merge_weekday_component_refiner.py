import re
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import ParsedResult, ParsedRangeResult


class JPMergeWeekdayComponentRefiner(AbstractMergingRefiner):
    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        current_moment = current_result.moment
        next_moment = next_result.moment

        if not (isinstance(current_moment, ParsingCivilTimeMoment) and isinstance(next_moment, ParsingCivilTimeMoment)):
            return False

        normal_date_then_weekday = (
            current_moment.is_certain(CivilTimeComponent.DAY)
            and next_moment.is_only_weekday_component()
            and not next_moment.is_certain(CivilTimeComponent.HOUR)
        )

        return normal_date_then_weekday and re.match(r"^[,、の]?\s*$", text_between) is not None

    def merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        new_start = current_result.moment.clone()
        new_start.assign(CivilTimeComponent.WEEKDAY, next_result.moment.get(CivilTimeComponent.WEEKDAY))

        new_end = None
        if isinstance(current_result, ParsedRangeResult):
            new_end = current_result.end.clone()
            new_end.assign(CivilTimeComponent.WEEKDAY, next_result.moment.get(CivilTimeComponent.WEEKDAY))

        text = current_result.text + text_between + next_result.text

        if new_end is not None:
            return ParsedRangeResult(index=current_result.index, text=text, moment=new_start, end=new_end)
        return ParsedResult(index=current_result.index, text=text, moment=new_start)
