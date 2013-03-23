#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from datetime import datetime
from parsers import DateParser
from parsers import ParsingResult

class ENDateParserSlash (DateParser):
    
    def pattern(self):
        return '(\W|^)([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{4}|[0-9]{2})(\W|$)'
    
    def extract(self, index):
        
        if len(self.parsing_results) > 0 :
            last_result = self.parsing_results[-1]
            if index < last_result.index + len(last_result.text):
                return None
        
        match = re.match(self.pattern(), self.original_text[index:])
        if match is None : return None
        
        #remove (\W|^) and (\W|$) at the end of pattern
        text = match.group(0)[len(match.group(1)): len(match.group(0)) - len(match.group(5))]
        index += len(match.group(1))
        
        year = int(match.group(4))
        
        if year < 100:
            if year > 50 :
                year = year + 2500 - 543 #BE SHORT
            else :
                year = year + 2000  #AD SHORT
                
        elif year > 2300:
            year = year - 543 #BE FULL
        
        tmp_text = match.group(2) +'/' + match.group(3) +'/'+ str(year)
        
        try:
            date = datetime.strptime(tmp_text, '%m/%d/%Y')
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
        



    


