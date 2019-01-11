#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime

from . import options

from .parsed_result import ParsedResult
from .parsed_result import ParsedComponent


class Chrono:
    def __init__(self, options):
        self.options = options
        self.parsers = options.parsers[:]
        self.refiners = options.refiners[:]

    def parse(self, text, ref_date, options):

        if ref_date is None: ref_date = datetime.now()

        results = []
        for parser in self.parsers:
            sub_results = parser.execute(text, ref_date, options)
            sub_results = self.refine_results(sub_results, text, options)
            results += sub_results

        results = sorted(results, key=lambda x: x.index)
        results = self.refine_results(results, text, options)
        return results

    def refine_results(self, results, text, options):

        for refiner in self.refiners:
            results = refiner.refine(results, text, options)

        return results


shared_instance = Chrono(options.standard_options())


def parse(text, ref_date=None, options=None):
    results = shared_instance.parse(text, ref_date, options)
    return results


def parse_date(text, ref_date=None, timezone=None):

    results = shared_instance.parse(text, ref_date, options)

    if len(results) == 0: return None
    return results[0].start.date()
