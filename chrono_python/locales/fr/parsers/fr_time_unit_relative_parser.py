import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.fr import constants
from chrono_python.types import Moment, ReferenceMoment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    modifier_pattern = r"(?:prochaine?s?|derni[eè]re?s?|pass[ée]e?s?|pr[ée]c[ée]dents?|suivante?s?)"
    return re.compile(
        r"(?:les?|la|l'|du|des?)\s*"
        f"({constants.NUMBER_PATTERN})?"
        rf"(?:\s*({modifier_pattern}))?"
        f"\\s*({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})"
        rf"(?:\s*({modifier_pattern}))?"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class FRTimeUnitRelativeParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        num = constants.parse_number_pattern(match.group(1)) if match.group(1) else 1
        unit_str = match.group(3).lower()
        if unit_str not in constants.TIME_UNIT_DICTIONARY:
            return None
        unit = constants.TIME_UNIT_DICTIONARY[unit_str]

        modifier = (match.group(2) or match.group(4) or "").lower()
        if not modifier:
            return None

        if re.search(r"derni[eè]re?s?|pass[ée]e?s?|pr[ée]c[ée]dents?", modifier):
            num = -num

        time_units = {unit: num}
        return ReferenceMoment.of(context.reference, time_units)
