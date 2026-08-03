import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class SVMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(T|kl|kl\.|klockan|på|om|vid|,|-)?\s*$", re.IGNORECASE)
