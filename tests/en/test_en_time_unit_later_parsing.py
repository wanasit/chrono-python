import datetime
import chrono_python as chrono
from chrono_python.types import ReferenceMoment, DateTimePrecision


def test_later_parsing():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # 5 days later
    result = chrono.en.parse('5 days later', reference=ref)
    assert len(result) == 1
    assert result[0].text == '5 days later'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 25, 12, 13)
    assert result[0].moment.precision() == DateTimePrecision.DAY

    # 2 weeks after
    result = chrono.en.parse('2 weeks after', reference=ref)
    assert len(result) == 1
    assert result[0].text == '2 weeks after'
    assert result[0].moment.datetime() == datetime.datetime(2024, 6, 3, 12, 13)

    # 3 hours from now
    result = chrono.en.parse('3 hours from now', reference=ref)
    assert len(result) == 1
    assert result[0].text == '3 hours from now'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 15, 13)

    # half an hour later
    result = chrono.en.parse('half an hour later', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'half an hour later'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 12, 43)


def test_later_abbreviations():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # Abbreviated units should match in casual
    result = chrono.en.casual.parse('2 hrs later', reference=ref)
    assert len(result) == 1
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 14, 13)

    # Abbreviated units should NOT match in strict
    result = chrono.en.strict.parse('2 hrs later', reference=ref)
    assert len(result) == 0

    # Non-abbreviated units should match in strict
    result = chrono.en.strict.parse('2 hours later', reference=ref)
    assert len(result) == 1
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 14, 13)
