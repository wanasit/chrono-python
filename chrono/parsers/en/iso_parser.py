#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from .util import date_exist

from ..parser import Parser
from ..parser import ParsedResult
from ..parser import ParsedComponent

from datetime import datetime


class ENInternationalStandardParser(Parser):
    def pattern(self):
        return '(^|\W)([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})(\W|T|$)'

    def extract(self, text, ref_date, match, options):

        text = match.group(0)
        text = text[len(match.groups()[0]):len(text) - len(match.groups()[-1])]

        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))

        if not date_exist(year, month, day): return None

        result = ParsedResult()
        result.index = match.start() + len(match.groups()[0])
        result.text = text
        result.start = ParsedComponent(year=year, month=month, day=day)

        return result
