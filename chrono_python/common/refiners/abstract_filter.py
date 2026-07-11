from abc import ABC, abstractmethod
from chrono_python import chrono
from chrono_python.chrono import ParsingContext
from chrono_python.types import ParsedResult


class AbstractFilter(chrono.Refiner, ABC):
    """
    An abstract base class for refiners that filter results.
    Subclasses must implement `is_valid`.
    """

    @abstractmethod
    def is_valid(self, context: ParsingContext, result: ParsedResult) -> bool:
        raise NotImplementedError()

    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        return [r for r in results if self.is_valid(context, r)]


Filter = AbstractFilter
