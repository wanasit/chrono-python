#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from ..parser import Parser
from ..parser import ParsedResult
from ..parser import ParsedComponent

from datetime import datetime
from .util import month_index
from .util import date_exist
from .util import find_closest_year

FULL_PATTERN = "(\W|^)((Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s*,?\s*)?(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)\s*(([0-9]{1,2})(st|nd|rd|th)?\s*(to|\-)\s*)?([0-9]{1,2})(st|nd|rd|th)?(,)?(\s*[0-9]{4})(\s*BE)?(\W|$)"
SHORT_PATTERN = "(\W|^)((Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s*,?\s*)?(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)\s*(([0-9]{1,2})(st|nd|rd|th)?\s*(to|\-)\s*)?([0-9]{1,2})(st|nd|rd|th)?([^0-9]|$)"


class ENMonthNameMiddleEndianParser(Parser):
    def pattern(self):
        return SHORT_PATTERN

    def extract(self, text, ref_date, match, options):

        index = match.start()
        month = month_index(match.group(4))
        day = int(match.group(9))
        year = None

        pattern = re.compile(FULL_PATTERN, re.IGNORECASE)
        if pattern.match(text[match.start():]):
            match = pattern.match(text[match.start():])
            year = int(match.group(12))

            if match.group(13):
                year -= 543

        text = match.group(0)
        text = text[len(match.groups()[0]):len(text) - len(match.groups()[-1])]

        result = ParsedResult()
        result.index = index + len(match.groups()[0])
        result.text = text
        result.start = ParsedComponent(month=month, day=day)

        if year:
            if not date_exist(year, month, day): return None
            result.start.assign('year', year)
        else:
            year = find_closest_year(ref_date=ref_date, month=month, day=day)
            if year is None: return None

            result.start.imply('year', year)

        if match.group(5):

            start_day = int(match.group(6))
            result.end = result.start.copy()
            result.start.assign('day', start_day)

        return result
