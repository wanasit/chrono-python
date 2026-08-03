import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.de import constants
from chrono_python.types import Moment, ReferenceMoment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    modifier_pattern = r"(?:letzte[nrsm]?|vergangene[nrsm]?|nächste[nrsm]?|naechste[nrsm]?|kommende[nrsm]?|diese[nrsm]?)"
    return re.compile(
        r"(?:"
        r"(?:vor\s+)"
        rf"({constants.NUMBER_PATTERN})\s*"
        rf"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})"
        r"|(?:(?:die|das|der|den|dem|des)\s*)?"
        rf"({constants.NUMBER_PATTERN})?\s*"
        rf"(?:({modifier_pattern})\s*)?"
        rf"({patterns.match_any(constants.TIME_UNIT_DICTIONARY)})\s*"
        rf"(?:({modifier_pattern}|später|danach|nach|zuvor|vorher))?"
        r")"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class DETimeUnitRelativeParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        full_match = match.group(0).lower()
        if full_match.startswith("vor "):
            num = constants.parse_number_pattern(match.group(1))
            unit_str = match.group(2).lower()
            unit = constants.TIME_UNIT_DICTIONARY[unit_str]
            return ReferenceMoment.of(context.reference, {unit: -num})

        num_str = match.group(3)
        num = constants.parse_number_pattern(num_str) if num_str else 1
        unit_str = match.group(5).lower()
        if unit_str not in constants.TIME_UNIT_DICTIONARY:
            return None
        unit = constants.TIME_UNIT_DICTIONARY[unit_str]

        modifier = (match.group(4) or match.group(6) or "").lower()
        if not modifier:
            return None

        if re.search(r"letzte|vergangene|zuvor|vorher", modifier):
            num = -num
        elif re.search(r"diese", modifier):
            num = 0

        return ReferenceMoment.of(context.reference, {unit: num})
