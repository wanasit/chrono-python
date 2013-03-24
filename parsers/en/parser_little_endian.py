#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from datetime import datetime
from parsers import DateParser
from parsers import ParsingResult

FULL_PATTERN    = '((Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s*,?\s*)?([0-9]{1,2})(st|nd|rd|th)?(\s*(to|\-)?\s*([0-9]{1,2})(st|nd|rd|th)?)?\s*(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)(\s*[0-9]{2,4})(\s*BE)?(\W|$)'
SHORT_PATTERN   = '((Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s*,?\s*)?([0-9]{1,2})(st|nd|rd|th)?(\s*(to|\-)?\s*([0-9]{1,2})(st|nd|rd|th)?)?\s*(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)(\W|$)'

MONTH_MAPPING = {"january":1,"jan":1,"february":2,"feb":2,"march":3,"mar":3,"april":4,"apr":4,"may":5,"june":6,"jun":6,"july":7,"jul":7,"august":8,"aug":8,"september":9,"sep":9,"october":10,"oct":10,"november":11,"nov":11,"december":12,"dec":12}

class ENDateParserLittleEndian (DateParser):
    
    def pattern(self):
        return SHORT_PATTERN
    
    def extract(self, index):

        if len(self.parsing_results) > 0 :
            last_result = self.parsing_results[-1]
            if index < last_result.index + len(last_result.text):
                return None
        
        implied_components = []
        match = re.match(FULL_PATTERN, self.original_text[index:], flags=re.IGNORECASE)
        if match :

            text = match.group(0)[: len(match.group(0)) - len(match.group(12))]
            year = int(match.group(10))
            
            if year < 100:
                if year > 50 :
                    year = year + 2500 - 543 #BE SHORT
                else :
                    year = year + 2000  #AD SHORT
            elif match.group(11):
                year = year - 543 #BE FULL (Explicit)
            elif year > 2300:
                year = year - 543 #BE FULL 
            
            month = MONTH_MAPPING[match.group(9).lower()]
            day   = int(match.group(3))
            
            try:
                date = datetime(year,month,day)
            except ValueError, e:
                return None
            
        else :
            match = re.match(SHORT_PATTERN, self.original_text[index:], flags=re.IGNORECASE)
            if match is None : return None
            
            text = match.group(0)[: len(match.group(0)) - len(match.group(10))]

            month = MONTH_MAPPING[match.group(9).lower()]
            day   = int(match.group(3))
            
            implied_components.append("year")
            
            try:
                date = datetime(self.reference_date.year, month, day)
            except ValueError, e:
                return None
            
            
            this_year = date.replace( year = self.reference_date.year)  
            last_year = date.replace(year = self.reference_date.year - 1)
            next_year = date.replace(year = self.reference_date.year + 1)
                
            if this_year:
                    
                date = this_year
                    
                if abs(this_year - self.reference_date) > abs(last_year - self.reference_date):
                    date = last_year
                elif abs(this_year - self.reference_date) > abs(next_year - self.reference_date): 
                    date = next_year
            else:
                if abs(next_year - self.reference_date) > abs(last_year - self.reference_date):
                    date = last_year
                else:
                    date = next_year
                
        if match.group(7):
            
            #Text text can be 'range' value. Such as '12 - 13 January 2012'
            end_day = int(match.group(7))
            start_day = int(match.group(3))
            
            date = date.replace(day=start_day)
            if date is None : return None
            
            end_date = date.replace(day=end_day)
            if end_date is None : return None
            
            return ParsingResult(
                                 index=index,
                                 text=text, 
                                 start = {
                                         'day'   : date.day,
                                         'month' : date.month,
                                         'year'  : date.year,
                                         }, 
                                 end =   {
                                         'day'   : end_date.day,
                                         'month' : end_date.month,
                                         'year'  : end_date.year,
                                         },
                                 reference_date=self.reference_date,
                                 implied_components=implied_components)
            
        else:
            
            return ParsingResult(
                                 index=index,
                                 text=text, 
                                 start = {
                                         'day'   : date.day,
                                         'month' : date.month,
                                         'year'  : date.year,
                                         },
                                 reference_date=self.reference_date,
                                 implied_components=implied_components)
            
            
            
        


