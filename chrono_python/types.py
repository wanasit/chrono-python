import datetime
import re
from abc import abstractmethod, ABC
from enum import Enum


class DateTimeComponent(Enum):
    YEAR = 'year'
    MONTH = 'month'
    WEEKDAY = 'weekday'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLI_SECOND = 'millisecond'
    TIMEZONE_OFFSET = 'timezone_offset'


class DateTimeUnit(Enum):
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    WEEK = 'week'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLI_SECOND = 'millisecond'


class DateTimePrecision(Enum):
    YEAR = 10
    MONTH = 20
    WEEK = 30
    DAY = 40
    HOUR = 50
    MINUTE = 60
    SECOND = 70
    MILLI_SECOND = 80


class Moment(ABC):
    """An abstract class represents a moment or time at certain precision."""

    @abstractmethod
    def datetime(self) -> datetime.datetime:
        raise NotImplementedError()

    @abstractmethod
    def precision(self) -> DateTimePrecision:
        raise NotImplementedError()


class DateTimeMoment(Moment):
    """A typical implementation of `Moment` based-on `datetime.datetime`."""

    def __init__(self, dt: datetime.datetime, precision: DateTimePrecision):
        self._dt = dt
        self._precision = precision

    @staticmethod
    def of(reference: datetime.datetime,
           precision: DateTimePrecision = DateTimePrecision.MILLI_SECOND) -> 'DateTimeMoment':
        return DateTimeMoment(reference, precision)

    @staticmethod
    def now():
        return DateTimeMoment(datetime.datetime.now(), DateTimePrecision.MILLI_SECOND)

    def datetime(self) -> datetime.datetime:
        return self._dt

    def precision(self) -> DateTimePrecision:
        return self._precision


class ReferenceMoment(Moment):

    def __init__(self, reference: Moment, delta: dict[DateTimeUnit, int]):
        self._reference = reference
        self._delta = delta

    def datetime(self) -> datetime.datetime:
        ref_datetime = self._reference.datetime()

        target_month = ref_datetime.month + self._delta.get(DateTimeUnit.MONTH, 0)
        adjusted_year = ref_datetime.year + self._delta.get(DateTimeUnit.YEAR, 0) + target_month // 12
        adjusted_month = target_month % 12

        adjusted_datetime = ref_datetime.replace(
            year=adjusted_year,
            month=adjusted_month,
        )
        return adjusted_datetime + datetime.timedelta(
            days=self._delta.get(DateTimeUnit.DAY, 0) + self._delta.get(DateTimeUnit.WEEK, 0) * 7,
            hours=self._delta.get(DateTimeUnit.HOUR, 0),
            minutes=self._delta.get(DateTimeUnit.MINUTE, 0),
            seconds=self._delta.get(DateTimeUnit.SECOND, 0),
            milliseconds=self._delta.get(DateTimeUnit.MILLI_SECOND, 0)
        )

    def precision(self) -> DateTimePrecision:
        ref_precision = self._reference.precision()
        if DateTimeUnit.MILLI_SECOND in self._delta and ref_precision >= DateTimePrecision.MILLI_SECOND:
            return DateTimePrecision.MILLI_SECOND
        if DateTimeUnit.SECOND in self._delta and ref_precision >= DateTimePrecision.SECOND:
            return DateTimePrecision.SECOND
        if DateTimeUnit.MINUTE in self._delta and ref_precision >= DateTimePrecision.MINUTE:
            return DateTimePrecision.MINUTE
        if DateTimeUnit.HOUR in self._delta and ref_precision >= DateTimePrecision.HOUR:
            return DateTimePrecision.HOUR
        if DateTimeUnit.DAY in self._delta and ref_precision >= DateTimePrecision.DAY:
            return DateTimePrecision.DAY
        if DateTimeUnit.WEEK in self._delta and ref_precision >= DateTimePrecision.WEEK:
            return DateTimePrecision.WEEK
        if DateTimeUnit.MONTH in self._delta and ref_precision >= DateTimePrecision.MONTH:
            return DateTimePrecision.MONTH
        if DateTimeUnit.YEAR in self._delta and ref_precision >= DateTimePrecision.YEAR:
            return DateTimePrecision.YEAR
        return ref_precision


class Match:
    """A class represents the result of a regular expression match.

    Chrono uses this class internally instead of `re.Match` to enable modifying or augmenting the result.
    Each method in this class follow the re.Match's method of the same name.

    Ref: https://docs.python.org/3/library/re.html#match-objects
    """

    def __init__(self, string: str,
                 group_spans: list[tuple[int, int]],
                 group_name_to_index: dict[str, int]):
        self._string = string
        self._group_spans = group_spans
        self._group_name_to_index = group_name_to_index

    @staticmethod
    def from_re_match(match: re.Match) -> 'Match':
        group_spans = [match.span(i) for i in range(match.re.groups + 1)]
        group_name_to_index = {name: i for name, i in match.re.groupindex.items()}
        return Match(match.string, group_spans, group_name_to_index)

    @property
    def string(self) -> str:
        return self._string

    def __getitem__(self, item):
        return self.group(item)

    def group(self, index: int | str) -> str | None:
        if isinstance(index, str):
            index = self._group_name_to_index[index]
        if index < 0 or index >= len(self._group_spans):
            raise IndexError(f'Group index {index} out of range')

        span = self._group_spans[index]
        if span == (-1, -1):
            return None

        return self._string[span[0]:span[1]]

    def start(self, group=0) -> int:
        return self._group_spans[group][0]

    def end(self, group=0) -> int:
        return self._group_spans[group][1]
