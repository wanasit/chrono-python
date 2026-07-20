import datetime
from chrono_python.types import DateTimePrecision, Weekday
from chrono_python.common.types import CivilTimeComponent
from chrono_python.common.weekdays import (
    nth_weekday_of_month,
    last_weekday_of_month,
)

def test_nth_weekday_of_month():
    # 2nd Sunday of March 2026 is March 8, 2026.
    moment = nth_weekday_of_month(2026, 3, Weekday.SUNDAY, 2, hour=2)
    assert moment.get(CivilTimeComponent.YEAR) == 2026
    assert moment.get(CivilTimeComponent.MONTH) == 3
    assert moment.get(CivilTimeComponent.DAY) == 8
    # Assert day-level precision (since YEAR, MONTH, DAY are the only known values)
    assert moment.precision() == DateTimePrecision.DAY
    # Hour should be present in implied values
    assert moment.get(CivilTimeComponent.HOUR) == 2
    # The resolved datetime should use the correct hour
    assert moment.datetime() == datetime.datetime(2026, 3, 8, 2, 0)


def test_last_weekday_of_month():
    # Last Sunday of October 2026 is October 25, 2026.
    moment = last_weekday_of_month(2026, 10, Weekday.SUNDAY, hour=3)
    assert moment.get(CivilTimeComponent.YEAR) == 2026
    assert moment.get(CivilTimeComponent.MONTH) == 10
    assert moment.get(CivilTimeComponent.DAY) == 25
    # Assert day-level precision
    assert moment.precision() == DateTimePrecision.DAY
    # Hour should be present in implied values
    assert moment.get(CivilTimeComponent.HOUR) == 3
    # The resolved datetime should use the correct hour
    assert moment.datetime() == datetime.datetime(2026, 10, 25, 3, 0)
