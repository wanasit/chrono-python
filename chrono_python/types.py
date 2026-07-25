import datetime
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Mapping



class DateTimePrecision(Enum):
    """
    Represents the level of precision of a parsed date or time.

    The numeric value indicate the level of granularity (higher the more fine-grained).
    """
    YEAR = 10
    MONTH = 20
    WEEK = 30
    DAY = 40
    HOUR = 50
    MINUTE = 60
    SECOND = 70
    MILLI_SECOND = 80


class Weekday(Enum):
    """
    Represents a day of the week, starting with Sunday as 0.
    """
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class Timeunit(Enum):
    """
    Represents a unit of time used for duration and offset calculations.
    """
    QUARTER = 'quarter'
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    WEEK = 'week'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLI_SECOND = 'millisecond'


Duration = Mapping[Timeunit, int]
"""Type alias representing a duration mapping from Timeunit to its integer quantity."""


class Moment(ABC):
    """An abstract class represents a moment in time."""

    @abstractmethod
    def datetime(self) -> datetime.datetime:
        """
        The `datetime.datetime` represents the moment. Typically, at the beginning of the moment.
        """
        raise NotImplementedError()

    @abstractmethod
    def precision(self) -> DateTimePrecision:
        """
        The precision of the moment.
        """
        raise NotImplementedError()

    def is_valid_date(self) -> bool:
        """
        Returns whether the moment represents a valid calendar date/time.
        """
        return True



@dataclass(frozen=True)
class DateTimeMoment(Moment):
    """A Moment based-on Python `datetime.datetime`."""
    _dt: datetime.datetime
    _precision: DateTimePrecision

    @classmethod
    def of(cls,
           reference: datetime.datetime,
           precision: DateTimePrecision = DateTimePrecision.MILLI_SECOND) -> 'DateTimeMoment':
        if precision is None:
            raise ValueError("DateTimeMoment precision cannot be None")
        return cls(_dt=reference, _precision=precision)

    @classmethod
    def now(cls):
        """
        Creates a DateTimeMoment representing the current system time.
        """
        return cls(_dt=datetime.datetime.now(), _precision=DateTimePrecision.MILLI_SECOND)

    def datetime(self) -> datetime.datetime:
        """
        Returns the python datetime representing this moment.
        """
        return self._dt

    def precision(self) -> DateTimePrecision:
        """
        Returns the precision of this moment.
        """
        return self._precision


@dataclass(frozen=True)
class ReferenceMoment(Moment):
    """A Moment represents time relative to another reference moment.

    While this class is frozen, the underlying reference could be mutable.
    When the reference is updated, the moment's value could also be changed.
    """
    _reference: Moment
    _delta: Duration

    @classmethod
    def of(cls,
           reference: Moment | datetime.datetime,
           delta: Duration | None = None) -> 'ReferenceMoment':
        ref_moment = reference if isinstance(reference, Moment) else DateTimeMoment.of(reference)
        return cls(_reference=ref_moment, _delta=delta if delta is not None else {Timeunit.DAY: 0})

    def datetime(self) -> datetime.datetime:
        ref_datetime = self._reference.datetime()

        target_month_0 = (
            ref_datetime.month - 1 +
            self._delta.get(Timeunit.MONTH, 0) +
            self._delta.get(Timeunit.QUARTER, 0) * 3
        )
        adjusted_year = ref_datetime.year + self._delta.get(Timeunit.YEAR, 0) + target_month_0 // 12
        adjusted_month = target_month_0 % 12 + 1

        adjusted_datetime = ref_datetime.replace(
            year=adjusted_year,
            month=adjusted_month,
        )
        return adjusted_datetime + datetime.timedelta(
            days=self._delta.get(Timeunit.DAY, 0) + self._delta.get(Timeunit.WEEK, 0) * 7,
            hours=self._delta.get(Timeunit.HOUR, 0),
            minutes=self._delta.get(Timeunit.MINUTE, 0),
            seconds=self._delta.get(Timeunit.SECOND, 0),
            milliseconds=self._delta.get(Timeunit.MILLI_SECOND, 0)
        )

    def precision(self) -> DateTimePrecision:
        ref_precision = self._reference.precision()
        for unit, precision in [
            (Timeunit.MILLI_SECOND, DateTimePrecision.MILLI_SECOND),
            (Timeunit.SECOND, DateTimePrecision.SECOND),
            (Timeunit.MINUTE, DateTimePrecision.MINUTE),
            (Timeunit.HOUR, DateTimePrecision.HOUR),
            (Timeunit.DAY, DateTimePrecision.DAY),
            (Timeunit.WEEK, DateTimePrecision.WEEK),
            (Timeunit.MONTH, DateTimePrecision.MONTH),
            (Timeunit.QUARTER, DateTimePrecision.MONTH),
            (Timeunit.YEAR, DateTimePrecision.YEAR),
        ]:
            if unit in self._delta and ref_precision.value >= precision.value:
                return precision
        return ref_precision


@dataclass(frozen=True)
class ParsedResult:
    """
    Represents the result of parsing a date/time expression.
    """
    index: int
    text: str
    moment: Moment

    def datetime(self) -> datetime.datetime:
        return self.moment.datetime()


@dataclass(frozen=True)
class ParsedRangeResult(ParsedResult):
    """
    Represents the result of parsing a date/time range expression (e.g., 'from X to Y').
    """
    end: Moment

    @property
    def start(self) -> Moment:
        return self.moment

