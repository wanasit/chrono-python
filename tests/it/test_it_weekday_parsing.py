import datetime
from chrono_python.locales import it
from chrono_python.common.types import CivilTimeComponent


def test_it_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9)  # Thursday

    results = it.parse("Lunedì", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Lunedì"
    assert results[0].start.get(CivilTimeComponent.WEEKDAY) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6

    results = it.parse("giovedì", ref_date)
    assert len(results) == 1
    assert results[0].text == "giovedì"
    assert results[0].start.get(CivilTimeComponent.WEEKDAY) == 4
    dt = results[0].moment.datetime()
    assert dt.day == 9

    results = it.parse("domenica", ref_date)
    assert len(results) == 1
    assert results[0].text == "domenica"
    assert results[0].start.get(CivilTimeComponent.WEEKDAY) == 0
    dt = results[0].moment.datetime()
    assert dt.day == 12

    results = it.parse("La scadenza è venerdì prossimo...", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "venerdì prossimo"
    dt = results[0].moment.datetime()
    assert dt.day == 17

    results = it.parse("Andrò questo venerdì", ref_date)
    assert len(results) == 1
    assert results[0].index == 6
    assert results[0].text == "questo venerdì"
    dt = results[0].moment.datetime()
    assert dt.day == 10


def test_it_weekday_with_time():
    ref_date = datetime.datetime(2012, 8, 9)

    results = it.parse("Lunedì mattina", ref_date)
    assert len(results) == 1
    assert results[0].text == "Lunedì mattina"
    dt = results[0].moment.datetime()
    assert dt.day == 6
    assert dt.hour == 6


def test_it_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9)

    results = it.parse("domenica, 7 dicembre 2014", ref_date)
    assert len(results) == 1
    assert results[0].text == "domenica, 7 dicembre 2014"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 12
    assert dt.day == 7
