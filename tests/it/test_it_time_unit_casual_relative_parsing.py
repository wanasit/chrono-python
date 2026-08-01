import datetime
from chrono_python.locales import it


def test_it_time_unit_casual_relative():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    results = it.parse("il mese prossimo", ref_date)
    assert len(results) == 1
    assert results[0].text == "il mese prossimo"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1

    results = it.parse("il mese scorso", ref_date)
    assert len(results) == 1
    assert results[0].text == "il mese scorso"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 1
