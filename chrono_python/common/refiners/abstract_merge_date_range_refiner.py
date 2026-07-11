import re
import datetime
from abc import ABC, abstractmethod
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.common.types import CivilTimeMoment, ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import ParsedResult, ParsedRangeResult


def add_duration(dt: datetime.datetime, *, day: int = 0, year: int = 0) -> datetime.datetime:
    if day != 0:
        return dt + datetime.timedelta(days=day)
    if year != 0:
        try:
            return dt.replace(year=dt.year + year)
        except ValueError:
            # Handle leap year Feb 29 to non-leap year adjustment
            return dt.replace(year=dt.year + year, day=28)
    return dt


class AbstractMergeDateRangeRefiner(AbstractMergingRefiner, ABC):
    """
    An abstract base class for merging two parsed date/time results separated by a range pattern
    (e.g., "to", "-", "until") into a single ParsedRangeResult.
    It handles logic such as component propagation, weekday/unknown year chronological alignment,
    and swapping range bounds if necessary.
    """

    @abstractmethod
    def pattern_between(self) -> re.Pattern:
        raise NotImplementedError()

    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        if isinstance(current_result, ParsedRangeResult) or isinstance(next_result, ParsedRangeResult):
            return False
        return self.pattern_between().search(text_between) is not None

    def merge_results(self, text_between: str, from_result: ParsedResult, to_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        from_moment = from_result.moment.clone() if hasattr(from_result.moment, 'clone') else from_result.moment
        to_moment = to_result.moment.clone() if hasattr(to_result.moment, 'clone') else to_result.moment

        # Merge known components to implied components if they are not weekday-only
        if isinstance(from_moment, CivilTimeMoment) and isinstance(to_moment, CivilTimeMoment):
            if not from_moment.is_only_weekday_component() and not to_moment.is_only_weekday_component():
                for key in to_moment.list(only_certain=True):
                    if not from_moment.is_certain(key):
                        from_moment.imply(key, to_moment.get(key))
                for key in from_moment.list(only_certain=True):
                    if not to_moment.is_certain(key):
                        to_moment.imply(key, from_moment.get(key))

        if from_moment.datetime() > to_moment.datetime():
            from_date = from_moment.datetime()
            to_date = to_moment.datetime()

            if isinstance(to_moment, CivilTimeMoment) and to_moment.is_only_weekday_component() and add_duration(to_date, day=7) > from_date:
                to_date = add_duration(to_date, day=7)
                to_moment.imply(CivilTimeComponent.DAY, to_date.day)
                to_moment.imply(CivilTimeComponent.MONTH, to_date.month)
                to_moment.imply(CivilTimeComponent.YEAR, to_date.year)
            elif isinstance(from_moment, CivilTimeMoment) and from_moment.is_only_weekday_component() and add_duration(from_date, day=-7) < to_date:
                from_date = add_duration(from_date, day=-7)
                from_moment.imply(CivilTimeComponent.DAY, from_date.day)
                from_moment.imply(CivilTimeComponent.MONTH, from_date.month)
                from_moment.imply(CivilTimeComponent.YEAR, from_date.year)
            elif isinstance(to_moment, CivilTimeMoment) and to_moment.is_date_with_unknown_year() and add_duration(to_date, year=1) > from_date:
                to_date = add_duration(to_date, year=1)
                to_moment.imply(CivilTimeComponent.YEAR, to_date.year)
            elif isinstance(from_moment, CivilTimeMoment) and from_moment.is_date_with_unknown_year() and add_duration(from_date, year=-1) < to_date:
                from_date = add_duration(from_date, year=-1)
                from_moment.imply(CivilTimeComponent.YEAR, from_date.year)
            else:
                # Swap them
                from_result, to_result = to_result, from_result
                from_moment, to_moment = to_moment, from_moment

        index = min(from_result.index, to_result.index)
        if from_result.index < to_result.index:
            text = from_result.text + text_between + to_result.text
        else:
            text = to_result.text + text_between + from_result.text

        return ParsedRangeResult(index=index, text=text, moment=from_moment, end=to_moment)
