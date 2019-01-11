import unittest

import chrono

from datetime import datetime


class MiddleEndianFormatTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_middle_endian(self):

        results = chrono.parse('Test : March 24, 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'March 24, 2013')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : mar 24 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'mar 24 2013')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : March 24, test', datetime(2000, 10, 1))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'March 24')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2001)
        self.assertEqual(result.start.date(), datetime(2001, 3, 24, 12))

    def test_middle_endian_as_range(self):

        results = chrono.parse('Test : Mar 21 to 25, 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'Mar 21 to 25, 2013')
        self.assertEqual(result.start.get('day'), 21)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 21, 12))
        self.assertEqual(result.end.get('day'), 25)
        self.assertEqual(result.end.get('month'), 3)
        self.assertEqual(result.end.get('year'), 2013)
        self.assertEqual(result.end.date(), datetime(2013, 3, 25, 12))

    def test_middle_endian_with_imposible_date(self):
        results = chrono.parse("August 32")
        self.assertEquals(len(results), 0)

        results = chrono.parse("August 32, 2014")
        self.assertEquals(len(results), 0)

        results = chrono.parse("Feb 29, 2014")
        self.assertEquals(len(results), 0)
