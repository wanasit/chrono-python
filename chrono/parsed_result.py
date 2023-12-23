#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime


class ParsedComponent():
    def __init__(self,
                 year=None,
                 month=None,
                 day=None,
                 hour=None,
                 minute=None,
                 second=None):
        self.known_values = {}
        self.implied_values = {}

        if year: self.assign('year', year)
        if month: self.assign('month', month)
        if day: self.assign('day', day)

        self.imply('hour', 12)
        self.imply('minute', 0)
        self.imply('second', 0)

    def date(self):

        date = datetime.now()

        year = self.get('year')
        month = self.get('month')
        day = self.get('day')
        hour = self.get('hour')
        minute = self.get('minute')
        second = self.get('second')

        return date.replace(year, month, day, hour, minute, second, 0)

    def is_certain(self, component):
        return component in self.known_values

    def assign(self, component, value):
        if component in self.implied_values:
            del self.implied_values[component]
        self.known_values[component] = value

    def imply(self, component, value):
        self.implied_values[component] = value

    def get(self, component):
        if component in self.known_values:
            return self.known_values[component]
        if component in self.implied_values:
            return self.implied_values[component]

    def copy(self):
        other = ParsedComponent()
        other.known_values = self.known_values.copy()
        other.implied_values = self.implied_values.copy()
        return other


class ParsedResult():
    def __init__(self):
        self.index = 0
        self.text = None
        self.start = None
        self.end = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        if self.end is None:
            return '<ParsedResult "{0}" : {1} >'.format(
                self.text, self.start.date())

        return '<ParsedResult "{0}" : {1} - {2} >'.format(
            self.text, self.start.date(), self.end.date())

    def copy(self):
        other = ParsedResult()
        other.index = self.index
        other.text = self.text

        if self.start:
            other.start = self.start.copy()

        if self.start:
            other.start = self.start.copy()

        return other
