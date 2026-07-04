from chrono_python import chrono
from chrono_python.chrono import ParsingContext
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import ParsedResult


class RemoveOverlapRefiner(chrono.Refiner):

    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        if len(results) <= 1:
            return results

        results.sort(key=lambda r: r.index)
        filtered_results: list[ParsedResult] = []
        previous_result: ParsedResult = results[0]
        for result in results[1:]:
            # If the current result doesn't overlap with the previous one
            if result.index >= previous_result.index + len(previous_result.text):
                filtered_results.append(previous_result)
                previous_result = result
                continue
            # If the current result overlaps with the last one
            if len(result.text) > len(previous_result.text):
                previous_result = result
            else:
                # Keep the previous result, drop the current one
                pass

        if previous_result is not None:
            filtered_results.append(previous_result)
        return filtered_results
