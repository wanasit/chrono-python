import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

def test_relative_merging_follow_by_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0) # Friday

    # "2 weeks before 2020-02-13" -> 2020-01-30
    results = chrono.parse('2 weeks before 2020-02-13', ref_date)
    assert len(results) == 1
    assert results[0].text == '2 weeks before 2020-02-13'
    assert results[0].moment.datetime().date() == datetime.date(2020, 1, 30)

    # "2 days after next Friday" -> next Friday is Aug 17, +2 days is Aug 19
    results = chrono.parse('2 days after next Friday', ref_date)
    assert len(results) == 1
    assert results[0].text == '2 days after next Friday'
    assert results[0].moment.datetime().date() == datetime.date(2012, 8, 19)


def test_relative_merging_after_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0) # Friday

    # "2020-02-13 +2 weeks" -> 2020-02-27
    results = chrono.parse('2020-02-13 +2 weeks', ref_date)
    assert len(results) == 1
    assert results[0].text == '2020-02-13 +2 weeks'
    assert results[0].moment.datetime().date() == datetime.date(2020, 2, 27)

    # "2020-02-13 -2 days" -> 2020-02-11
    results = chrono.parse('2020-02-13 -2 days', ref_date)
    assert len(results) == 1
    assert results[0].text == '2020-02-13 -2 days'
    assert results[0].moment.datetime().date() == datetime.date(2020, 2, 11)

    # "yesterday +2 weeks" -> yesterday is Aug 9, +2 weeks is Aug 23
    results = chrono.parse('yesterday +2 weeks', ref_date)
    assert len(results) == 1
    assert results[0].text == 'yesterday +2 weeks'
    assert results[0].moment.datetime().date() == datetime.date(2012, 8, 23)
