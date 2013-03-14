#!/usr/bin/env python
# -*- coding: utf8 -*-

from parsers import IntegratedDateParser


def parse(text, ref=None, timezone = None):
    
    parser = IntegratedDateParser(text, ref, timezone)
    parser.parse_all()
    return parser.parsing_results


def parse_date(text, ref=None, timezone = None):

    results = parse(text, ref, timezone)

    if len(results) == 0 : return None
    return results[0].start_date
