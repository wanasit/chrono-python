import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_en_merge_date_time():
    # Set ref_date to July 10, 2020 so July 4th is closest to 2020
    ref_date = datetime.datetime(2020, 7, 10, 12, 0)

    # July 4th at 8pm
    results = chrono.parse("July 4th at 8pm", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "July 4th at 8pm"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2020
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 4
    assert result.moment.get(CivilTimeComponent.HOUR) == 20
    assert result.moment.get(CivilTimeComponent.MINUTE) == 0
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 2020-02-13 at 6pm
    results = chrono.parse("2020-02-13 at 6pm", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2020-02-13 at 6pm"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2020
    assert result.moment.get(CivilTimeComponent.MONTH) == 2
    assert result.moment.get(CivilTimeComponent.DAY) == 13
    assert result.moment.get(CivilTimeComponent.HOUR) == 18
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM


def test_en_merge_date_time_range_increment():
    # 2020-02-13 9pm - 1am (imply ending day increment)
    ref_date = datetime.datetime(2020, 2, 1, 12, 0)
    results = chrono.parse("2020-02-13 9pm - 1am", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2020-02-13 9pm - 1am"
    assert result.start.get(CivilTimeComponent.DAY) == 13
    assert result.start.get(CivilTimeComponent.HOUR) == 21
    assert result.end.get(CivilTimeComponent.YEAR) == 2020
    assert result.end.get(CivilTimeComponent.MONTH) == 2
    assert result.end.get(CivilTimeComponent.DAY) == 14  # next day
    assert result.end.get(CivilTimeComponent.HOUR) == 1
