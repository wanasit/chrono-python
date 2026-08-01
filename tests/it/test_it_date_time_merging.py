import datetime
from chrono_python.locales import it


def test_it_date_time_merging():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9)

    results = it.parse("domani alle 13:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "domani alle 13:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11
    assert dt.hour == 13
    assert dt.minute == 0

    results = it.parse("ieri alle 10:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "ieri alle 10:00"
    dt = results[0].moment.datetime()
    assert dt.day == 9
    assert dt.hour == 10

    results = it.parse("venerdì prossimo alle 18:00", datetime.datetime(2012, 8, 9))
    assert len(results) == 1
    assert results[0].text == "venerdì prossimo alle 18:00"
    dt = results[0].moment.datetime()
    assert dt.day == 17
    assert dt.hour == 18
