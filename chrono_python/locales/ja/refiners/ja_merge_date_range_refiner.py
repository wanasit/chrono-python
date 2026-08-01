import re
from chrono_python.common.refiners.abstract_merge_date_range_refiner import AbstractMergeDateRangeRefiner


class JAMergeDateRangeRefiner(AbstractMergeDateRangeRefiner):
    """
    Merges two parsed Japanese dates separated by range indicators.
    
    Examples of patterns matched and merged:
    - "2月11日ー2月13日"
    - "水曜日から日曜日"
    - "2020/02/13〜2020/02/15"
    """

    def pattern_between(self) -> re.Pattern:
        return re.compile(r'^\s*(から|－|ー|-|～|~|〜)\s*$', re.IGNORECASE)
