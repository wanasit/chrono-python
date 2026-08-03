import datetime
from chrono_python.locales import nl


def test_nl_time_unit_casual_relative_positive():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    results = nl.parse("komende 2 weken", ref_date)
    assert len(results) == 1
    assert results[0].text == "komende 2 weken"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 15

    results = nl.parse("komende 2 dagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "komende 2 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 3
    assert dt.hour == 12

    results = nl.parse("komende 2 jaar", ref_date)
    assert len(results) == 1
    assert results[0].text == "komende 2 jaar"
    dt = results[0].moment.datetime()
    assert dt.year == 2018
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 12

    results = nl.parse("komende 2 weken 3 dagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "komende 2 weken 3 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 18
    assert dt.hour == 12


def test_nl_time_unit_casual_relative_negative():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    results = nl.parse("afgelopen 2 weken", ref_date)
    assert len(results) == 1
    assert results[0].text == "afgelopen 2 weken"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 17
    assert dt.hour == 12

    results = nl.parse("afgelopen twee weken", ref_date)
    assert len(results) == 1
    assert results[0].text == "afgelopen twee weken"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 17
    assert dt.hour == 12

    results = nl.parse("afgelopen 2 dagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "afgelopen 2 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 29
    assert dt.hour == 12

    results = nl.parse("+2 maanden 5 dagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "+2 maanden 5 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 12
    assert dt.day == 6
    assert dt.hour == 12


def test_nl_time_unit_casual_relative_plus():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    results = nl.parse("+15 minuten", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15 minuten"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = nl.parse("+15min", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15min"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = nl.parse("+1 dag 2 uur", ref_date)
    assert len(results) == 1
    assert results[0].text == "+1 dag 2 uur"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 14
    assert dt.minute == 14


def test_nl_time_unit_casual_relative_minus():
    ref_date = datetime.datetime(2015, 7, 10, 12, 14)

    results = nl.parse("-3jr", ref_date)
    assert len(results) == 1
    assert results[0].text == "-3jr"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 10
    assert dt.hour == 12
    assert dt.minute == 14

    ref_date = datetime.datetime(2016, 10, 1, 12, 0)
    results = nl.parse("-2u5min", ref_date)
    assert len(results) == 1
    assert results[0].text == "-2u5min"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 9
    assert dt.minute == 55
