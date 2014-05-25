#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from ..parser import Parser
from ..parser import ParsedResult

from datetime import datetime


class ENInternationalStandardParser (Parser):

    def pattern(self):
        return '([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})(T|\W|$)'

    def extract(self, text, ref_date, match, options):

        text = match.group(0)[: len(match.group(0)) - len(match.group(4)) ]

        try:
            date = datetime.strptime(text, '%Y-%m-%d')
        except ValueError, e:
            return None

        result = ParsedResult()
        result.index = match.start()
        result.text  = text
        return result
