import datetime
from chrono_python.locales import fi
from chrono_python.common.types import CivilTimeComponent


def test_fi_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9)  # Thursday, Aug 9, 2012

    results = fi.parse("maanantai", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "maanantai"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    results = fi.parse("maanantaina", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "maanantaina"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1


def test_fi_weekday_next_last():
    ref_date = datetime.datetime(2012, 8, 9)

    results = fi.parse("ensi maanantai", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "ensi maanantai"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    results = fi.parse("viime maanantai", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "viime maanantai"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1


def test_fi_weekday_variations():
    ref_date = datetime.datetime(2012, 8, 9)

    results = fi.parse("sunnuntai", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0

    results = fi.parse("tiistai", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2

    results = fi.parse("keskiviikko", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 3

    results = fi.parse("torstai", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 4

    results = fi.parse("perjantai", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    results = fi.parse("lauantai", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 6


def test_fi_weekday_abbreviations():
    ref_date = datetime.datetime(2012, 8, 9)

    results = fi.parse("ma", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    results = fi.parse("pe", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    results = fi.parse("su", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0
