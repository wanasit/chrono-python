#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import datetime

MONTH_NAMES = {
    "january":1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12
}


def date_exist(year, month, day):
    try:
        return datetime.date(year, month, day).day == day
    except ValueError:
        return False


def month_index(month_name):
    return MONTH_NAMES[month_name.lower()]
