import unittest


import chrono

from datetime import datetime

class TestEnglishParser(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_1_general_parsing(self):
        
        pass
    
    
    def test_2_slash_parsing(self):
        
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
    
    
        
    
    