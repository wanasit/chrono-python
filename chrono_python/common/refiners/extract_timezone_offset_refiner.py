import re
from chrono_python.chrono import ParsingContext, Refiner
from chrono_python.types import ParsedResult, ParsedRangeResult
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

TIMEZONE_OFFSET_PATTERN = re.compile(
    r"^\s*(?:\(?(?:GMT|UTC)\s?)?([+-])(\d{1,2})(?::?(\d{2}))?\)?",
    re.IGNORECASE
)

class ExtractTimezoneOffsetRefiner(Refiner):
    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        refined_results = []
        for result in results:
            if not isinstance(result.moment, ParsingCivilTimeMoment):
                refined_results.append(result)
                continue

            if result.moment.is_certain(CivilTimeComponent.TIMEZONE_OFFSET):
                refined_results.append(result)
                continue

            suffix = context.text[result.index + len(result.text):]
            match = TIMEZONE_OFFSET_PATTERN.match(suffix)
            if not match:
                refined_results.append(result)
                continue

            hour_offset = int(match.group(2))
            minute_offset_str = match.group(3)
            minute_offset = int(minute_offset_str) if minute_offset_str else 0
            timezone_offset = hour_offset * 60 + minute_offset

            # Disregard offsets greater than 14 hours
            if timezone_offset > 14 * 60:
                refined_results.append(result)
                continue

            if match.group(1) == "-":
                timezone_offset = -timezone_offset

            # Clone the start moment to avoid mutating the original
            new_start = result.moment.to_mutable()
            new_start.assign(CivilTimeComponent.TIMEZONE_OFFSET, timezone_offset)

            new_text = result.text + match.group(0)

            if isinstance(result, ParsedRangeResult):
                new_end = result.end
                if isinstance(new_end, ParsingCivilTimeMoment):
                    new_end = new_end.to_mutable()
                    new_end.assign(CivilTimeComponent.TIMEZONE_OFFSET, timezone_offset)
                new_result = ParsedRangeResult(index=result.index, text=new_text, moment=new_start, end=new_end)
            else:
                new_result = ParsedResult(index=result.index, text=new_text, moment=new_start)

            refined_results.append(new_result)

        return refined_results
