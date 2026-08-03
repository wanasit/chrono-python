import datetime
from chrono_python.locales import sv


def test_sv_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # idag
    results = sv.parse("idag", ref_date)
    assert len(results) == 1
    assert results[0].text == "idag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # imorgon
    results = sv.parse("imorgon", ref_date)
    assert len(results) == 1
    assert results[0].text == "imorgon"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # igår
    results = sv.parse("igår", ref_date)
    assert len(results) == 1
    assert results[0].text == "igår"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # förrgår
    results = sv.parse("förrgår", ref_date)
    assert len(results) == 1
    assert results[0].text == "förrgår"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 8


def test_sv_casual_date_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # idag på morgonen
    results = sv.parse("idag på morgonen", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 6

    # idag på förmiddagen
    results = sv.parse("idag på förmiddagen", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 9

    # idag på middagen
    results = sv.parse("idag på middagen", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 12

    # idag på eftermiddagen
    results = sv.parse("idag på eftermiddagen", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15

    # idag på kvällen
    results = sv.parse("idag på kvällen", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 20

    # idag på natten
    results = sv.parse("idag på natten", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 2

    # idag vid midnatt
    results = sv.parse("idag vid midnatt", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 0
