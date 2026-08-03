import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.vi import constants
from chrono_python.types import Moment, ReferenceMoment
from chrono_python.utils import patterns


def compile_pattern() -> re.Pattern:
    casual_unit_pattern = (
        f"(?:{constants.NUMBER_PATTERN}\\s{{0,5}})?"
        f"(?:{patterns.match_any(constants.TIME_UNIT_DICTIONARY)})"
    )
    return re.compile(
        rf"(này|trước|qua|sau|tới|tiếp)\s*({casual_unit_pattern})"
        rf"|({casual_unit_pattern})\s*(này|trước|qua|sau|tới|tiếp)"
        r"(?=\W|$)",
        re.IGNORECASE,
    )


class VITimeUnitCasualRelativeParser(AbstractParserWithWordBoundary):
    def __init__(self):
        super().__init__()
        self._pattern = compile_pattern()

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        modifier = (match[1] or match[4] or "").lower()
        unit_text = (match[2] or match[3] or "").lower()

        duration = constants.parse_duration(unit_text)
        if not duration:
            unit = constants.TIME_UNIT_DICTIONARY.get(unit_text)
            if not unit:
                return None
            duration = {unit: 1}

        if modifier in ("trước", "qua"):
            duration = {k: -v for k, v in duration.items()}

        return ReferenceMoment.of(context.reference, duration)


class VITimeUnitRelativeParser(VITimeUnitCasualRelativeParser):
    pass
