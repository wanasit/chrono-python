import unittest


import chrono

from parsers import DateParser
from parsers import ParsingResult

from parsers import IntegratedDateParser
from parsers.en import ENDateParserISO

from datetime import datetime

class MockUpDateParser(DateParser):
    
    extract_called  = 0 
    extract_first_result = ParsingResult(start={})
    extract_second_result = ParsingResult(start={})
    
    @staticmethod
    def testing_text():
        return '01234-pattern-01234-pattern'
    
    
    def pattern(self):
        return 'pattern'
    
    
    def extract(self, index):
        
        result = None
        
        if self.extract_called == 0:
            assert index == 6
            result = self.extract_first_result
            
        elif self.extract_called == 1:
            assert index == 20
            result = self.extract_second_result
        
        self.extract_called += 1
        return result


class TestBesicOperations(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    def test_1_plain_parser(self):
        
        parser = DateParser('Hello World')
        self.assertEqual(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, False)
        
        self.assertIsNone(parser.parse())
        self.assertIsNone(parser.parse())
        self.assertGreater(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        
        parser.parse_all()
        self.assertGreater(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, True)

    def test_2_mockup_parser(self):
        
        parser = MockUpDateParser(MockUpDateParser.testing_text())
        self.assertEqual(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, False)
        
        result = parser.parse()
        self.assertEqual(result, parser.extract_first_result)
        self.assertEqual(parser.extract_called, 1)
        
        self.assertGreater(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [parser.extract_first_result])
        
        result = parser.parse()
        self.assertEqual(result, parser.extract_second_result)
        self.assertEqual(parser.extract_called, 2)
        
        self.assertGreater(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [parser.extract_first_result, parser.extract_second_result])
        
        parser.parse_all()
        self.assertGreater(parser.parsing_index, 0)
        self.assertEqual(parser.extract_called, 2)
        self.assertEqual(len(parser.parsing_results), 2)
        self.assertEqual(parser.parsing_finished, True)
    
    def test_2_integrate_parser(self):
        
        parser = IntegratedDateParser('Hello World')
        self.assertGreater(len(parser.parser_classes), 0)
        self.assertGreater(len(parser.parser_instances), 0)
        self.assertIn(ENDateParserISO, parser.parser_classes)
        
        parser.parse_all()
        self.assertEqual(parser.parsing_finished, True)
    
    
    def test_3_exmple_parser(self):
        
        parser = ENDateParserISO('Hello World')
        self.assertEqual(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, False)
        
        parser.parse_all()
        self.assertEqual(len(parser.parsing_results), 0)
        self.assertEqual(parser.parsing_finished, True)
        
        parser = ENDateParserISO('Test : 2013-2-27')
        self.assertEqual(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, False)
        
        parser.parse_all()
        self.assertGreater(len(parser.parsing_results), 0)
        self.assertEqual(parser.parsing_finished, True)
        
        result = parser.parsing_results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))
        
        parser = ENDateParserISO('Test : 2013-2-27 at 7.30.12 AM')
        self.assertEqual(parser.parsing_index, 0)
        self.assertEqual(parser.parsing_results, [])
        self.assertEqual(parser.parsing_finished, False)
        
        parser.parse_all()
        self.assertGreater(len(parser.parsing_results), 0)
        self.assertEqual(parser.parsing_finished, True)
        
        result = parser.parsing_results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27 at 7.30.12 AM')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start['hour'], 7)
        self.assertEqual(result.start['minute'], 30)
        self.assertEqual(result.start['second'], 12)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 7, 30, 12))
        
    def test_4_chorono_functions(self):
        
        results = chrono.parse('Hello World')
        self.assertEqual(len(results), 0)
        
        result = chrono.parse_date('Hello World')
        self.assertEqual(result, None)
        
        results = chrono.parse('Test : 2013-2-27')
        self.assertGreater(len(results), 0)
        
        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27')
        self.assertEqual(result.start['day'], 27)
        self.assertEqual(result.start['month'], 2)
        self.assertEqual(result.start['year'], 2013)
        self.assertEqual(result.start_date, datetime(2013, 2, 27, 12))
        
        
        pass
    
    
if __name__ == '__main__':
    unittest.main()