from abc import ABC, abstractmethod
from chrono_python import chrono
from chrono_python.chrono import ParsingContext
from chrono_python.types import ParsedResult


class AbstractMergingRefiner(chrono.Refiner, ABC):
    """
    An abstract base class for refiners that merge consecutive parsed results.
    Subclasses must implement `should_merge_results` and `merge_results`.
    """

    @abstractmethod
    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        raise NotImplementedError()

    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        if len(results) < 2:
            return results

        merged_results: list[ParsedResult] = []
        cur_result = results[0]

        for i in range(1, len(results)):
            next_result = results[i]

            text_between = context.text[cur_result.index + len(cur_result.text):next_result.index]
            if not self.should_merge_results(text_between, cur_result, next_result, context):
                merged_results.append(cur_result)
                cur_result = next_result
            else:
                merged_result = self.merge_results(text_between, cur_result, next_result, context)
                cur_result = merged_result

        if cur_result is not None:
            merged_results.append(cur_result)

        return merged_results
