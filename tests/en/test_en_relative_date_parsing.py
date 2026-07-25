import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

def test_relative_week():
    # Sunday is 0, Monday is 1, ... Saturday is 6.
    # Reference date: Friday, Aug 10, 2012
    ref_date = datetime.datetime(2012, 8, 10, 12, 0) # Friday

    # "this week" -> Aug 5, 2012 (Sunday)
    results = chrono.parse('this week', ref_date)
    assert len(results) == 1
    assert results[0].text == 'this week'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 5

    # "next week" -> Aug 17, 2012 (+7 days from ref_date)
    results = chrono.parse('next week', ref_date)
    assert len(results) == 1
    assert results[0].text == 'next week'
    # ReferenceMoment(ref_date, {Timeunit.WEEK: 1})
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 17, 12, 0)

    # "last week" -> Aug 3, 2012 (-7 days from ref_date)
    results = chrono.parse('last week', ref_date)
    assert len(results) == 1
    assert results[0].text == 'last week'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 3, 12, 0)


def test_relative_month():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # "this month" -> Aug 1, 2012
    results = chrono.parse('this month', ref_date)
    assert len(results) == 1
    assert results[0].text == 'this month'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1

    # "next month" -> Sept 10, 2012 (+1 month)
    results = chrono.parse('next month', ref_date)
    assert len(results) == 1
    assert results[0].text == 'next month'
    assert results[0].moment.datetime() == datetime.datetime(2012, 9, 10, 12, 0)

    # "last month" -> July 10, 2012 (-1 month)
    results = chrono.parse('last month', ref_date)
    assert len(results) == 1
    assert results[0].text == 'last month'
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 10, 12, 0)


def test_relative_year():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # "this year" -> Jan 1, 2012
    results = chrono.parse('this year', ref_date)
    assert len(results) == 1
    assert results[0].text == 'this year'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1

    # "next year" -> Aug 10, 2013 (+1 year)
    results = chrono.parse('next year', ref_date)
    assert len(results) == 1
    assert results[0].text == 'next year'
    assert results[0].moment.datetime() == datetime.datetime(2013, 8, 10, 12, 0)

    # "last year" -> Aug 10, 2011 (-1 year)
    results = chrono.parse('last year', ref_date)
    assert len(results) == 1
    assert results[0].text == 'last year'
    assert results[0].moment.datetime() == datetime.datetime(2011, 8, 10, 12, 0)
