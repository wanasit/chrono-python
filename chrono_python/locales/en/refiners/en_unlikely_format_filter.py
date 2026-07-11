import re
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners import Filter
from chrono_python.types import ParsedResult


class ENUnlikelyFormatFilter(Filter):
    """
    Filters out unlikely date/time matches in English, such as:
    - "may" (when it is likely used as a modal verb instead of the month of May)
    - "the second" (when it is likely used as an ordinal or unit of time, followed by other text)
    """

    def is_valid(self, context: ParsingContext, result: ParsedResult) -> bool:
        text = result.text.strip()

        # If the result consists of the whole text (e.g. "2024", "May", etc),
        # then it is unlikely to be a date.
        if text == context.text.strip():
            return True

        # In English, the word "may" is a month name, but it is also a modal verb.
        # Check if the text before "may" follows some allowed patterns.
        if text.lower() == "may":
            text_before = context.text[:result.index].rstrip()
            if not re.search(r'\b(in)$', text_before, re.IGNORECASE):
                return False

        # In English, "the second" could refer to the ordinal number or timeunit.
        if text.lower().endswith("the second"):
            text_after = context.text[result.index + len(result.text):].lstrip()
            if len(text_after) > 0:
                return False

        return True
