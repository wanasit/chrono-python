import datetime
from chrono_python.locales import it


def test_it_time_expr_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9)

    results = it.parse("Proviamo a incontrarci alle 6:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 23
    assert results[0].text == "alle 6:00"
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert dt.minute == 0

    results = it.parse("Proviamo a incontrarci alle 6:00 PM", ref_date)
    assert len(results) == 1
    assert results[0].text == "alle 6:00 PM"
    dt = results[0].moment.datetime()
    assert dt.hour == 18
    assert dt.minute == 0

    results = it.parse("Proviamo a incontrarci alle 6:00 AM", ref_date)
    assert len(results) == 1
    assert results[0].text == "alle 6:00 AM"
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert dt.minute == 0


def test_it_time_expr_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("8:00 - 12:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "8:00 - 12:00"
    assert results[0].start.datetime().hour == 8
    assert results[0].end.datetime().hour == 12

    results = it.parse(" dalle 6:00 alle 9:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 1
    assert results[0].text == "dalle 6:00 alle 9:00"
    assert results[0].start.datetime().hour == 6
    assert results[0].end.datetime().hour == 9
