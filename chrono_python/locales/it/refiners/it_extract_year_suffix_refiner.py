import re
from chrono_python import chrono
from chrono_python.chrono import ParsingContext, Refiner
from chrono_python.types import ParsedResult, ParsedRangeResult
from chrono_python.common.types import CivilTimeComponent, CivilTimeMoment
from chrono_python.locales.it import constants

YEAR_SUFFIX_PATTERN = re.compile(rf"^\s*({constants.YEAR_PATTERN})", re.IGNORECASE)


class ITExtractYearSuffixRefiner(Refiner):
    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        refined_results: list[ParsedResult] = []
        for result in results:
            moment = result.start
            if not isinstance(moment, CivilTimeMoment):
                refined_results.append(result)
                continue

            if (
                moment.get(CivilTimeComponent.DAY) is None
                or moment.get(CivilTimeComponent.MONTH) is None
                or moment.is_certain(CivilTimeComponent.YEAR)
            ):
                refined_results.append(result)
                continue

            suffix = context.text[result.index + len(result.text):]
            match = YEAR_SUFFIX_PATTERN.search(suffix)
            if not match:
                refined_results.append(result)
                continue

            if len(match.group(0).strip()) <= 3:
                refined_results.append(result)
                continue

            year = constants.parse_year(match.group(1))

            start_moment = moment.to_mutable()
            start_moment.assign(CivilTimeComponent.YEAR, year)

            new_text = result.text + match.group(0)

            if isinstance(result, ParsedRangeResult):
                end_moment = result.end.to_mutable() if isinstance(result.end, CivilTimeMoment) else result.end
                if isinstance(end_moment, CivilTimeMoment):
                    end_moment.assign(CivilTimeComponent.YEAR, year)
                refined_results.append(
                    context.create_parsed_result(
                        result.index, result.index + len(new_text), start=start_moment, end=end_moment
                    )
                )
            else:
                refined_results.append(
                    context.create_parsed_result(
                        result.index, result.index + len(new_text), start=start_moment
                    )
                )

        return refined_results
