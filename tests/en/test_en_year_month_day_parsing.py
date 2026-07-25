import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

def test_slash_year_month_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 2012/8/10
    results = chrono.parse('2012/8/10', ref_date)
    assert len(results) == 1
    assert results[0].text == '2012/8/10'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10
    assert results[0].moment.is_certain(CivilTimeComponent.DAY) is True

    # 2014.12.28
    results = chrono.parse('2014.12.28', ref_date)
    assert len(results) == 1
    assert results[0].text == '2014.12.28'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2014
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 12
    assert results[0].moment.get(CivilTimeComponent.DAY) == 28

    # 2014 12 28
    results = chrono.parse('2014 12 28', ref_date)
    assert len(results) == 1
    assert results[0].text == '2014 12 28'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2014
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 12
    assert results[0].moment.get(CivilTimeComponent.DAY) == 28


def test_slash_year_month_date_with_month_name():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 2012/Aug/10
    results = chrono.parse('2012/Aug/10', ref_date)
    assert len(results) == 1
    assert results[0].text == '2012/Aug/10'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    # 2018 March 18
    results = chrono.parse('2018 March 18', ref_date)
    assert len(results) == 1
    assert results[0].text == '2018 March 18'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2018
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 3
    assert results[0].moment.get(CivilTimeComponent.DAY) == 18


def test_slash_year_month_optional_day():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 2012/08
    results = chrono.parse('2012/08', ref_date)
    assert len(results) == 1
    assert results[0].text == '2012/08'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.is_certain(CivilTimeComponent.DAY) is False


def test_slash_year_month_date_swap():
    # Casual mode should swap month and day if month is > 12
    # 2024/13/1 -> Jan 13, 2024
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = chrono.en.casual.parse('2024/13/1', ref_date)
    assert len(results) == 1
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2024
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 13

    # Strict mode should reject it
    results_strict = chrono.en.strict.parse('2024/13/1', ref_date)
    assert len(results_strict) == 0
