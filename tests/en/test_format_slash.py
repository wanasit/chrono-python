import unittest

import chrono

from datetime import datetime


class SlashFormatTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_slash_format(self):

        results = chrono.parse('Test : 2/27/2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/2013')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 12))

        # short
        results = chrono.parse('Test : 2/27/13')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/13')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 12))

    def test_slash_format_bc(self):

        # BC years
        results = chrono.parse('Test : 2/27/2556')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/2556')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 12))

        # BC years short
        results = chrono.parse('Test : 2/27/56')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/56')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 12))

    def test_slash_format_range(self):
        results = chrono.parse(' 5/1/2013 - 5/10/2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 1)
        self.assertEqual(result.text, '5/1/2013 - 5/10/2013')
        self.assertEqual(result.start.get('day'), 1)
        self.assertEqual(result.start.get('month'), 5)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 5, 1, 12))

        self.assertEqual(result.end.get('day'), 10)
        self.assertEqual(result.end.get('month'), 5)
        self.assertEqual(result.end.get('year'), 2013)
        self.assertEqual(result.end.date(), datetime(2013, 5, 10, 12))

    def test_slash_format_impossible(self):

        results = chrono.parse('Impossible 2/29/2013')
        self.assertEqual(len(results), 0)
