import datetime
import chrono_python as chrono
from chrono_python.types import ReferenceMoment, DateTimePrecision


def test_casual_reference_parsing():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # Past 2 days
    result = chrono.en.parse('past 2 days', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'past 2 days'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 18, 12, 13)
    assert result[0].moment.precision() == DateTimePrecision.DAY

    # Next 3 months
    result = chrono.en.parse('next 3 months', reference=ref)
    assert len(result) == 1
    assert result[0].text == 'next 3 months'
    assert result[0].moment.datetime() == datetime.datetime(2024, 8, 20, 12, 13)
    assert result[0].moment.precision() == DateTimePrecision.MONTH

    # Plus offset
    result = chrono.en.parse('+5 days', reference=ref)
    assert len(result) == 1
    assert result[0].text == '+5 days'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 25, 12, 13)

    # Minus offset
    result = chrono.en.parse('-2 hours', reference=ref)
    assert len(result) == 1
    assert result[0].text == '-2 hours'
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 20, 10, 13)


def test_casual_reference_abbreviations():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    # With abbreviations in casual configuration
    result = chrono.en.casual.parse('next 2 wks', reference=ref)
    assert len(result) == 1
    assert result[0].moment.datetime() == datetime.datetime(2024, 6, 3, 12, 13)

    # Abbreviations not present in strict configuration
    # (Since ENTimeUnitCasualReferenceParser is ONLY registered in casual configuration,
    # strict should not find anything)
    result = chrono.en.strict.parse('next 2 wks', reference=ref)
    assert len(result) == 0
