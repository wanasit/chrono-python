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
        pattern = re.compile(self.pattern(), re.IGNORECASE)

        offset = 0
        
        while len(text[offset:]) > 0:

            result = None
            match = pattern.search(text[offset:])

            if match:
                result = self.extract(text[offset:], ref_date, match, options)

            if result: 
                result.index += offset
                results.append(result)
                
                offset += result.index + len(result.text)
            else:
                offset += 1

        return results
