#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from ..parser import Parser
from ..parser import ParsedResult
from ..parser import ParsedComponent

from datetime import datetime

FIRST_REG_PATTERN = "((at|from|\W|^|T)\s*)([0-9]{1,2}|noon|midnight)((\.|\:|\：)([0-9]{2})((\.|\:|\：)([0-9]{2}))?)?(\s*(AM|PM))?(\W|$)"
SECOND_REG_PATTERN = "\s*(\-|\~|\〜|to|\?)\s*([0-9]{1,2})((\.|\:|\：)([0-9]{2})((\.|\:|\：)([0-9]{2}))?)?(\s*(AM|PM))?\)?"


class ENTimeExpressionParser(Parser):
    def pattern(self):
        return FIRST_REG_PATTERN

    def extract(self, text, ref_date, match, options):

        result = ParsedResult()
        result.start = ParsedComponent()
        result.start.imply('year', ref_date.year)
        result.start.imply('month', ref_date.month)
        result.start.imply('day', ref_date.day)

        hour = 0
        minute = 0
        second = 0
        meridiem = None

        if match.group(3).lower() == "noon":
            meridiem = 'pm'
            hour = 12
        elif match.group(3).lower() == "midnight":
            meridiem = 'am'
            hour = 0
        else:
            hour = int(match.group(3))

        if match.group(6):
            minute = int(match.group(6))
            if (minute >= 60): return None
        elif hour > 100:
            minute = hour % 100
            hour = hour / 100

        if match.group(9):
            second = int(match.group(9))
            if second >= 60: return None

        if match.group(11):
            if hour > 12: return None

            if match.group(11).lower() == 'am':
                meridiem = 'am'
                if hour == 12:
                    hour = 0

            if match.group(11).lower() == "pm":
                meridiem = 'pm'
                if hour != 12:
                    hour += 12

        if hour >= 24: return None
        if hour >= 12: meridiem = 'pm'

        result.text = match.group(0)
        result.text = result.text[len(match.groups()[0]):len(result.text) -
                                  len(match.groups()[-1])]
        result.index = match.start() + len(match.group(1))

        result.start.assign('hour', hour)
        result.start.assign('minute', minute)
        result.start.assign('second', second)

        if meridiem:
            result.start.assign('meridiem', meridiem)

        second_pattern = re.compile(SECOND_REG_PATTERN, re.IGNORECASE)

        match = second_pattern.match(text[result.index + len(result.text):])
        if not match:
            if re.match('^\d+$', result.text): return None
            return result

        hour = int(match.group(2))
        minute = 0
        second = 0
        meridiem = None

        if match.group(5):

            minute = int(match.group(5))
            if minute >= 60: return None

        elif hour > 100:
            minute = hour % 100
            hour = hour / 100

        if match.group(8):
            second = int(matcher.group(8))
            if second >= 60: return None

        if match.group(10):

            if hour > 12: return None
            if match.group(10).lower() == "am":
                meridiem = 'am'
                if hour == 12:
                    hour = 0  #!!!!!

            if match.group(10).lower() == "pm":
                meridiem = 'pm'
                if hour != 12: hour += 12

            if not result.start.is_certain('meridiem'):

                if meridiem == 'am':

                    result.start.imply('meridiem', 'am')

                    if result.start.get('hour') == 12:
                        result.start.assign('hour', 0)

                if meridiem == 'pm':

                    result.start.imply('meridiem', 'pm')

                    if result.start.get('hour') != 12:
                        result.start.assign('hour',
                                            result.start.get('hour') + 12)

        if hour >= 24: return None
        if hour >= 12: meridiem = 'pm'

        result.text = result.text + match.group()
        result.end = result.start.copy()

        result.end.assign('hour', hour)
        result.end.assign('minute', minute)
        result.end.assign('second', second)

        if meridiem:
            result.end.assign('meridiem', meridiem)

        return result
