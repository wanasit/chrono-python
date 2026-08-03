import datetime
from chrono_python.locales import pt


def test_pt_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("segunda 8/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "segunda 8/2/2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    results = pt.parse("Terça-feira 9/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Terça-feira 9/2/2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 9
