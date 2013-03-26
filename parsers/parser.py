#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from datetime import datetime


class DateParser(object):
    
    original_text  = ''
    reference_date = datetime.now()
    reference_timezone = None
    
    parsing_index = 0
    parsing_text  = ''
    parsing_finished  = False
    parsing_results = []
    
    def __init__(self, text, reference_date=None, timezone=None):
        
        self.original_text = text
        self.reference_date = reference_date if reference_date else datetime.now()
        self.reference_timezone = timezone if timezone else None
        
        self.parsing_text = self.original_text
        self.parsing_index = 0
        self.parsing_finished = False
        self.parsing_results = []
    
    
    def pattern(self):
        return '.'
    
    
    def parse(self):
        """Countinue parsing the text, stop at the first detected pattern, and extract the information by self.extract(..)
        This function can return both [ParsingResult] or [None] depend on the extaction result"""
        
        match = re.search(self.pattern(), self.parsing_text, flags=re.IGNORECASE)

        if match is None:
            self.parsing_finished = True
            return None
        
        detected_index = self.parsing_index + match.start()
        result = self.extract(detected_index)
        
        if result:
            
            if len(self.parsing_results) > 0 :
                old_result = self.parsing_results[-1]
                merged_result = self.merge_overlap_results(result, old_result)
                
                if merged_result : result = merged_result 
            
            
            self.find_time(result)
            self.find_concordance(result)
            self.parsing_results.append(result)
        
        self.parsing_text = self.parsing_text[(match.start()+1):]
        self.parsing_index = detected_index+1
        
        return result
    
    
    def parse_all(self):
        """Parse the whole text by keep calling self.parse() untill """
        while not self.parsing_finished:
            self.parse()
        

    def extract(self, index):
        """Try extracting date information from the text at given index - return ParsingResult if success, None otherwise"""
        pass
    
    
    def find_time(self, result):
        """Find missing 'time' part of giving ParsingResult"""
        
        if ('hour' in result.start) and ( result.end is None or 'hour' not in result.end) :
            return
        
        SUFFIX_PATTERN = '\s*(at|T|on|from|\()?\s*([0-9]{1,2})((\.|\:|\Ôºö)([0-9]{1,2})((\.|\:|\Ôºö)([0-9]{1,2}))?)?(\s*(AM|PM))?';
        TO_SUFFIX_PATTERN = '\s*(\-|\~|\„Äú|to)?\s*([0-9]{1,2})((\.|\:|\Ôºö)([0-9]{1,2})((\.|\:|\Ôºö)([0-9]{1,2}))?)?(\s*(AM|PM))?\)?';
        
        
        if len(self.original_text) < result.index + len(result.text) :
            return;
        
        text  = self.original_text[ result.index + len(result.text) :]
        match = re.match(SUFFIX_PATTERN, text)
        if match is None : return None
        
        minute = 0
        second = 0
        hour   = int(match.group(2))
        
        if match.group(10) : # AM & PM
            if hour > 12 : return
            if match.group(10).lower() == "pm" : hour += 12
        
        if match.group(5): # minute
            minute = int(match.group(5))
            if minute >= 60: return
        
        if match.group(8): # second
            second = int(match.group(8))
            if second >= 60: return
        
        result.text = result.text + match.group(0)
        
        if 'hour' not in result.start :
            result.start['hour'] = hour
            result.start['minute'] = minute
            result.start['second'] = second
        
        text = text[len(match.group(0)):]
        match2 = re.match(TO_SUFFIX_PATTERN, text)
        
        if match2 is None:
            
            if result.end and 'hour' not in result.end :
                result.end['hour'] = hour
                result.end['minute'] = minute
                result.end['second'] = second
            
            return
        
        minute = 0
        second = 0
        hour   = int(match2.group(2))
        
        if match2.group(10) : # AM & PM
            if hour > 12 : return
            if match2.group(10).lower() == "pm" : hour += 12
            
            if match.group(10) is None :
                if result.start['hour'] <= 12 : 
                    if match2.group(10).lower() == "pm" :
                        result.start['hour'] = result.start['hour'] + 12
        
        if match2.group(5): # minute
            minute = int(match2.group(5))
            if minute >= 60: return
        
        if match2.group(8): # second
            second = int(match2.group(8))
            if second >= 60: return
        
        result.text = result.text + match2.group(0)
        
        if result.end is None:
            result.end = result.start.copy()
        
        result.end['hour'] = hour
        result.end['minute'] = minute
        result.end['second'] = second
             
    def find_concordance(self, result):
        """Find missing 'concordance' part of giving ParsingResult"""
        pass
    
    
    def merge_overlap_results(self, result1, result2):
        """Try merging two overlaping results - return new ParsingResult if success, None otherwise"""
        if result2.index < result1.index:
            result1, result2 = result2, result1
            
        if result1.end or result2.end : return None
        
        begin = result1.index + len(result1.text)
        end   = result2.index
        text_between = self.original_text[begin:end]
        OVERLAP_PATTERN = '^\s*(to|\-)\s*$'
        

        
        if re.match(OVERLAP_PATTERN, text_between, flags=re.IGNORECASE) is None:
            return None
        
        merged_text = result1.text + text_between + result2.text
        
        
        # If there is component implication, use the one with more confidence
        components_1 = result1.start
        components_2 = result2.start
        
        for component in result1.implied_components:
            if component not in result2.implied_components:
                components_1[component] = result2.start[component]
                
        for component in result2.implied_components:
            if component not in result1.implied_components:
                components_2[component] = result1.start[component]
        
        
        
        if result1.start_date < result2.start_date :
            
            return ParsingResult(index=result1.index, 
                                 text=merged_text, 
                                 start=result1.start, 
                                 end=result2.start, 
                                 reference_date=result1.reference_date())
        else:
            
            return ParsingResult(index=result1.index, 
                                 text=merged_text, 
                                 start=result2.start, 
                                 end=result1.start, 
                                 reference_date=result1.reference_date())
    

class ParsingResult:
    

    def __init__(self, index=0, text='', start=None, end=None, reference_date=None, concordance='', implied_components=[]):
        self._index = index
        self._text  = text
        self._start = start
        self._end   = end
        self._concordance    = concordance
        self._reference_date = reference_date
        self._implied = set(implied_components)
    
    @staticmethod
    def date_for_component(components):
        
        year    = components['year']
        month   = components['month']
        day     = components['day']
        hour    = components.get('hour', 12)
        minute  = components.get('minute',  0)
        second  = components.get('second',  0)
        
        return datetime(year,month,day,hour,minute,second)
    
    @property
    def implied_components(self):
        return self._implied
    
    @property
    def index(self):
        return self._index
    
    
    @property
    def text(self):
        return self._text
    
    def reference_date(self):
        return self._reference_date
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @property
    def start_date(self):
        
        if self.start is None:
            return None
        
        return ParsingResult.date_for_component(self.start)
    
    @property
    def end_date(self):
        
        if self.end is None:
            return None

        return ParsingResult.date_for_component(self.end)
    
    @property
    def concordance(self):
        return self._concordance
    
    


    
    
    