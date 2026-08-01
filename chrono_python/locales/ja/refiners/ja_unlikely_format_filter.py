import re
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners import Filter
from chrono_python.types import ParsedResult

UNLIKELY_SUFFIX_PATTERN = re.compile(
    r'^(的|金|停止|保存|帰国|避難|休止|しのぎ|預[かけ]|払[い]?|借入|所得|退院|保育|利用|解雇|措置)'
)


class JAUnlikelyFormatFilter(Filter):
    """
    Filters out unlikely date/time matches in Japanese, such as:
    - "一時" when it is likely used to mean "temporary" or "at one time"
      instead of "1 o'clock".
    """

    def is_valid(self, context: ParsingContext, result: ParsedResult) -> bool:
        text = result.text.strip()

        if text == "一時":
            text_after = context.text[result.index + len(result.text):].lstrip()
            if UNLIKELY_SUFFIX_PATTERN.match(text_after):
                return False

        return True
