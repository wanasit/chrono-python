#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from .util import date_exist

from ..parser import Parser
from ..parser import ParsedResult
from ..parser import ParsedComponent

from datetime import datetime


class ENSlashDateFormatParser(Parser):
    def pattern(self):
        return '((?:\W|^)(Sun|Sunday|Mon|Monday|Tue|Tuesday|Wed|Wednesday|Thur|Thursday|Fri|Friday|Sat|Saturday)?\s*\,?\s*)([0-9]{1,2})/([0-9]{1,2})(/([0-9]{4}|[0-9]{2}))?(\W|$)'

    def extract(self, text, ref_date, match, options):

        text = match.group(0)
        text = text[len(match.groups()[0]):len(text) - len(match.groups()[-1])]

        year = ref_date.year
        month = int(match.group(3))
        day = int(match.group(4))

        if month < 1 or month > 12: return None
        if day < 1 or day > 31: return None

        if match.group(6):
            year = int(match.group(6))
            if year < 100:
                if year > 50:
                    year = year + 2500 - 543  #BE
                else:
                    year = year + 2000

            elif year > 2500:
                year = year - 543  #BE

        if not date_exist(year, month, day): return None

        result = ParsedResult()
        result.index = match.start() + len(match.groups()[0])
        result.text = text
        result.start = ParsedComponent(year=year, month=month, day=day)

        return result