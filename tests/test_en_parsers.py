import unittest


import chrono

from datetime import datetime

class TestEnglishParser(unittest.TestCase):

    def setUp(self):
        pass

    def test_en_1_general_parsing(self):

        results = chrono.parse('Test : today', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'today')
        self.assertEqual(result.start['day'], 22)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2012)
        self.assertEqual(result.start_date, datetime(2012, 3, 22, 12))

        pass

    def test_en_2_slash_parsing(self):

        results = chrono.parse('Test : 2/27/2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/2013')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))

        # BC years
        results = chrono.parse('Test : 2/27/2556')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/2556')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))

        # short
        results = chrono.parse('Test : 2/27/13')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/13')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))

        # BC years short
        results = chrono.parse('Test : 2/27/56')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2/27/56')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))

        #range...
        results = chrono.parse(' 5/1/2013 - 5/10/2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 1)
        self.assertEqual(result.text, '5/1/2013 - 5/10/2013')
        self.assertEqual(result.start['day'], 1)
        self.assertEqual(result.start['month'], 5)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 5, 1, 12))

        self.assertEqual(result.end['day'], 10)
        self.assertEqual(result.end['month'], 5)
        self.assertEqual(result.end['year'], 2013)
        self.assertEqual(result.end_date, datetime(2013, 5, 10, 12))

        results = chrono.parse('Impossible 2/29/2013')
        self.assertEqual(len(results), 0)

    def test_en_3_little_endian(self):

        results = chrono.parse('Test : 24 March 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 March 2013')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : 24 Mar 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Mar 2013')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : 24 mar 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 mar 2013')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 24, 12))


        results = chrono.parse('Test : 24 Mar', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Mar')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2012)
        self.assertEqual(result.start_date, datetime(2012, 3, 24, 12))



        results = chrono.parse('Test : 24 - 25 Mar', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 - 25 Mar')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2012)
        self.assertEqual(result.start_date, datetime(2012, 3, 24, 12))
        self.assertEqual(result.end['day'], 25)
        self.assertEqual(result.end['month'], 3)
        self.assertEqual(result.end['year'], 2012)
        self.assertEqual(result.end_date, datetime(2012, 3, 25, 12))


        results = chrono.parse('Test : 24 - 25 Mar 2014', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 - 25 Mar 2014')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2014)
        self.assertEqual(result.start_date, datetime(2014, 3, 24, 12))
        self.assertEqual(result.end['day'], 25)
        self.assertEqual(result.end['month'], 3)
        self.assertEqual(result.end['year'], 2014)
        self.assertEqual(result.end_date, datetime(2014, 3, 25, 12))


        results = chrono.parse('Test : 24 Feb - 2 Mar 2014', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '24 Feb - 2 Mar 2014')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2014)
        self.assertEqual(result.start_date, datetime(2014, 2, 24, 12))
        self.assertEqual(result.end['day'], 2)
        self.assertEqual(result.end['month'], 3)
        self.assertEqual(result.end['year'], 2014)
        self.assertEqual(result.end_date, datetime(2014, 3, 2, 12))


        results = chrono.parse('Test : 2 Mar 2014 (10.00 - 12.00 AM)', datetime(2012,3,22))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2 Mar 2014 (10.00 - 12.00 AM)')
        self.assertEqual(result.start['day'], 2)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2014)
        self.assertEqual(result.start_date, datetime(2014, 3, 2, 10))
        self.assertEqual(result.end['day'], 2)
        self.assertEqual(result.end['month'], 3)
        self.assertEqual(result.end['year'], 2014)
        self.assertEqual(result.end_date, datetime(2014, 3, 2, 12))

    def test_en_4_middle_endian(self):

        results = chrono.parse('Test : March 24, 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'March 24, 2013')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 24, 12))

        results = chrono.parse('Test : mar 24 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'mar 24 2013')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 24, 12))


        results = chrono.parse('Test : March 24, test', datetime(2000,10,1))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'March 24')
        self.assertEqual(result.start['day'], 24)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2001)
        self.assertEqual(result.start_date, datetime(2001, 3, 24, 12))

        results = chrono.parse('Test : Mar 21 to 25, 2013')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, 'Mar 21 to 25, 2013')
        self.assertEqual(result.start['day'], 21)
        self.assertEqual(result.start['month'], 3)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 3, 21, 12))
        self.assertEqual(result.end['day'], 25)
        self.assertEqual(result.end['month'], 3)
        self.assertEqual(result.end['year'], 2013)
        self.assertEqual(result.end_date, datetime(2013, 3, 25, 12))

    def test_en_5_time_parsing(self):

        results = chrono.parse('Test : 2013-2-27')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertNotIn('hour', result.start)
        self.assertNotIn('minute', result.start)
        self.assertNotIn('second', result.start)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))

        results = chrono.parse('Test : 2013-2-27T21:08:12')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27T21:08:12')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 21)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start['second'], 12)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 21,8,12))


        results = chrono.parse('Test : 2013-2-27 21:08:12')
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 21:08:12')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 21)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start['second'], 12)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 21,8,12))

        results = chrono.parse('Test : 2013-2-27 at 21:08:12')
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 at 21:08:12')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 21)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start['second'], 12)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 21,8,12))

        results = chrono.parse('Test : 2013-2-27 on 9:08 PM')
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 on 9:08 PM')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 21)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 21,8))

        results = chrono.parse('Test : 2013-2-27 21:08:12 AM')
        self.assertEqual(len(results), 1)
        self.assertNotIn('hour', results[0].start)


        results = chrono.parse('Test : 2013-2-27 21:08:12 PM')
        self.assertEqual(len(results), 1)
        self.assertNotIn('hour', results[0].start)

    def test_en_6_time_period_parsing(self):

        results = chrono.parse('Test : 2013-2-27 from 9:08 - 11.05 PM')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 from 9:08 - 11.05 PM')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 21)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 21,8))

        self.assertEqual(result.end['day'], 27)
        self.assertEqual(result.end['month'], 2)
        self.assertEqual(result.end['year'], 2013)
        self.assertEqual(result.end['hour'], 23)
        self.assertEqual(result.end['minute'], 5)
        self.assertEqual(result.end_date, datetime(2013, 2, 27, 23, 5))


        results = chrono.parse('Test : 2013-2-27 at 9:08 to 11.55')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 at 9:08 to 11.55')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 9)
        self.assertEqual(result.start['minute'], 8)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 9,8))

        self.assertEqual(result.end['day'], 27)
        self.assertEqual(result.end['month'], 2)
        self.assertEqual(result.end['year'], 2013)
        self.assertEqual(result.end['hour'], 11)
        self.assertEqual(result.end['minute'], 55)
        self.assertEqual(result.end_date, datetime(2013, 2, 27, 11, 55))
