import datetime
from chrono_python.locales import de


def test_de_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 8/2/2016 (little-endian: 8 Feb 2016)
    results = de.parse("8/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8/2/2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    # am 8/2/2016
    results = de.parse("am 8/2/2016", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    # 8/2 (in 2012)
    results = de.parse("8/2", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 2
    assert dt.day == 8
