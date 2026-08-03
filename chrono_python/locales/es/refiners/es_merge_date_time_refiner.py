import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class ESMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(?:,|de|a\s*las|a)?\s*$", re.IGNORECASE)
