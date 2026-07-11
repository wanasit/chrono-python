import re

from chrono_python.chrono import Parser, ParsingContext
from chrono_python.locales.ja.constants import WEEKDAY_OFFSET
from chrono_python.common.weekdays import create_parsing_components_at_weekday

_PATTERN = re.compile(
    r"(?:\(|\（)(?P<weekday>" + "|".join(WEEKDAY_OFFSET.keys()) + r")(?:\)|\）)",
    re.IGNORECASE
)

class JPWeekdayWithParenthesesParser(Parser):
    """
    Weekday with parentheses in Japanese
    For examples:
    - (水)
    - （土）
    """
    
    def pattern(self) -> re.Pattern:
        return _PATTERN
        
    def extract(self, context: ParsingContext, match: re.Match):
        day_of_week = match.group("weekday")
        offset = WEEKDAY_OFFSET.get(day_of_week)
        if offset is None:
            return None
            
        return create_parsing_components_at_weekday(context.reference, offset)
