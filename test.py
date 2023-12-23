#!/usr/bin/python
import optparse
import unittest

USAGE = """%prog [TEST_PATH] [SDK_PATH]
Run unit tests for App Engine apps.

TEST_PATH   Path to package containing test modules
"""


def main(test_path):
    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()

    TEST_PATH = './tests'

    if len(args) >= 1:
        TEST_PATH = args[0]

    main(TEST_PATH)