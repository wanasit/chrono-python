import datetime
from chrono_python.locales import sv


def test_sv_time_unit_relative():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # nästa 2 dagar
    results = sv.parse("nästa 2 dagar", ref_date)
    assert len(results) == 1
    assert results[0].text == "nästa 2 dagar"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 3
    assert dt.hour == 12

    # nästa två år
    results = sv.parse("nästa två år", ref_date)
    assert len(results) == 1
    assert results[0].text == "nästa två år"
    dt = results[0].moment.datetime()
    assert dt.year == 2018
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 12

    # nästa 2 veckor 3 dagar
    results = sv.parse("nästa 2 veckor 3 dagar", ref_date)
    assert len(results) == 1
    assert results[0].text == "nästa 2 veckor 3 dagar"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 18
    assert dt.hour == 12

    # efter ett år
    results = sv.parse("efter ett år", ref_date)
    assert len(results) == 1
    assert results[0].text == "efter ett år"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 12

    # efter en timme
    ref_date_15 = datetime.datetime(2016, 10, 1, 15, 0)
    results = sv.parse("efter en timme", ref_date_15)
    assert len(results) == 1
    assert results[0].text == "efter en timme"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 16


def test_sv_time_unit_negative():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # förra 2 veckor
    results = sv.parse("förra 2 veckor", ref_date)
    assert len(results) == 1
    assert results[0].text == "förra 2 veckor"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 17
    assert dt.hour == 12

    # förra två veckor
    results = sv.parse("förra två veckor", ref_date)
    assert len(results) == 1
    assert results[0].text == "förra två veckor"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 17
    assert dt.hour == 12

    # passerade 2 dagar
    results = sv.parse("passerade 2 dagar", ref_date)
    assert len(results) == 1
    assert results[0].text == "passerade 2 dagar"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 29
    assert dt.hour == 12

    # +2 månader, 5 dagar
    results = sv.parse("+2 månader, 5 dagar", ref_date)
    assert len(results) == 1
    assert results[0].text == "+2 månader, 5 dagar"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 12
    assert dt.day == 6
    assert dt.hour == 12


def test_sv_time_unit_plus():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    # +15 minuter
    results = sv.parse("+15 minuter", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15 minuter"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    # +15min
    results = sv.parse("+15min", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15min"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    # +1 dag 2 timmar
    results = sv.parse("+1 dag 2 timmar", ref_date)
    assert len(results) == 1
    assert results[0].text == "+1 dag 2 timmar"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 14
    assert dt.minute == 14

    # +1min
    results = sv.parse("+1min", ref_date)
    assert len(results) == 1
    assert results[0].text == "+1min"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 15


def test_sv_time_unit_minus():
    ref_date = datetime.datetime(2015, 7, 10, 12, 14)

    # -3år
    results = sv.parse("-3år", ref_date)
    assert len(results) == 1
    assert results[0].text == "-3år"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 10
    assert dt.hour == 12
    assert dt.minute == 14

    # -2tim5min
    ref_date_oct = datetime.datetime(2016, 10, 1, 12, 0)
    results = sv.parse("-2tim5min", ref_date_oct)
    assert len(results) == 1
    assert results[0].text == "-2tim5min"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 9
    assert dt.minute == 55
