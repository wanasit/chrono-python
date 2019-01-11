#!/usr/bin/env python
# -*- coding: utf8 -*-

#from parsers.en import ENGeneralDateParser
from .parsers.en import ENInternationalStandardParser
from .parsers.en import ENMonthNameLittleEndianParser
from .parsers.en import ENMonthNameMiddleEndianParser
from .parsers.en import ENSlashDateFormatParser
from .parsers.en import ENTimeExpressionParser

from .parsers.jp import JPStandartDateFormatParser

from .refiners.en import ENRemoveOverlapRefiner
from .refiners.en import ENMergeDateTimeRefiner
from .refiners.en import ENMergeDateRangeRefiner

class Options():

    def __init__(self):
        self.parsers = []
        self.refiners = []


def standard_options():

    options = Options()
    options.parsers.append(ENInternationalStandardParser())
    options.parsers.append(ENMonthNameLittleEndianParser())
    options.parsers.append(ENMonthNameMiddleEndianParser())
    options.parsers.append(ENSlashDateFormatParser())
    options.parsers.append(ENTimeExpressionParser())
    options.parsers.append(JPStandartDateFormatParser())

    options.refiners.append(ENRemoveOverlapRefiner())
    options.refiners.append(ENMergeDateTimeRefiner())
    options.refiners.append(ENMergeDateRangeRefiner())

    return options
