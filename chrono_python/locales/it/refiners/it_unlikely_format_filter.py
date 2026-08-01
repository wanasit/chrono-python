from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners import Filter
from chrono_python.common.types import CivilTimeMoment
from chrono_python.types import ParsedResult


class ITUnlikelyFormatFilter(Filter):
    """
    Filters out unlikely date/time matches in Italian, such as:
    - "secondo" (when it is likely used as an ordinal number rather than a unit of time)
    - Standalone weekday name in strict mode
    """

    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode

    def is_valid(self, context: ParsingContext, result: ParsedResult) -> bool:
        text = result.text.strip()

        if text == context.text.strip():
            if self.strict_mode and isinstance(result.moment, CivilTimeMoment):
                if result.moment.is_only_weekday_component():
                    return False
            return True

        lower_text = text.lower()
        if lower_text.endswith("il secondo") or lower_text == "secondo":
            return False

        return True
