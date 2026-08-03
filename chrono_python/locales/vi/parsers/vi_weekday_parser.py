import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common import weekdays
from chrono_python.locales.vi import constants
from chrono_python.types import Moment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    return re.compile(
        f"({patterns.match_any(constants.WEEKDAY_DICTIONARY)})"
        r"(?:\s*(này|tới|sau(?!\s*khi)|qua))?"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VIWeekdayParser(AbstractParserWithWordBoundary):
    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        dow_text = match[1].lower()
        dow = constants.WEEKDAY_DICTIONARY.get(dow_text)
        if dow is None:
            return None

        modifier = match[2]
        if self.strict_mode and not modifier:
            return None
        modifier_type = None
        if modifier:
            m = modifier.lower()
            if "tới" in m or "sau" in m:
                modifier_type = "next"
            elif "qua" in m:
                modifier_type = "last"

        return weekdays.create_parsing_components_at_weekday(
            context.reference, dow, modifier_type
        )
