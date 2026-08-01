import datetime
from chrono_python.locales import it


def test_it_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10)

    # 25/12/2012
    results = it.parse("Sarà il 25/12/2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "25/12/2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 12
    assert dt.day == 25

    # 25/12/12
    results = it.parse("Sarà il 25/12/12", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "25/12/12"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 12
    assert dt.day == 25

    # 25/12
    results = it.parse("Sarà il 25/12", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "25/12"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 12
    assert dt.day == 25


def test_it_slash_date_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("dal 25/12/2012 al 30/12/2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 4
    assert results[0].text == "25/12/2012 al 30/12/2012"
    assert results[0].start.datetime().day == 25
    assert results[0].end.datetime().day == 30
