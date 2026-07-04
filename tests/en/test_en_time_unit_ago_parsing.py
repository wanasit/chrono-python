import datetime

import chrono_python as chrono

from chrono_python.types import Moment, DateTimePrecision, DateTimeMoment, ReferenceMoment
from chrono_python.common.types import CivilTimeComponent


def test_years_ago():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    result = chrono.en.parse('10 years ago', reference=ref)
    assert isinstance(result[0].moment, ReferenceMoment)
    assert result[0].moment.datetime() == datetime.datetime(2014, 5, 20, 12, 13)
    assert result[0].moment.precision() == DateTimePrecision.YEAR



    result = chrono.en.casual.parse('10y ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2014, 5, 20, 12, 13)

    result = chrono.en.casual.parse('10yr ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2014, 5, 20, 12, 13)

    result = chrono.en.casual.parse('10yrs ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2014, 5, 20, 12, 13)


def test_months_ago_less_than_12():
    ref = datetime.datetime(2024, 5, 20, 12, 13)
    result = chrono.en.parse('11 months ago', reference=ref)

    assert len(result) == 1
    assert result[0].text == '11 months ago'
    assert result[0].moment.datetime() == datetime.datetime(2023, 6, 20, 12, 13)


def test_months_ago_more_than_12():
    ref = datetime.datetime(2024, 5, 20, 12, 13)
    result = chrono.en.parse('21 months ago', reference=ref)

    assert len(result) == 1
    assert result[0].text == '21 months ago'
    assert result[0].moment.datetime() == datetime.datetime(2022, 8, 20, 12, 13)


def test_weeks_ago():
    ref = datetime.datetime(2024, 5, 20, 12, 13)
    result = chrono.en.strict.parse('1 week ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 13, 12, 13)

    result = chrono.en.casual.parse('1w ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 13, 12, 13)


def test_days_ago():
    ref = datetime.datetime(2024, 5, 20, 12, 13)
    result = chrono.en.parse('12 days ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 8, 12, 13)

    result = chrono.en.parse('12days ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 8, 12, 13)

    result = chrono.en.parse('12d ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 8, 12, 13)


def test_hours_mins_ago():
    ref = datetime.datetime(2024, 5, 20, 12, 13)

    result = chrono.en.strict.parse('20 hours 12 minutes ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 1)

    result = chrono.en.casual.parse('20 hours 12 min ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 1)

    result = chrono.en.casual.parse('20h 12min ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 1)

    result = chrono.en.casual.parse('20h 12m ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 1)

    result = chrono.en.casual.parse('20h12m ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 1)


def test_hours_mins_sec_ago():
    ref = datetime.datetime(2024, 5, 20, 12, 13, 0)

    result = chrono.en.strict.parse('20 hours 0 minutes 3seconds ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 12, 57)

    result = chrono.en.strict.parse('20 hours 12 minutes 3seconds ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 0, 57)

    result = chrono.en.casual.parse('20h 12m 3s ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 0, 57)

    result = chrono.en.casual.parse('20h12m3s ago', reference=ref)
    assert result[0].moment.datetime() == datetime.datetime(2024, 5, 19, 16, 0, 57)

    assert len(chrono.en.strict.parse('20h 12m 3s ago', reference=ref)) == 0
