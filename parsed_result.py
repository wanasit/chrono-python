#!/usr/bin/env python
# -*- coding: utf8 -*-

class ParsedComponent():

    def __init__(self):
        self.known_values = {}
        self.implied_values = {}

    def date(self):
        return None

    def is_certain(self, component):
        pass

    def assign(self, component, value):
        pass

    def imply(self, component, value):
        pass

class ParsedResult():

    def __init__(self):
        
        self.index = 0
        self.text = None
        self.start = None
        self.end   = None
