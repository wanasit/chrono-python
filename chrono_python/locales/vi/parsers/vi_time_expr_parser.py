import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment


def compile_pattern() -> re.Pattern:
    return re.compile(
        r"(?:lúc\s*|vào\s*)?"
        r"([0-9]{1,2})"
        r"(?:\s*giờ\s*([0-9]{1,2})?\s*(?:phút\s*)?"
        r"(sáng|trưa|chiều|tối|đêm)?"
        r"|:([0-9]{2}))"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VITimeExprParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        hour = int(match[1])
        if hour > 23:
            return None

        moment = ParsingCivilTimeMoment.of(context.reference)
        moment.assign(CivilTimeComponent.HOUR, hour)

        if match[4]:
            minute = int(match[4])
        elif match[2]:
            minute = int(match[2])
        else:
            minute = 0

        if minute >= 60:
            return None

        moment.assign(CivilTimeComponent.MINUTE, minute)

        meridiem_str = match[3].lower() if match[3] else None
        if meridiem_str == "sáng":
            moment.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            if hour == 12:
                moment.assign(CivilTimeComponent.HOUR, 0)
        elif meridiem_str == "trưa":
            if hour < 10:
                moment.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
                moment.assign(CivilTimeComponent.HOUR, hour + 12)
            else:
                moment.assign(
                    CivilTimeComponent.MERIDIEM,
                    Meridiem.PM if hour >= 12 else Meridiem.AM,
                )
        elif meridiem_str in ("chiều", "tối", "đêm"):
            moment.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            if hour < 12:
                moment.assign(CivilTimeComponent.HOUR, hour + 12)

        moment.imply(CivilTimeComponent.SECOND, 0)
        moment.imply(CivilTimeComponent.MILLI_SECOND, 0)
        return moment
