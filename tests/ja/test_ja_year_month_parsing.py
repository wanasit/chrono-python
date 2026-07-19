import datetime

import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent


def test_year_month_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    
    # 2026年4月
    results = chrono.ja.parse("主なイベントは2026年4月です", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2026年4月"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2026
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 1
    assert result.moment.is_certain(CivilTimeComponent.DAY) is False
    assert result.moment.precision() == DateTimePrecision.MONTH

    # 2026年4月上旬・中旬
    results = chrono.ja.parse("主なイベントは2026年4月上旬・中旬です", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2026年4月上旬・中旬"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2026
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 1
    assert result.moment.is_certain(CivilTimeComponent.DAY) is False
    assert result.moment.precision() == DateTimePrecision.MONTH
    assert result.end is not None
    assert result.end.get(CivilTimeComponent.YEAR) == 2026
    assert result.end.get(CivilTimeComponent.MONTH) == 4
    assert result.end.get(CivilTimeComponent.DAY) == 20
    assert result.end.is_certain(CivilTimeComponent.DAY) is False
    assert result.end.precision() == DateTimePrecision.MONTH

    # 2026年4月下旬
    results = chrono.ja.parse("2026年4月下旬", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2026年4月下旬"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2026
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 21
    assert result.moment.precision() == DateTimePrecision.MONTH
    assert result.end is not None
    assert result.end.get(CivilTimeComponent.YEAR) == 2026
    assert result.end.get(CivilTimeComponent.MONTH) == 4
    assert result.end.get(CivilTimeComponent.DAY) == 30  # April has 30 days
    assert result.end.precision() == DateTimePrecision.MONTH

    # 4月上旬 (No year)
    results = chrono.ja.parse("4月上旬", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "4月上旬"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 1
    assert result.moment.precision() == DateTimePrecision.MONTH
    assert result.end is not None
    assert result.end.get(CivilTimeComponent.YEAR) == 2012
    assert result.end.get(CivilTimeComponent.MONTH) == 4
    assert result.end.get(CivilTimeComponent.DAY) == 10
    assert result.end.precision() == DateTimePrecision.MONTH


def test_year_month_expression_with_no():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    
    # 2026年4月の下旬
    results = chrono.ja.parse("2026年4月の下旬", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2026年4月の下旬"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2026
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 21
    assert result.moment.precision() == DateTimePrecision.MONTH
    assert result.end is not None
    assert result.end.get(CivilTimeComponent.YEAR) == 2026
    assert result.end.get(CivilTimeComponent.MONTH) == 4
    assert result.end.get(CivilTimeComponent.DAY) == 30
    assert result.end.precision() == DateTimePrecision.MONTH

    # 4月の下旬 (No year)
    results = chrono.ja.parse("4月の下旬", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "4月の下旬"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 4
    assert result.moment.get(CivilTimeComponent.DAY) == 21
    assert result.moment.precision() == DateTimePrecision.MONTH
    assert result.end is not None
    assert result.end.get(CivilTimeComponent.YEAR) == 2012
    assert result.end.get(CivilTimeComponent.MONTH) == 4
    assert result.end.get(CivilTimeComponent.DAY) == 30
    assert result.end.precision() == DateTimePrecision.MONTH
