import datetime
from abc import ABC, abstractmethod
from enum import Enum

from chrono_python.types import Moment, DateTimeComponent, DateTimePrecision


class ParsedResult:
    def __init__(self, index: int, text: str, moment: Moment):
        self._index = index
        self._text = text
        self._moment = moment

    @property
    def index(self) -> int:
        return self._index

    @property
    def text(self) -> str:
        return self._text

    @property
    def moment(self) -> Moment:
        return self._moment

    def datetime(self) -> datetime.datetime:
        return self._moment.datetime()


class ParsedRangeResult(ParsedResult):
    def __init__(self, index: int, text: str, start: Moment, end: Moment):
        super().__init__(index, text, start)
        self._start = start
        self._end = end

    @property
    def start(self) -> Moment:
        return self._start

    @property
    def end(self) -> Moment:
        return self._end


class ParsingMoment(Moment):

    def __init__(self,
                 reference: Moment,
                 known_values: dict[DateTimeComponent, int],
                 implied_values: dict[DateTimeComponent, int] | None = None
                 ):
        self._reference = reference
        self._known_values = known_values
        self._implied_values = implied_values if implied_values is not None else {}

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
