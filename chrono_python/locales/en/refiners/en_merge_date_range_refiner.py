import re
from chrono_python.common.refiners.abstract_merge_date_range_refiner import AbstractMergeDateRangeRefiner


class ENMergeDateRangeRefiner(AbstractMergeDateRangeRefiner):
    """
    Merges two parsed English dates separated by range indicators.
    
    Examples of patterns matched and merged:
    - "2020-02-13 to 2020-02-15"
    - "Wednesday - Friday"
    - "July 1st through July 4th"
    - "Dec 30 until Jan 5"
    """

    def pattern_between(self) -> re.Pattern:
        return re.compile(r'^\s*(to|-|–|until|through|till)\s*$', re.IGNORECASE)
