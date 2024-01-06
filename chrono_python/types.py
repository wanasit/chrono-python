import datetime
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
    @abstractmethod
    def datetime(self) -> datetime.datetime:
        raise NotImplementedError()

    @abstractmethod
    def precision(self) -> DateTimePrecision:
        raise NotImplementedError()


class DateTimeMoment(Moment):

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
