# -*- coding: utf8 -*-
import unittest
import chrono

from datetime import datetime


class StandardDateFormatTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_standard_parsing(self):

        results = chrono.parse("初めて動画が投稿されたのは 4月23日である", datetime(2012, 8, 10))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, len('初めて動画が投稿されたのは '))
        self.assertEqual(result.text, '4月23日')
        self.assertEqual(result.start.get('day'), 23)
        self.assertEqual(result.start.get('month'), 4)
        self.assertEqual(result.start.get('year'), 2012)
        self.assertEqual(result.start.date(), datetime(2012, 4, 23, 12))

        results = chrono.parse("主な株主（2012年９月3日現在）", datetime(2012, 8, 10))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, len('主な株主（'))
        self.assertEqual(result.text, '2012年９月3日')
        self.assertEqual(result.start.get('day'), 3)
        self.assertEqual(result.start.get('month'), 9)
        self.assertEqual(result.start.get('year'), 2012)
        self.assertEqual(result.start.date(), datetime(2012, 9, 3, 12))

        results = chrono.parse("主な株主（２０１３年９月１３日現在）", datetime(2012, 8, 10))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, len('主な株主（'))
        self.assertEqual(result.text, '２０１３年９月１３日')
        self.assertEqual(result.start.get('day'), 13)
        self.assertEqual(result.start.get('month'), 9)
        self.assertEqual(result.start.get('year'), 2013)
        self.assertEqual(result.start.date(), datetime(2013, 9, 13, 12))
