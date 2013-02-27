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
            insert_result (self.parsing_results, result);
            
        if current_parser.parsing_finished :
            self.parser_index += 1
        
        return result
    
    
    @staticmethod
    def insert_result(results, new_result):
        
        pass
        
        
    
    