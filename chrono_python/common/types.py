import datetime
from enum import Enum
from chrono_python.types import Moment, DateTimeMoment, DateTimePrecision

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

COMPONENT_PRECISION_MAP = {
    DateTimeComponent.YEAR: DateTimePrecision.YEAR,
    DateTimeComponent.MONTH: DateTimePrecision.MONTH,
    DateTimeComponent.DAY: DateTimePrecision.DAY,
    DateTimeComponent.WEEKDAY: DateTimePrecision.DAY,
    DateTimeComponent.HOUR: DateTimePrecision.HOUR,
    DateTimeComponent.MINUTE: DateTimePrecision.MINUTE,
    DateTimeComponent.SECOND: DateTimePrecision.SECOND,
    DateTimeComponent.MILLI_SECOND: DateTimePrecision.MILLI_SECOND,
}

class ParsingDateTimeMoment(DateTimeMoment):

    def __init__(self,
                 reference: Moment,
                 known_values: dict[DateTimeComponent, int],
                 implied_values: dict[DateTimeComponent, int] | None = None
                 ):
        # Initialize the frozen DateTimeMoment base class
        super().__init__(_dt=reference.datetime(), _precision=DateTimePrecision.MILLI_SECOND)
        self._reference = reference
        self._known_values = known_values
        self._implied_values = implied_values if implied_values is not None else {}

    def __setattr__(self, name, value):
        # Bypass the frozen class restrictions on subclass attributes
        object.__setattr__(self, name, value)

    def clone(self) -> 'ParsingDateTimeMoment':
        return ParsingDateTimeMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

    def get(self, component: DateTimeComponent) -> int | None:
        if component in self._known_values:
            return self._known_values[component]
        if component in self._implied_values:
            return self._implied_values[component]
        return None

    def is_certain(self, component: DateTimeComponent) -> bool:
        return component in self._known_values

    def assign(self, component: DateTimeComponent, value: int) -> 'ParsingDateTimeMoment':
        if component in self._implied_values:
            del self._implied_values[component]
        self._known_values[component] = value
        return self

    def imply(self, component: DateTimeComponent, value: int) -> 'ParsingDateTimeMoment':
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
        
        year = self.get(DateTimeComponent.YEAR)
        if year is None:
            year = ref_dt.year
            
        month = self.get(DateTimeComponent.MONTH)
        if month is None:
            month = ref_dt.month
            
        day = self.get(DateTimeComponent.DAY)
        if day is None:
            day = ref_dt.day
            
        hour = self.get(DateTimeComponent.HOUR)
        if hour is None:
            hour = 12
            
        minute = self.get(DateTimeComponent.MINUTE)
        if minute is None:
            minute = 0
            
        second = self.get(DateTimeComponent.SECOND)
        if second is None:
            second = 0
            
        millisecond = self.get(DateTimeComponent.MILLI_SECOND)
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


