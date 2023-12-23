#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import unicodedata
import datetime

MONTH_NAMES = {
    "january": 1,
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


def normalize(text):
    return unicodedata.normalize('NFKC', text)


def month_index(month_name):
    return MONTH_NAMES[month_name.lower()]


def date_exist(year, month, day):
    try:
        return datetime.date(year, month, day).day == day
    except ValueError:
        return False


def find_closest_year(ref_date, month, day):

    year = None

    if date_exist(ref_date.year, month, day):
        year = ref_date.year

    if date_exist(ref_date.year - 1, month, day):
        if year:
            tdelta1 = datetime.datetime(year, month, day) - ref_date
            tdelta2 = datetime.datetime(ref_date.year - 1, month,
                                        day) - ref_date
            if abs(tdelta2) < abs(tdelta1):
                year = ref_date.year - 1
        else:
            year = ref_date.year - 1

    if date_exist(ref_date.year + 1, month, day):
        if year:
            tdelta1 = datetime.datetime(year, month, day) - ref_date
            tdelta2 = datetime.datetime(ref_date.year + 1, month,
                                        day) - ref_date
            if abs(tdelta2) < abs(tdelta1):
                year = ref_date.year + 1
        else:
            year = ref_date.year + 1

    return year
