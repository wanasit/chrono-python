"""
Internal types for chrono (or custom parsers/refiners), not intended for direct use by end users.
"""

import datetime
from enum import Enum
from chrono_python.types import Moment, DateTimeMoment, DateTimePrecision

class Meridiem(Enum):
    """
    Represents the period of the day (AM or PM) in a 12-hour clock system.
    """
    AM = 0
    PM = 1


class CivilTimeComponent(Enum):
    """
    Represents individual fields of a human-readable calendar date and clock time (e.g., year, month, day, hour).
    """
    YEAR = 'year'
    MONTH = 'month'
    WEEKDAY = 'weekday'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLI_SECOND = 'millisecond'
    TIMEZONE_OFFSET = 'timezone_offset'
    MERIDIEM = 'meridiem'


class CivilTimeMoment(DateTimeMoment):
    """
    An immutable DateTimeMoment that is represented by human-readable calendar and clock components (e.g., year, month, day, hour).

    Unlike `datetime` or system epoch, this class represents time from the perspective of a human reading a calendar and clock. 
    This follows the concept of `CivilTime` in Abseil, or `Temporal.PlainDateTime`/`Temporal.LocalDateTime` in JavaScript.

    The time components made of this moment are separated into two groups:
        1. `known_values`: components that are explicitly set by the user.
        2. `implied_values`: components that are inferred and weaker than known_values.
    """

    def __init__(
                 self,
                 reference: Moment,
                 known_values: dict[CivilTimeComponent, int],
                 implied_values: dict[CivilTimeComponent, int] | None = None
                 ):
        # Initialize the frozen DateTimeMoment base class
        super().__init__(_dt=reference.datetime(), _precision=DateTimePrecision.MILLI_SECOND)
        object.__setattr__(self, '_reference', reference)
        object.__setattr__(self, '_known_values', known_values.copy())
        object.__setattr__(self, '_implied_values', implied_values.copy() if implied_values is not None else {})

    def __setattr__(self, name, value):
        raise AttributeError("CivilTimeMoment is immutable. Use to_mutable() to modify.")

    def clone(self) -> 'CivilTimeMoment':
        return CivilTimeMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

    def to_mutable(self) -> 'ParsingCivilTimeMoment':
        return ParsingCivilTimeMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

    def freeze(self) -> 'CivilTimeMoment':
        return self

    def is_valid_date(self) -> bool:
        year = self.get(CivilTimeComponent.YEAR)
        month = self.get(CivilTimeComponent.MONTH)
        day = self.get(CivilTimeComponent.DAY)

        if month is not None and (month < 1 or month > 12):
            return False
        if day is not None:
            if day < 1 or day > 31:
                return False
            if month is not None:
                is_leap = True
                if year is not None:
                    # Python leap year rules (works for negative years too)
                    is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
                month_days = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if day > month_days[month - 1]:
                    return False
        return True



    def get(self, component: CivilTimeComponent) -> int | None:
        if component in self._known_values:
            return self._known_values[component]
        if component in self._implied_values:
            return self._implied_values[component]
        return None

    def is_certain(self, component: CivilTimeComponent) -> bool:
        return component in self._known_values

    def list(self, only_certain: bool = True) -> list[CivilTimeComponent]:
        if only_certain:
            return list(self._known_values.keys())
        return list(set(self._known_values.keys()) | set(self._implied_values.keys()))

    def is_only_weekday_component(self) -> bool:
        return (
            self.is_certain(CivilTimeComponent.WEEKDAY)
            and not self.is_certain(CivilTimeComponent.DAY)
            and not self.is_certain(CivilTimeComponent.MONTH)
        )

    def is_only_date(self) -> bool:
        return (
            not self.is_certain(CivilTimeComponent.HOUR)
            and not self.is_certain(CivilTimeComponent.MINUTE)
            and not self.is_certain(CivilTimeComponent.SECOND)
        )

    def is_only_time(self) -> bool:
        return (
            not self.is_certain(CivilTimeComponent.WEEKDAY)
            and not self.is_certain(CivilTimeComponent.DAY)
            and not self.is_certain(CivilTimeComponent.MONTH)
            and not self.is_certain(CivilTimeComponent.YEAR)
        )

    def is_date_with_unknown_year(self) -> bool:
        return (
            self.is_certain(CivilTimeComponent.MONTH)
            and not self.is_certain(CivilTimeComponent.YEAR)
        )

    def precision(self) -> DateTimePrecision:
        max_precision = None
        for component in self._known_values.keys():
            precision = COMPONENT_PRECISION_MAP.get(component)
            if precision is not None:
                if max_precision is None or precision.value > max_precision.value:
                    max_precision = precision
        
        if max_precision is None:
            return self._reference.precision()
        return max_precision

    def datetime(self) -> datetime.datetime:
        ref_dt = self._reference.datetime()
        
        year = self.get(CivilTimeComponent.YEAR)
        if year is None:
            year = ref_dt.year
            
        month = self.get(CivilTimeComponent.MONTH)
        if month is None:
            month = ref_dt.month
            
        day = self.get(CivilTimeComponent.DAY)
        if day is None:
            day = ref_dt.day
            
        hour = self.get(CivilTimeComponent.HOUR)
        if hour is None:
            hour = 12
            
        minute = self.get(CivilTimeComponent.MINUTE)
        if minute is None:
            minute = 0
            
        second = self.get(CivilTimeComponent.SECOND)
        if second is None:
            second = 0
            
        millisecond = self.get(CivilTimeComponent.MILLI_SECOND)
        microsecond = millisecond * 1000 if millisecond is not None else 0
        
        return datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            tzinfo=ref_dt.tzinfo
        )


class ParsingCivilTimeMoment(CivilTimeMoment):
    """
    A mutable CivilTimeMoment that can be updated during parsing.
    """

    def __init__(
                 self,
                 reference: Moment,
                 known_values: dict[CivilTimeComponent, int],
                 implied_values: dict[CivilTimeComponent, int] | None = None
                 ):
        super().__init__(reference, known_values, implied_values)

    def __setattr__(self, name, value):
        # Bypass the frozen class restrictions on subclass attributes
        object.__setattr__(self, name, value)

    def clone(self) -> 'ParsingCivilTimeMoment':
        return ParsingCivilTimeMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

    def to_mutable(self) -> 'ParsingCivilTimeMoment':
        return self

    def freeze(self) -> CivilTimeMoment:
        return CivilTimeMoment(self._reference, self._known_values, self._implied_values)

    def assign(self, component: CivilTimeComponent, value: int) -> 'ParsingCivilTimeMoment':
        if component in self._implied_values:
            del self._implied_values[component]
        self._known_values[component] = value
        return self

    def imply(self, component: CivilTimeComponent, value: int) -> 'ParsingCivilTimeMoment':
        if component not in self._known_values:
            self._implied_values[component] = value
        return self

    def delete(self, component: CivilTimeComponent) -> 'ParsingCivilTimeMoment':
        if component in self._known_values:
            del self._known_values[component]
        if component in self._implied_values:
            del self._implied_values[component]
        return self

    def assign_similar_date(self, target: datetime.datetime | Moment) -> 'ParsingCivilTimeMoment':
        dt = target.datetime() if isinstance(target, Moment) else target
        prec = target.precision() if isinstance(target, Moment) else DateTimePrecision.MILLI_SECOND
        
        if prec.value >= DateTimePrecision.YEAR.value:
            self.assign(CivilTimeComponent.YEAR, dt.year)
        if prec.value >= DateTimePrecision.MONTH.value:
            self.assign(CivilTimeComponent.MONTH, dt.month)
        if prec.value >= DateTimePrecision.DAY.value or prec == DateTimePrecision.WEEK:
            self.assign(CivilTimeComponent.DAY, dt.day)
        return self

    def assign_similar_time(self, target: datetime.datetime | Moment) -> 'ParsingCivilTimeMoment':
        dt = target.datetime() if isinstance(target, Moment) else target
        prec = target.precision() if isinstance(target, Moment) else DateTimePrecision.MILLI_SECOND
        
        if prec.value >= DateTimePrecision.HOUR.value:
            self.assign(CivilTimeComponent.HOUR, dt.hour)
            self.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM if dt.hour < 12 else Meridiem.PM)
        if prec.value >= DateTimePrecision.MINUTE.value:
            self.assign(CivilTimeComponent.MINUTE, dt.minute)
        if prec.value >= DateTimePrecision.SECOND.value:
            self.assign(CivilTimeComponent.SECOND, dt.second)
        if prec.value >= DateTimePrecision.MILLI_SECOND.value:
            self.assign(CivilTimeComponent.MILLI_SECOND, dt.microsecond // 1000)
        return self

    def imply_similar_date(self, target: datetime.datetime | Moment) -> 'ParsingCivilTimeMoment':
        dt = target.datetime() if isinstance(target, Moment) else target
        prec = target.precision() if isinstance(target, Moment) else DateTimePrecision.MILLI_SECOND
        
        if prec.value >= DateTimePrecision.YEAR.value:
            self.imply(CivilTimeComponent.YEAR, dt.year)
        if prec.value >= DateTimePrecision.MONTH.value:
            self.imply(CivilTimeComponent.MONTH, dt.month)
        if prec.value >= DateTimePrecision.DAY.value or prec == DateTimePrecision.WEEK:
            self.imply(CivilTimeComponent.DAY, dt.day)
        return self

    def imply_similar_time(self, target: datetime.datetime | Moment) -> 'ParsingCivilTimeMoment':
        dt = target.datetime() if isinstance(target, Moment) else target
        prec = target.precision() if isinstance(target, Moment) else DateTimePrecision.MILLI_SECOND
        
        if prec.value >= DateTimePrecision.HOUR.value:
            self.imply(CivilTimeComponent.HOUR, dt.hour)
            self.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM if dt.hour < 12 else Meridiem.PM)
        if prec.value >= DateTimePrecision.MINUTE.value:
            self.imply(CivilTimeComponent.MINUTE, dt.minute)
        if prec.value >= DateTimePrecision.SECOND.value:
            self.imply(CivilTimeComponent.SECOND, dt.second)
        if prec.value >= DateTimePrecision.MILLI_SECOND.value:
            self.imply(CivilTimeComponent.MILLI_SECOND, dt.microsecond // 1000)
        return self



COMPONENT_PRECISION_MAP = {
    CivilTimeComponent.YEAR: DateTimePrecision.YEAR,
    CivilTimeComponent.MONTH: DateTimePrecision.MONTH,
    CivilTimeComponent.DAY: DateTimePrecision.DAY,
    CivilTimeComponent.WEEKDAY: DateTimePrecision.DAY,
    CivilTimeComponent.HOUR: DateTimePrecision.HOUR,
    CivilTimeComponent.MINUTE: DateTimePrecision.MINUTE,
    CivilTimeComponent.SECOND: DateTimePrecision.SECOND,
    CivilTimeComponent.MILLI_SECOND: DateTimePrecision.MILLI_SECOND,
    CivilTimeComponent.MERIDIEM: DateTimePrecision.DAY,
}
"""
Mapping from CivilTimeComponent to its precision (DateTimePrecision).
"""