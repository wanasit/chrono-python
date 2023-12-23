#!/usr/bin/env python
# -*- coding: utf8 -*-

from ..parsed_result import ParsedResult
from ..parsed_result import ParsedComponent
from .refiner import Refiner


class Filter(Refiner):
    def verify(self, result):
        return True

    def refine(self, results, text, options):
        return [r for r in results if self.verify(r)]
