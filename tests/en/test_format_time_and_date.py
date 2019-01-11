import unittest

import chrono

from datetime import datetime


class DateTimeParsingTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_date_time_as_point(self):

        results = chrono.parse('Test : 2013-2-27T21:08:12')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27T21:08:12')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 21)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.get('second'), 12)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 21, 8, 12))

        results = chrono.parse('Test : 21:08:12 on 2013-2-27')

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '21:08:12 on 2013-2-27')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 21)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.get('second'), 12)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 21, 8, 12))

        results = chrono.parse('Test : 2013-2-27 at 21:08:12')
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 at 21:08:12')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 21)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.get('second'), 12)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 21, 8, 12))

        results = chrono.parse('Test : 2013-2-27 on 9:08 PM')
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 on 9:08 PM')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 21)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 21, 8))

    def test_date_time_as_range(self):

        results = chrono.parse('Test : 2013-2-27 from 9:08 - 11.05 PM')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 from 9:08 - 11.05 PM')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 21)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 21, 8))

        self.assertEqual(result.end.get('day'), 27)
        self.assertEqual(result.end.get('month'), 2)
        self.assertEqual(result.end.get('year'), 2013)
        self.assertEqual(result.end.get('hour'), 23)
        self.assertEqual(result.end.get('minute'), 5)
        self.assertEqual(result.end.date(), datetime(2013, 2, 27, 23, 5))

        results = chrono.parse('Test : 2013-2-27 at 9:08 to 11.55')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 at 9:08 to 11.55')
        self.assertEqual(result.start.get('day'), 27)
        self.assertEqual(result.start.get('month'), 2)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.get('hour'), 9)
        self.assertEqual(result.start.get('minute'), 8)
        self.assertEqual(result.start.date(), datetime(2013, 2, 27, 9, 8))

        self.assertEqual(result.end.get('day'), 27)
        self.assertEqual(result.end.get('month'), 2)
        self.assertEqual(result.end.get('year'), 2013)
        self.assertEqual(result.end.get('hour'), 11)
        self.assertEqual(result.end.get('minute'), 55)
        self.assertEqual(result.end.date(), datetime(2013, 2, 27, 11, 55))
