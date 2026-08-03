import datetime
from chrono_python.locales import uk


def test_uk_slash_date_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = uk.parse("10/08/2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10/08/2012"
    dt = results[0].start.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
