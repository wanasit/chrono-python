import re
from chrono_python.common.refiners.abstract_merge_date_time_refiner import AbstractMergeDateTimeRefiner


class ITMergeDateTimeRefiner(AbstractMergeDateTimeRefiner):
    def pattern_between(self) -> re.Pattern:
        return re.compile(r"^\s*(T|alle?|dopo\s*le|prima\s*delle?|,|-|\.|\∙|:)?\s*$", re.IGNORECASE)
