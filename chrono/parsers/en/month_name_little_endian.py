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


class ENMonthNameLittleEndianParser(Parser):
    def pattern(self):
        return '(\W|^)((Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s*,?\s*)?([0-9]{1,2})(st|nd|rd|th)?(\s*(to|\-|\s)\s*([0-9]{1,2})(st|nd|rd|th)?)?\s*(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)((\s*[0-9]{2,4})(\s*BE)?)?(\W|$)'

    def extract(self, text, ref_date, match, options):

        text = match.group(0)
        text = text[len(match.groups()[0]):len(text) - len(match.groups()[-1])]

        month = month_index(match.group(10))
        day = int(match.group(4))

        year = None
        if match.group(11):
            year = int(match.group(12))

            if year < 100:
                year = year + 2000
            elif match.group(13):
                year = year - 543

        result = ParsedResult()
        result.index = match.start() + len(match.groups()[0])
        result.text = text
        result.start = ParsedComponent(month=month, day=day)

        if year:
            if not date_exist(year, month, day): return None
            result.start.assign('year', year)
        else:
            year = find_closest_year(ref_date=ref_date, month=month, day=day)
            if year is None: return None

            result.start.imply('year', year)

        if match.group(8):
            endDay = int(match.group(8))
            result.end = ParsedComponent(year=year, month=month, day=endDay)

        return result
