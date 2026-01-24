import datetime
from dataclasses import dataclass

from chrono_python.types import Moment, DateTimeComponent, DateTimePrecision


@dataclass(frozen=True)
class ParsedResult:
    index: int
    text: str
    moment: Moment

    def datetime(self) -> datetime.datetime:
        return self.moment.datetime()


@dataclass(frozen=True)
class ParsedRangeResult(ParsedResult):
    end: Moment

    @property
    def start(self) -> Moment:
        return self.moment


class ParsingMoment(Moment):

    def __init__(self,
                 reference: Moment,
                 known_values: dict[DateTimeComponent, int],
                 implied_values: dict[DateTimeComponent, int] | None = None
                 ):
        self._reference = reference
        self._known_values = known_values
        self._implied_values = implied_values if implied_values is not None else {}

    def clone(self) -> 'ParsingMoment':
        return ParsingMoment(self._reference, self._known_values.copy(), self._implied_values.copy())

    def get(self, component: DateTimeComponent) -> int | None:
        if component in self._known_values:
            return self._known_values[component]
        if component in self._implied_values:
            return self._implied_values[component]
        return None

    def is_certain(self, component: DateTimeComponent) -> bool:
        return component in self._known_values

    def assign(self, component: DateTimeComponent, value: int) -> 'ParsingMoment':
        if component in self._implied_values:
            del self._implied_values[component]
        self._known_values[component] = value
        return self

    def imply(self, component: DateTimeComponent, value: int) -> 'ParsingMoment':
        if component not in self._known_values:
            self._implied_values[component] = value
        return self

    def datetime(self) -> datetime.datetime:
        return self._reference.datetime()

    def precision(self) -> DateTimePrecision:
        return self._reference.precision()
