import datetime
import chrono_python as chrono


def test_parse_function_no_result():
    results = chrono.parse('Hello World')
    assert len(results) == 0


def test_parse_function_success():
    results = chrono.parse('Test : 2013-2-27')
    assert len(results) == 1

    result = results[0]
    assert result.index == 7
    assert result.text == '2013-2-27'
