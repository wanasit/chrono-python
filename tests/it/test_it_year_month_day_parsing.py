import datetime
from chrono_python.locales import it


def test_it_year_month_day_single():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("2012-8-10", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "2012-8-10"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = it.parse("2012/8/10", ref_date)
    assert len(results) == 1
    assert results[0].text == "2012/8/10"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = it.parse("Il 2012/8/10", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "2012/8/10"


def test_it_year_month_day_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("2012/8/10 - 2012/8/15", ref_date)
    assert len(results) == 1
    assert results[0].text == "2012/8/10 - 2012/8/15"
    assert results[0].start.datetime().day == 10
    assert results[0].end.datetime().day == 15
