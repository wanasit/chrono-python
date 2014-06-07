#!/usr/bin/env python
# -*- coding: utf8 -*-

#from parsers.en import ENGeneralDateParser
from parsers.en import ENInternationalStandardParser


class Options():

    def __init__(self):
        self.parser_classes = []
        self.refiner_classes = []


def standard_options():

    options = Options()
    options.parser_classes.append(ENInternationalStandardParser)

    return options
