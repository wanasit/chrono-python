#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from datetime import datetime
from datetime import timedelta

from parsers import DateParser
from parsers import ParsingResult

class ENDateParserGeneral (DateParser):
    
    def pattern(self):
        
        return '(today|tomorrow|yesterday|last\s*night|([1-9]+)\s*day(s)\s*ago)(\W|$)'
    
    def extract(self, index):
        
        match = re.match(self.pattern(), self.original_text[index:])
        if match is None : return None
        
        text = match.group(0)[: len(match.group(0)) - len(match.group(4)) ]
        
        date = None
        lowercase_text = text.lower()
        
        if lowercase_text == 'today':
            date = self.reference_date
        elif lowercase_text == 'tomorrow':
            date = self.reference_date + timedelta(days = 1)
        elif lowercase_text == 'yesterday' :
            date = self.reference_date - timedelta(days = 1)
        elif re.match('last',lowercase_text) :
            date = self.reference_date - timedelta(days = 1)
        elif re.search('ago', lowercase_text) :
            days_ago = int(match.group(2))
            date = self.reference_date - timedelta(days = days_ago)
        else:
            pass
            #self.parsing_index += len(lowercase_text)
            #print 'Move,....'+lowercase_text
            #date = self.reference_date
            #text = ''
        
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
        
    def find_time(self, result):
            
        super(ENDateParserGeneral, self).find_time(result)
            
        #detect keyword 'night'
        if re.search('night', result.text) :
                
            #Set the time to midnight
            if 'hour' not in result.start :
                result.start['day'] = result.start['day'] + 1;
                result.start['hour'] = 0
                result.start['minute'] = 0
                result.start['second'] = 0
                    
            else:
                    
                if result.start['hour'] > 6 and result.start['hour'] < 12 : # AM -> PM
                    result.start['hour'] = result.start['hour']+12
                    
                if result.end and result.end['hour'] > 6 and result.end['hour'] < 12 : # AM -> PM
                    result.end['hour'] = result.end['hour']+12
                    
                
            
        



