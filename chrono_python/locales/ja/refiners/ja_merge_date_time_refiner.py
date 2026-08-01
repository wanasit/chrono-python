import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class JAMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    """
    Merging date-only result and time-only result for Japanese.
    - 2012年3月31日の午後3時
    - 7月27日 10時
    """

    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(の)?\s*$", re.IGNORECASE)
