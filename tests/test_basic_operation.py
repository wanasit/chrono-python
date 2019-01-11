import unittest
from datetime import datetime

import chrono

from chrono import Parser
from chrono import ParsedResult
from chrono import options
from datetime import datetime


class TestBesicOperations(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_0_plain_parser(self):

        parser = Parser()
        results = parser.execute('Hello World', datetime.now(), {})
        self.assertEqual(results, [])

    def test_basic_1_exmple_parser(self):

        parser = options.ENInternationalStandardParser()
        results = parser.execute('Hello World', datetime.now(), {})
        self.assertEqual(results, [])

        results = parser.execute('Test : 2013-2-27', datetime.now(), {})
        self.assertGreater(len(results), 0)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27')

    def test_basic_2_chorono_functions(self):

        results = chrono.parse('Hello World')
        self.assertEqual(len(results), 0)

        result = chrono.parse_date('Hello World')
        self.assertEqual(result, None)

        results = chrono.parse('Test : 2013-2-27')
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.index, 7)
        self.assertEqual(result.text, '2013-2-27')


if __name__ == '__main__':
    unittest.main()
