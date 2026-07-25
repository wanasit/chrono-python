import re
from chrono_python import chrono
from chrono_python.chrono import ParsingContext
from chrono_python.common.refiners.abstract_merging_refiner import AbstractMergingRefiner
from chrono_python.types import ParsedResult, ReferenceMoment
from chrono_python.locales.en import constants
from chrono_python.common.types import CivilTimeComponent, CivilTimeMoment

def has_implied_earlier_reference_date(result: ParsedResult) -> bool:
    return re.search(r'\s+(before|from)$', result.text, re.IGNORECASE) is not None

def has_implied_later_reference_date(result: ParsedResult) -> bool:
    return re.search(r'\s+(after|since)$', result.text, re.IGNORECASE) is not None


class ENMergeRelativeFollowByDateRefiner(AbstractMergingRefiner):
    """
    Merges a relative date/time followed by an absolute date.
    - [2 weeks before] [2020-02-13]
    - [2 days after] [next Friday]
    """

    def should_merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> bool:
        if not re.match(r'^\s*$', text_between):
            return False

        if not has_implied_earlier_reference_date(current_result) and not has_implied_later_reference_date(current_result):
            return False

        next_moment = next_result.moment
        if not isinstance(next_moment, CivilTimeMoment):
            return False

        return (
            next_moment.get(CivilTimeComponent.DAY) is not None
            and next_moment.get(CivilTimeComponent.MONTH) is not None
            and next_moment.get(CivilTimeComponent.YEAR) is not None
        )

    def merge_results(self, text_between: str, current_result: ParsedResult, next_result: ParsedResult, context: ParsingContext) -> ParsedResult:
        duration = constants.parse_duration(current_result.text) or {}
        if has_implied_earlier_reference_date(current_result):
            duration = {k: -v for k, v in duration.items()}

        moment = ReferenceMoment(next_result.moment, duration)
        new_text = current_result.text + text_between + next_result.text
        return context.create_parsed_result(current_result.index, current_result.index + len(new_text), moment)
