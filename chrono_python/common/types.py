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

    Components that are neither explicitly set (`known_values`) nor inferred (`implied_values`) are treated as zero values (e.g. month 1, day 1, minute 0, second 0), except year (which defaults to 1970) and hour (which defaults to 12:00 for date-only expressions).
    """

    def __init__(
        self,
        known_values: dict[CivilTimeComponent, int] | None = None,
        implied_values: dict[CivilTimeComponent, int] | None = None,
        precision: DateTimePrecision | None = None
    ):
        super().__init__(_dt=None, _precision=precision)

        object.__setattr__(self, '_known_values', known_values.copy() if known_values else {})
        object.__setattr__(self, '_implied_values', implied_values.copy() if implied_values else {})

    @classmethod
    def of(
        cls,
        reference: Moment | datetime.datetime,
        precision: DateTimePrecision | None = None
    ):
        """Factory constructor creating a CivilTimeMoment / ParsingCivilTimeMoment with implied components from a reference based on precision."""
        ref_dt = reference.datetime() if isinstance(reference, Moment) else reference
        if precision is not None:
            target_prec = precision
        else:
            ref_prec = reference.precision() if isinstance(reference, Moment) else DateTimePrecision.DAY
            target_prec = ref_prec if ref_prec.value <= DateTimePrecision.DAY.value else DateTimePrecision.DAY

        implied = {}
        if target_prec.value >= DateTimePrecision.YEAR.value:
            implied[CivilTimeComponent.YEAR] = ref_dt.year
        if target_prec.value >= DateTimePrecision.MONTH.value:
            implied[CivilTimeComponent.MONTH] = ref_dt.month
        if target_prec.value >= DateTimePrecision.DAY.value or target_prec == DateTimePrecision.WEEK:
            implied[CivilTimeComponent.DAY] = ref_dt.day
        if target_prec.value >= DateTimePrecision.HOUR.value:
            implied[CivilTimeComponent.HOUR] = ref_dt.hour
            implied[CivilTimeComponent.MERIDIEM] = Meridiem.AM if ref_dt.hour < 12 else Meridiem.PM
        if target_prec.value >= DateTimePrecision.MINUTE.value:
            implied[CivilTimeComponent.MINUTE] = ref_dt.minute
        if target_prec.value >= DateTimePrecision.SECOND.value:
            implied[CivilTimeComponent.SECOND] = ref_dt.second
        if target_prec.value >= DateTimePrecision.MILLI_SECOND.value:
            implied[CivilTimeComponent.MILLI_SECOND] = ref_dt.microsecond // 1000

        return cls(known_values=None, implied_values=implied, precision=precision or (reference.precision() if isinstance(reference, Moment) else None))

    def __setattr__(self, name, value):
        raise AttributeError("CivilTimeMoment is immutable. Use to_mutable() to modify.")

    def clone(self) -> 'CivilTimeMoment':
        return CivilTimeMoment(
            known_values=self._known_values.copy(),
            implied_values=self._implied_values.copy(),
            precision=super().precision()
        )

    def to_mutable(self) -> 'ParsingCivilTimeMoment':
        return ParsingCivilTimeMoment(
            known_values=self._known_values.copy(),
            implied_values=self._implied_values.copy(),
            precision=super().precision()
        )

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
            prec = COMPONENT_PRECISION_MAP.get(component)
            if prec is not None:
                if max_precision is None or prec.value > max_precision.value:
                    max_precision = prec
        
        if max_precision is None:
            fallback = super().precision()
            if fallback is not None:
                return fallback
            raise ValueError("Cannot determine precision for CivilTimeMoment without known components.")
        return max_precision

    def datetime(self) -> datetime.datetime:
        year = self.get(CivilTimeComponent.YEAR) or 1970
        month = self.get(CivilTimeComponent.MONTH) or 1
        day = self.get(CivilTimeComponent.DAY) or 1
        hour = self.get(CivilTimeComponent.HOUR)
        if hour is None:
            hour = 12
        minute = self.get(CivilTimeComponent.MINUTE) or 0
        second = self.get(CivilTimeComponent.SECOND) or 0
        millisecond = self.get(CivilTimeComponent.MILLI_SECOND)
        microsecond = millisecond * 1000 if millisecond is not None else 0

        tz_offset = self.get(CivilTimeComponent.TIMEZONE_OFFSET)
        tzinfo = datetime.timezone(datetime.timedelta(minutes=tz_offset)) if tz_offset is not None else None

        return datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            tzinfo=tzinfo
        )


class ParsingCivilTimeMoment(CivilTimeMoment):
    """
    A mutable CivilTimeMoment that can be updated during parsing.
    """

    def __init__(
        self,
        known_values: dict[CivilTimeComponent, int] | None = None,
        implied_values: dict[CivilTimeComponent, int] | None = None,
        precision: DateTimePrecision | None = None
    ):
        super().__init__(known_values=known_values, implied_values=implied_values, precision=precision)

    def __setattr__(self, name, value):
        # Bypass the frozen class restrictions on subclass attributes
        object.__setattr__(self, name, value)

    def clone(self) -> 'ParsingCivilTimeMoment':
        return ParsingCivilTimeMoment(
            known_values=self._known_values.copy(),
            implied_values=self._implied_values.copy(),
            precision=super().precision()
        )

    def to_mutable(self) -> 'ParsingCivilTimeMoment':
        return self

    def freeze(self) -> CivilTimeMoment:
        return CivilTimeMoment(
            known_values=self._known_values.copy(),
            implied_values=self._implied_values.copy(),
            precision=super().precision()
        )

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