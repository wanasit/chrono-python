#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import unicodedata
from ..parser import Parser
from ..parser import ParsedResult
from ..parser import ParsedComponent

from datetime import datetime
from .util import date_exist
from .util import find_closest_year
from .util import normalize


class JPStandartDateFormatParser(Parser):
    def pattern(self):
        return '(((平成|昭和)?([0-9]{2,4}|[０-９]{6,12})年|今年|去年|来年)|[^年]|^)([0-9]{1,2}|[０-９]{3,6}|今|先|来)月([0-9]{1,2}|[０-９]{3,6})日\s*(?:\((?:日|月|火|水|木|金|土)\))?'

    def extract(self, text, ref_date, match, options):

        result = ParsedResult()
        result.index = match.start()
        result.text = match.group(0)

        day = int(normalize(match.group(6)))
        month = ref_date.month
        if match.group(5) == '先':
            month -= 1
        elif match.group(5) == '来':
            month += 1
        elif match.group(5) != '今':
            month = int(normalize(match.group(5)))

        year = None
        if match.group(4):
            year = int(normalize(match.group(4)))

            if match.group(3) == '平成':
                year += 1989
            elif match.group(3) == '昭和':
                year += 1926
        else:

            if match.group(5) == '今年':
                year = ref_date.year
            elif match.group(5) == '去年':
                year = ref_date.year - 1
            elif match.group(5) == '来年':
                year = ref_date.year + 1
            else:
                result.index += len(match.group(1))
                result.text = result.text[len(match.group(1)):]

        result.start = ParsedComponent(month=month, day=day)
        if year:
            if not date_exist(year, month, day): return None
            result.start.assign('year', year)
        else:
            year = find_closest_year(ref_date=ref_date, month=month, day=day)
            if year is None: return None

            result.start.imply('year', year)

        return result
