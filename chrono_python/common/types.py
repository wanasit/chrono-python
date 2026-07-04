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


class ParsingCivilTimeMoment(DateTimeMoment):
    """
    A mutable DateTimeMoment that is represented by human-readable calendar and clock components (e.g., year, month, day, hour).

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
        self._reference = reference
        self._known_values = known_values
        self._implied_values = implied_values if implied_values is not None else {}

    def __setattr__(self, name, value):
        # Bypass the frozen class restrictions on subclass attributes
        object.__setattr__(self, name, value)

    def clone(self) -> 'ParsingCivilTimeMoment':
        return ParsingCivilTimeMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

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

    def is_date_with_unknown_year(self) -> bool:
        return (
            self.is_certain(CivilTimeComponent.MONTH)
            and not self.is_certain(CivilTimeComponent.YEAR)
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

    def precision(self) -> DateTimePrecision:
        max_precision = None
        all_components = set(self._known_values.keys()) | set(self._implied_values.keys())
        for component in all_components:
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



COMPONENT_PRECISION_MAP = {
    CivilTimeComponent.YEAR: DateTimePrecision.YEAR,
    CivilTimeComponent.MONTH: DateTimePrecision.MONTH,
    CivilTimeComponent.DAY: DateTimePrecision.DAY,
    CivilTimeComponent.WEEKDAY: DateTimePrecision.DAY,
    CivilTimeComponent.HOUR: DateTimePrecision.HOUR,
    CivilTimeComponent.MINUTE: DateTimePrecision.MINUTE,
    CivilTimeComponent.SECOND: DateTimePrecision.SECOND,
    CivilTimeComponent.MILLI_SECOND: DateTimePrecision.MILLI_SECOND,
    CivilTimeComponent.MERIDIEM: DateTimePrecision.HOUR,
}
"""
Mapping from CivilTimeComponent to its precision (DateTimePrecision).
"""