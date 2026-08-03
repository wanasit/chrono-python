import re
from chrono_python.common.refiners.abstract_merge_date_range_refiner import AbstractMergeDateRangeRefiner


class NLMergeDateRangeRefiner(AbstractMergeDateRangeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(tot|-)\s*$", re.IGNORECASE)
