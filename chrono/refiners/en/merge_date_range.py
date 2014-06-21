#!/usr/bin/env python
# -*- coding: utf8 -*-
import re

from ..refiner import Refiner
from ..refiner import ParsedResult
from ..refiner import ParsedComponent

class ENMergeDateRangeRefiner(Refiner):

    
    def refine(self, results, text, options):
        if len(results) < 2: return results
        
        merged_results = []
        prev_result = None
        curr_result = None
        i = 1

        while i < len(results):
            prev_result = results[i-1]
            curr_result = results[i]

            if prev_result.end is None and curr_result.end is None and is_able_to_merge(text, prev_result, curr_result):
                prev_result = merge_result(text, prev_result, curr_result)
                curr_result = None
                i += 1

            merged_results.append(prev_result)
            i += 1

        if curr_result:
            merged_results.append(curr_result)

        return merged_results


def merge_result(text, from_result, to_result):
    
    if from_result.start.date() > to_result.start.date():
        from_result, to_result = to_result, from_result
        
    result = from_result.copy()
    result.end = to_result.start;
        
    begin_index = min(from_result.index, to_result.index)
    end_index   = max(from_result.index + len(from_result.text), to_result.index + len(to_result.text))
    result.index = begin_index
    result.text  = text[begin_index : end_index]

    return result

def is_able_to_merge(text, result1, result2):
    pattern = re.compile("\s*(and|to|-|ー)?\s*", re.IGNORECASE)
    text_between = text[result1.index + len(result1.text) : result2.index]
    return pattern.match(text_between)