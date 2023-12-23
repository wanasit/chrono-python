import unittest

import chrono

from datetime import datetime


class ISOFormatTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_iso_format(self):

        results = chrono.parse('Test : 2013-3-22', datetime(2013, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-3-22')
        self.assertEqual(result.start.get('day'), 22)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 22, 12))

    def test_iso_format_with_imposible_date(self):

        results = chrono.parse("2013-8-32")
        self.assertEquals(len(results), 0)

        results = chrono.parse("2014-8-32")
        self.assertEquals(len(results), 0)

        results = chrono.parse("2014-2-29")
        self.assertEquals(len(results), 0)
