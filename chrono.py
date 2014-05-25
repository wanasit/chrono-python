#!/usr/bin/env python
# -*- coding: utf8 -*-

import options

from parsed_result import ParsedResult
from parsed_result import ParsedComponent

from parsers.parser import Parser

class Chrono:

    def __init__(self, options):
        self.options = options
        self.parsers = [parser_cls() for parser_cls in options.parser_classes]

    def parse(self, text, ref_date, options):

        results = []
        for parser in self.parsers:
            results += parser.execute(text, ref_date, options)

        return results

shared_instance = Chrono( options.standard_options() )


def parse(text, ref_date=None, options = None):
    results = shared_instance.parse(text, ref_date, options)
    return results


def parse_date(text, ref_date=None, timezone = None):

    results = shared_instance.parse(text, ref_date, options)

    if len(results) == 0 : return None
    return results[0].start_date
