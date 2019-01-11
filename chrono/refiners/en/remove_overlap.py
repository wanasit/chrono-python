#!/usr/bin/env python
# -*- coding: utf8 -*-

from ..refiner import Refiner
from ..refiner import ParsedResult
from ..refiner import ParsedComponent


class ENRemoveOverlapRefiner(Refiner):
    def refine(self, results, text, options):

        if len(results) < 2: return results

        filtered_results = []
        prev_result = results[0]

        for result in results[1:]:

            # If overlap, compare the length and discard the shorter one
            if result.index < prev_result.index + len(prev_result.text):
                if len(result.text) > len(prev_result.text):
                    prev_result = result
            else:
                filtered_results.append(prev_result)
                prev_result = result

        # The last one
        if prev_result:
            filtered_results.append(prev_result)

        return filtered_results
