import re
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.types import ParsedResult, ReferenceMoment
from chrono_python.locales.it import constants


def is_positive_following_reference(result: ParsedResult) -> bool:
    return re.match(r"^[+-]", result.text) is not None


def is_negative_following_reference(result: ParsedResult) -> bool:
    return re.match(r"^-", result.text) is not None


class ITMergeRelativeAfterDateRefiner(AbstractMergingRefiner):
    """
    Merges a relative date/time that comes after an absolute date.
    - [2020-02-13] [+2 settimane]
    - [martedì prossimo] [+10 giorni]
    """

    def should_merge_results(
        self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext
    ) -> bool:
        if not re.match(r"^\s*$", text_between):
            return False

        return is_positive_following_reference(next_result) or is_negative_following_reference(next_result)

    def merge_results(
        self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext
    ) -> ParsedResult:
        duration = constants.parse_duration(next_result.text) or {}
        if is_negative_following_reference(next_result):
            duration = {k: -v for k, v in duration.items()}

        moment = ReferenceMoment.of(current_result.moment, duration)
        new_text = current_result.text + text_between + next_result.text
        return context.create_parsed_result(current_result.index, current_result.index + len(new_text), moment)
