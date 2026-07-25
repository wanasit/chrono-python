import datetime
import chrono_python as chrono

def test_invalid_date_filtering():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 2014-02-30 (invalid day)
    results = chrono.parse('2014-02-30', ref_date)
    assert len(results) == 0

    # 2014-08-32 (invalid day)
    results = chrono.parse('2014-08-32', ref_date)
    assert len(results) == 0

    # 2014-02-28 (valid)
    results = chrono.parse('2014-02-28', ref_date)
    assert len(results) == 1
    assert results[0].text == '2014-02-28'

    # 2014-02-29 (not a leap year -> invalid)
    results = chrono.parse('2014-02-29', ref_date)
    assert len(results) == 0

    # 2016-02-29 (leap year -> valid)
    results = chrono.parse('2016-02-29', ref_date)
    assert len(results) == 1
    assert results[0].text == '2016-02-29'
