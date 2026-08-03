import re
from chrono_python.common.refiners.abstract_merge_date_range_refiner import AbstractMergeDateRangeRefiner


class DEMergeDateRangeRefiner(AbstractMergeDateRangeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(bis\s*zum|bis\s*zu|bis|-|–|~)\s*$", re.IGNORECASE)
