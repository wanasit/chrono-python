import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class NLMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(om|na|voor|in de|,|-)?\s*$", re.IGNORECASE)
