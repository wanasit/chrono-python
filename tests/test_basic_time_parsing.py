import unittest


import chrono

from datetime import datetime

class TestBesicTimeParsingOperations(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_1_point_of_time_parsing(self):
        
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
        
    def test_2_time_period_parsing(self):
        
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

    
    
if __name__ == '__main__':
    unittest.main()