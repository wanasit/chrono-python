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


class Timeunit(Enum):
    """
    Represents a unit of time used for duration and offset calculations.
    """
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


@dataclass(frozen=True)
class DateTimeMoment(Moment):
    """A Moment based-on Python `datetime.datetime`."""
    _dt: datetime.datetime
    _precision: DateTimePrecision

    @classmethod
    def of(cls,
           reference: datetime.datetime,
           precision: DateTimePrecision = DateTimePrecision.MILLI_SECOND) -> 'DateTimeMoment':
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
    When the reference is update, the moment's value could also be changed.
    """
    reference: Moment
    delta: Duration

    def datetime(self) -> datetime.datetime:
        ref_datetime = self.reference.datetime()

        target_month = ref_datetime.month + self.delta.get(Timeunit.MONTH, 0)
        adjusted_year = ref_datetime.year + self.delta.get(Timeunit.YEAR, 0) + target_month // 12
        adjusted_month = target_month % 12

        adjusted_datetime = ref_datetime.replace(
            year=adjusted_year,
            month=adjusted_month,
        )
        return adjusted_datetime + datetime.timedelta(
            days=self.delta.get(Timeunit.DAY, 0) + self.delta.get(Timeunit.WEEK, 0) * 7,
            hours=self.delta.get(Timeunit.HOUR, 0),
            minutes=self.delta.get(Timeunit.MINUTE, 0),
            seconds=self.delta.get(Timeunit.SECOND, 0),
            milliseconds=self.delta.get(Timeunit.MILLI_SECOND, 0)
        )

    def precision(self) -> DateTimePrecision:
        ref_precision = self.reference.precision()
        for unit, precision in [
            (Timeunit.MILLI_SECOND, DateTimePrecision.MILLI_SECOND),
            (Timeunit.SECOND, DateTimePrecision.SECOND),
            (Timeunit.MINUTE, DateTimePrecision.MINUTE),
            (Timeunit.HOUR, DateTimePrecision.HOUR),
            (Timeunit.DAY, DateTimePrecision.DAY),
            (Timeunit.WEEK, DateTimePrecision.WEEK),
            (Timeunit.MONTH, DateTimePrecision.MONTH),
            (Timeunit.YEAR, DateTimePrecision.YEAR),
        ]:
            if unit in self.delta and ref_precision.value >= precision.value:
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

