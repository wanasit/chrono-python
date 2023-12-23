import unittest

import chrono

from datetime import datetime


class LittleEndianFormatTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_little_endian(self):

        results = chrono.parse('Test : 24 March 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 March 2013')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : 24 Mar 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Mar 2013')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : 24 mar 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 mar 2013')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : 24 Mar', datetime(2012, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Mar')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2012)
        self.assertEqual(result.start.date(), datetime(2012, 3, 24, 12))

        results = chrono.parse('Test : 24 March, test', datetime(2000, 10, 1))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 March')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2001)
        self.assertEqual(result.start.date(), datetime(2001, 3, 24, 12))

    def test_little_endian_range(self):

        results = chrono.parse('Test : 24 - 25 Mar', datetime(2012, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 - 25 Mar')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2012)
        self.assertEqual(result.start.date(), datetime(2012, 3, 24, 12))
        self.assertEqual(result.end.get('day'), 25)
        self.assertEqual(result.end.get('month'), 3)
        self.assertEqual(result.end.get('year'), 2012)
        self.assertEqual(result.end.date(), datetime(2012, 3, 25, 12))

        results = chrono.parse('Test : 24 - 25 Mar 2014', datetime(
            2012, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 - 25 Mar 2014')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2014)
        self.assertEqual(result.start.date(), datetime(2014, 3, 24, 12))
        self.assertEqual(result.end.get('day'), 25)
        self.assertEqual(result.end.get('month'), 3)
        self.assertEqual(result.end.get('year'), 2014)
        self.assertEqual(result.end.date(), datetime(2014, 3, 25, 12))

        results = chrono.parse('Test : 24 Feb - 2 Mar 2014',
                               datetime(2012, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Feb - 2 Mar 2014')
        self.assertEqual(result.start.get('day'), 24)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2014)
        self.assertEqual(result.start.date(), datetime(2014, 2, 24, 12))
        self.assertEqual(result.end.get('day'), 2)
        self.assertEqual(result.end.get('month'), 3)
        self.assertEqual(result.end.get('year'), 2014)
        self.assertEqual(result.end.date(), datetime(2014, 3, 2, 12))

    def test_little_endian_with_time(self):
        results = chrono.parse('Test : 2 Mar 2014 (10.00 - 11.00 AM)',
                               datetime(2012, 3, 22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2 Mar 2014 (10.00 - 11.00 AM)')
        self.assertEqual(result.start.get('day'), 2)
        self.assertEqual(result.start.get('month'), 3)
        self.assertEqual(result.start.get('year'), 2014)
        self.assertEqual(result.start.date(), datetime(2014, 3, 2, 10))
        self.assertEqual(result.end.get('day'), 2)
        self.assertEqual(result.end.get('month'), 3)
        self.assertEqual(result.end.get('year'), 2014)
        self.assertEqual(result.end.date(), datetime(2014, 3, 2, 11))

    def test_little_endian_with_imposible_date(self):
        results = chrono.parse("32 August")
        self.assertEquals(len(results), 0)

        results = chrono.parse("32 August 2014")
        self.assertEquals(len(results), 0)

        results = chrono.parse("29 Feb 2014")
        self.assertEquals(len(results), 0)
