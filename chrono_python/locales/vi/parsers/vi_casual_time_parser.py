import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment


def compile_pattern() -> re.Pattern:
    return re.compile(
        r"(buổi\s*)?(sáng sớm|sáng|trưa|chiều|tối|đêm|nửa đêm|bình minh)(?=\W|$)",
        re.IGNORECASE,
    )


class VICasualTimeParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        component = ParsingCivilTimeMoment.of(context.reference)
        component.imply_similar_time(context.reference.datetime())
        keyword = match[2].lower()
        return extract_time_components(component, keyword)


def extract_time_components(
    component: ParsingCivilTimeMoment, keyword: str
) -> ParsingCivilTimeMoment:
    if keyword in ("bình minh", "sáng sớm"):
        component.imply(CivilTimeComponent.HOUR, 6)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
    elif keyword == "sáng":
        component.imply(CivilTimeComponent.HOUR, 9)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
    elif keyword == "trưa":
        component.imply(CivilTimeComponent.HOUR, 12)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
    elif keyword == "chiều":
        component.imply(CivilTimeComponent.HOUR, 15)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
    elif keyword == "tối":
        component.imply(CivilTimeComponent.HOUR, 19)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
    elif keyword == "đêm":
        component.imply(CivilTimeComponent.HOUR, 22)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
    elif keyword == "nửa đêm":
        component.imply(CivilTimeComponent.HOUR, 0)
        component.imply(CivilTimeComponent.MINUTE, 0)
        component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
    return component
