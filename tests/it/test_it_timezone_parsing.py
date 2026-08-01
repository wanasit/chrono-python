import datetime
from chrono_python.locales import it
from chrono_python.common.types import CivilTimeComponent


def test_it_timezone_abbreviation():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("10 agosto 2012 10:00 CET", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 2012 10:00 CET"
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 120

    results = it.parse("10 agosto 2012 10:00 CEST", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 2012 10:00 CEST"
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 120


def test_it_timezone_offset():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("10 agosto 2012 10:00 +0100", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 2012 10:00 +0100"
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 60

    results = it.parse("10 agosto 2012 10:00 +02:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 2012 10:00 +02:00"
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 120
