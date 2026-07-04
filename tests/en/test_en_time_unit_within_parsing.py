import datetime
import chrono_python as chrono
from chrono_python.types import ReferenceMoment, DateTimePrecision


def test_within_parsing():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # in 5 minutes
    result = chrono.en.parse('in 5 minutes', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'in 5 minutes'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 12, 18)
    assert result[0].moment.precision() == DateTimePrecision.MINUTE

    # within a year
    result = chrono.en.parse('within a year', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'within a year'
    assert result[0].moment.datetime() == datetime.datetime(2025, 5, 20, 12, 13)

    # for 2 weeks
    result = chrono.en.parse('for 2 weeks', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'for 2 weeks'
    assert result[0].moment.datetime() == datetime.datetime(2024, 6, 3, 12, 13)


def test_within_exclusions():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # Exclude "for the year", "for the month"
    assert len(chrono.en.parse('for the year', reference=ref)) == 0
    assert len(chrono.en.parse('for the month', reference=ref)) == 0


def test_within_abbreviations():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # Abbreviated units should match in casual
    result = chrono.en.casual.parse('in 3 mins', reference=ref)
    assert len(result) == 1
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 12, 16)

    # Abbreviated units should NOT match in strict
    result = chrono.en.strict.parse('in 3 mins', reference=ref)
    assert len(result) == 0

    # Non-abbreviated units should match in strict
    result = chrono.en.strict.parse('in 3 minutes', reference=ref)
    assert len(result) == 1
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 12, 16)
