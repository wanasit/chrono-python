import re
from chrono_python.chrono import ParsingContext, Refiner
from chrono_python.types import ParsedResult, ParsedRangeResult
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.common.timezone import to_timezone_offset

TIMEZONE_NAME_PATTERN = re.compile(
    r"^\s*,?\s*\(?([A-Z]{2,4})\)?(?=\W|$)",
    re.IGNORECASE
)

class ExtractTimezoneAbbrRefiner(Refiner):
    def __init__(self, timezone_overrides: dict = None):
        self.timezone_overrides = timezone_overrides or {}

    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        refined_results = []
        for result in results:
            if not isinstance(result.moment, ParsingCivilTimeMoment):
                refined_results.append(result)
                continue

            suffix = context.text[result.index + len(result.text):]
            match = TIMEZONE_NAME_PATTERN.match(suffix)
            if not match:
                refined_results.append(result)
                continue

            timezone_abbr = match.group(1).upper()
            ref_date = result.moment.datetime()

            extracted_timezone_offset = to_timezone_offset(
                timezone_abbr,
                ref_date,
                self.timezone_overrides
            )
            if extracted_timezone_offset is None:
                refined_results.append(result)
                continue

            current_timezone_offset = result.moment.get(CivilTimeComponent.TIMEZONE_OFFSET)
            if current_timezone_offset is not None and extracted_timezone_offset != current_timezone_offset:
                if result.moment.is_certain(CivilTimeComponent.TIMEZONE_OFFSET):
                    refined_results.append(result)
                    continue

                # For relative times or inferred timezones, double check case sensitivity
                if timezone_abbr != match.group(1):
                    refined_results.append(result)
                    continue

            if result.moment.is_only_date():
                if timezone_abbr != match.group(1):
                    refined_results.append(result)
                    continue

            # Clone start moment
            new_start = result.moment.to_mutable()
            if not new_start.is_certain(CivilTimeComponent.TIMEZONE_OFFSET):
                new_start.assign(CivilTimeComponent.TIMEZONE_OFFSET, extracted_timezone_offset)

            new_text = result.text + match.group(0)

            if isinstance(result, ParsedRangeResult):
                new_end = result.end
                if isinstance(new_end, ParsingCivilTimeMoment):
                    new_end = new_end.to_mutable()
                    if not new_end.is_certain(CivilTimeComponent.TIMEZONE_OFFSET):
                        new_end.assign(CivilTimeComponent.TIMEZONE_OFFSET, extracted_timezone_offset)
                new_result = ParsedRangeResult(index=result.index, text=new_text, moment=new_start, end=new_end)
            else:
                new_result = ParsedResult(index=result.index, text=new_text, moment=new_start)

            refined_results.append(new_result)

        return refined_results
