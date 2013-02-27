#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from datetime import datetime
from parsers import DateParser
from parsers import ParsingResult

class ENDateParserISO (DateParser):
    
    def pattern(self):
        return '([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})(\W|$)'
    
    
    def extract(self, index):
        
        match = re.match(self.pattern(), self.original_text[index:])
        if match is None : return None
        
        text = match.group(0)[: len(match.group(0)) - len(match.group(4)) ]
        
        try:
            date = datetime.strptime(text, '%Y-%m-%d')
        except ValueError, e:
            return None
        
        return ParsingResult(
            index=index,
            text=text,
			reference_date=self.reference_date,
            start= {
                'day'   : date.day,
                'month' : date.month,
                'year'  : date.year,
                }
        )
        




    


