import re
from chrono_python.common.refiners.abstract_merge_date_range_refiner import AbstractMergeDateRangeRefiner


class ITMergeDateRangeRefiner(AbstractMergeDateRangeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(a|al|-|–|fino\s*a|fino\s*al)\s*$", re.IGNORECASE)
