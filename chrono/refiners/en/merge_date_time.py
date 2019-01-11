#!/usr/bin/env python
# -*- coding: utf8 -*-
import re

from ..refiner import Refiner
from ..refiner import ParsedResult
from ..refiner import ParsedComponent


class ENMergeDateTimeRefiner(Refiner):
    def refine(self, results, text, options):

        if len(results) < 2: return results

        merged_results = []
        prev_result = None
        curr_result = None
        i = 1

        while i < len(results):
            prev_result = results[i - 1]
            curr_result = results[i]

            if is_able_to_merge(text, prev_result, curr_result):

                if is_time_only(curr_result) and is_date_only(prev_result):
                    prev_result = merge_result(text, prev_result, curr_result)
                    curr_result = None
                    i += 1

                elif is_time_only(prev_result) and is_date_only(curr_result):
                    prev_result = merge_result(text, curr_result, prev_result)
                    curr_result = None
                    i += 1

            merged_results.append(prev_result)
            i += 1

        if curr_result:
            merged_results.append(curr_result)

        return merged_results


def is_date_only(result):
    return not result.start.is_certain('hour')


def is_time_only(result):
    return not result.start.is_certain('day') and not result.start.is_certain(
        'day_of_week')


def is_able_to_merge(text, result1, result2):
    pattern = re.compile("\s*(T|at|on|of|,)?\s*", re.IGNORECASE)
    text_between = text[result1.index + len(result1.text):result2.index]
    return pattern.match(text_between)


def merge_result(text, date_result, time_result):
    result = ParsedResult()
    begin_index = min(date_result.index, time_result.index)
    end_index = max(date_result.index + len(date_result.text),
                    time_result.index + len(time_result.text))
    result.index = begin_index
    result.text = text[begin_index:end_index]

    result.start = date_result.start.copy()
    result.start.assign('hour', time_result.start.get('hour'))
    result.start.assign('minute', time_result.start.get('minute'))
    result.start.assign('second', time_result.start.get('second'))

    if time_result.end or date_result.end:
        time_result_end = time_result.end if time_result.end else time_result.start
        date_result_end = date_result.end if date_result.end else date_result.start

        result.end = date_result_end.copy()
        result.end.assign('hour', time_result_end.get('hour'))
        result.end.assign('minute', time_result_end.get('minute'))
        result.end.assign('second', time_result_end.get('second'))

    return result
