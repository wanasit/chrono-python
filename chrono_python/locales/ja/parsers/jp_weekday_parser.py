import re
from chrono_python import chrono
from chrono_python.locales.ja.constants import WEEKDAY_OFFSET
from chrono_python.utils.weekdays import create_parsing_components_at_weekday
from chrono_python.types import Moment

# Pattern matching Japanese weekdays with optional prefixes (e.g., 前の火曜日, 今週土曜)
PATTERN = re.compile(
    r'(?:(前の|次の|今週))?(' + '|'.join(WEEKDAY_OFFSET.keys()) + r')(?:曜日|曜)',
    re.IGNORECASE
)


class JPWeekdayParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        prefix = match.group(1) or ""
        weekday_word = match.group(2)

        offset = WEEKDAY_OFFSET.get(weekday_word)
        if offset is None:
            return None

        modifier = None
        if "前の" in prefix:
            modifier = "last"
        elif "次の" in prefix:
            modifier = "next"
        elif "今週" in prefix:
            modifier = "this"

        return create_parsing_components_at_weekday(context.reference, offset, modifier)
