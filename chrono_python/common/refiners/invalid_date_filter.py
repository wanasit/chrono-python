from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_filter import Filter
from chrono_python.types import ParsedResult, ParsedRangeResult


class InvalidDateFilter(Filter):
    """
    Filters out parsed results that have invalid calendar dates (e.g. February 30th).
    """

    def is_valid(self, context: ParsingContext, result: ParsedResult) -> bool:
        if not result.moment.is_valid_date():
            return False
        if isinstance(result, ParsedRangeResult) and not result.end.is_valid_date():
            return False
        return True
