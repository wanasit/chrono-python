import unittest

import chrono

from datetime import datetime


class RandomTest1(unittest.TestCase):
    def setUp(self):
        pass

    def test_en_random_parsing_1(self):

        results = chrono.parse(
            """A Wiki is a website which is editable over the web by it's users.
        This allows information to be more rapidly updated than traditional websites.
        Many Apache projects make active use of wikis for community support and for extra project information,
        in addition to their main project websites.
        This General Wiki is a top-level overview of other wikis at the Apache Software Foundation,
        as well as overall Foundation-level information, at the bottom of this page."""
        )

        self.assertEqual(len(results), 0)

    def test_en_random_parsing_1(self):

        results = chrono.parse(
            """An event on February 24, 2013, and another event on March 1, 2013"""
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].text, 'February 24, 2013')
        self.assertEqual(results[1].text, 'March 1, 2013')
