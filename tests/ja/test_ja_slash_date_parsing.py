import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent
from chrono_python.types import DateTimePrecision

def test_ja_slash_date_format():
    ref_date = datetime.datetime(2012, 7, 10, 12, 0)

    # 2012/8/10
    results = chrono.ja.parse("2012/8/10", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2012/8/10"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 10
    assert result.moment.precision() == DateTimePrecision.DAY

    # Full-width: ２０１２／８／１０
    results = chrono.ja.parse("２０１２／８／１０", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "２０１２／８／１０"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 10
    assert result.moment.precision() == DateTimePrecision.DAY

    # 2014/12/28
    results = chrono.ja.parse("2014/12/28", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2014/12/28"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2014
    assert result.moment.get(CivilTimeComponent.MONTH) == 12
    assert result.moment.get(CivilTimeComponent.DAY) == 28
    assert result.moment.precision() == DateTimePrecision.DAY
