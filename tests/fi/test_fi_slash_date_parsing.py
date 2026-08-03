import datetime
from chrono_python.locales import fi


def test_fi_slash_date():
    ref_date = datetime.datetime(2012, 8, 10)

    # 15/8/2012 (little endian: day/month/year)
    results = fi.parse("15/8/2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15/8/2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15
