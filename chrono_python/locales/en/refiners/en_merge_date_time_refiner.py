import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class ENMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    """
    Merging date-only result and time-only result.
    This implementation handles English connecting phrases:
    - 2020-02-13 at 6pm
    - Tomorrow after 7am
    """

    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(T|at|after|before|on|of|,|-|\.|∙|:)?\s*$", re.IGNORECASE)
