import datetime
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


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

class DateTimePrecision(Enum):
    YEAR = 10
    MONTH = 20
    WEEK = 30
    DAY = 40
    HOUR = 50
    MINUTE = 60
    SECOND = 70
    MILLI_SECOND = 80


class Timeunit(Enum):
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    WEEK = 'week'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLI_SECOND = 'millisecond'


Duration = Mapping[Timeunit, int]


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
    dt: datetime.datetime
    precision: DateTimePrecision

    @classmethod
    def of(cls,
           reference: datetime.datetime,
           precision: DateTimePrecision = DateTimePrecision.MILLI_SECOND) -> 'DateTimeMoment':
        return cls(reference, precision)

    @classmethod
    def now(cls):
        return cls(datetime.datetime.now(), DateTimePrecision.MILLI_SECOND)

    def datetime(self) -> datetime.datetime:
        return self.dt

    def precision(self) -> DateTimePrecision:
        return self.precision


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
