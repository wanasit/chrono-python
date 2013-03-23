#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import inspect
import importlib

from datetime import datetime

from parsers import DateParser
from parsers import ParsingResult

supported_languages = ['en','th','jp']

class IntegratedDateParser(DateParser):
    
    parser_index = 0
    parser_classes   = []
    parser_instances = []
    
    def __init__(self, text, reference_date=None, timezone=None):
        
        
        #Loading the module for each language
        for lang in supported_languages:
            
            module = importlib.import_module('parsers.'+lang)
            if module is None : continue
            
            #Loading the DateParser class from each module
            parser_classes = inspect.getmembers(module, lambda x: inspect.isclass(x) and issubclass(x, DateParser))
            parser_classes = [pc[1] for pc in parser_classes if pc[1] != IntegratedDateParser]
            
            self.parser_classes = self.parser_classes + parser_classes
            
        #Instantiate all parsers
        for parser_class in self.parser_classes:
            parser = parser_class(text, reference_date, timezone)
            self.parser_instances.append(parser)
    
    def parse(self):
        
        if self.parser_index >= len(self.parser_instances) :
            self.parsing_finished = True;
            return
        
        current_parser = self.parser_instances[self.parser_index];
        result         = current_parser.parse()
        
        if result :
            self.parsing_results = IntegratedDateParser.insert_result (self.parsing_results, result)
            
        if current_parser.parsing_finished :
            self.parser_index += 1
        
        return result
    
    
    @staticmethod
    def insert_result(results, new_result):
        
        original_results = results[:]
        results          = results[:]
        
        #Find the place in the array that this result is belong to
        # Change to binary search later.
        index = 0
        while index < len(results) and results[index].index < new_result.index :
            index += 1
        
        if index < len(results) :
            
            #Checking conflict with other results on the RIGHT side
            overlapped_index = index;
            while overlapped_index < len(results) and results[overlapped_index].index < (new_result.index + len(new_result.text)) :
            
                #Comapare length
                #If old value is longer, discard the new_result and skip the remaining operation
                if len(results[overlapped_index].text) >= len(new_result.text) : return original_results
                overlapped_index += 1;
            
            #remove all overlapped results
            results = results[:index] + results[overlapped_index:]
        
        if index-1 >= 0 :
            
            #Checking conflict with other results on the LEFT side
            old_result = results[index-1]
            
            if new_result.index < (old_result.index + len(old_result.text)) :
                
                #Comapare length
                # If old value is longer, discard the new_result
                # Otherwise, discard the old_result
                if len(old_result.text) >= len(new_result.text) : return original_results
                else :
                    results.pop(index-1);
                    index = index-1
            
        results.insert(index, new_result)
        return results
        
        
        
    
    