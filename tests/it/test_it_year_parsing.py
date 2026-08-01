import datetime
from chrono_python.locales import it


def test_it_two_digit_year():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("10 agosto 12", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 12"
    assert results[0].moment.datetime().year == 2012

    results = it.parse("10 agosto 99", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 99"
    assert results[0].moment.datetime().year == 1999

    results = it.parse("10 agosto 68", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 agosto 68"
    assert results[0].moment.datetime().year == 1968
