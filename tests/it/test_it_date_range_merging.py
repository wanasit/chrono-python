import datetime
from chrono_python.locales import it


def test_it_date_range_merging():
    ref_date = datetime.datetime(2012, 8, 4, 12, 0)

    results = it.parse("L'evento è oggi - venerdì prossimo", ref_date)
    assert len(results) == 1
    assert results[0].index == 11
    assert results[0].text == "oggi - venerdì prossimo"
    start_dt = results[0].start.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 4

    end_dt = results[0].end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 10

    # 10 agosto - 12 settembre
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = it.parse("10 agosto - 12 settembre", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto - 12 settembre"
    assert results[0].start.datetime().day == 10
    assert results[0].end.datetime().month == 9
    assert results[0].end.datetime().day == 12

    # dal 25/12/2012 al 30/12/2012
    results = it.parse("dal 25/12/2012 al 30/12/2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "25/12/2012 al 30/12/2012"
    assert results[0].start.datetime().day == 25
    assert results[0].end.datetime().day == 30
