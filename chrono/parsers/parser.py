#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from datetime import datetime


from ..parsed_result import ParsedResult
from ..parsed_result import ParsedComponent

class Parser(object):

    def pattern(self):
        return '$'

    def extract(self, text, ref_date, match, options):
        return None


    def execute(self, text, ref_date, options):

        results = []
        pattern = re.compile(self.pattern())

        for match in pattern.finditer(text):

            result = self.extract(text, ref_date, match, options);
            if result: results.append(result);

        return results