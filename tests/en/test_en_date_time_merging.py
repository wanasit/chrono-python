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


def test_en_merge_casual_date_time():
    from chrono_python.types import DateTimePrecision
    
    ref_date = datetime.datetime(2020, 7, 10, 12, 0)

    # today at 8pm
    results = chrono.parse("today at 8pm", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "today at 8pm"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2020
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 10
    assert result.moment.get(CivilTimeComponent.HOUR) == 20
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    # since we specify "at 8pm", the hour and meridiem are known, and minute is assigned to 0, so precision is MINUTE
    assert result.moment.precision() == DateTimePrecision.MINUTE

    # tomorrow at 10:30
    results = chrono.parse("tomorrow at 10:30", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "tomorrow at 10:30"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2020
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 11
    assert result.moment.get(CivilTimeComponent.HOUR) == 10
    assert result.moment.get(CivilTimeComponent.MINUTE) == 30
    # since we specify "at 10:30", hour and minute are known, so precision is MINUTE
    assert result.moment.precision() == DateTimePrecision.MINUTE


def test_en_merge_casual_date_and_casual_time():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # this evening
    results = chrono.parse("this evening", ref_date)
    assert len(results) == 1
    assert results[0].text == "this evening"
    assert results[0].datetime() == datetime.datetime(2016, 10, 1, 20, 0)

    # yesterday afternoon
    results = chrono.parse("yesterday afternoon", ref_date)
    assert len(results) == 1
    assert results[0].text == "yesterday afternoon"
    assert results[0].datetime() == datetime.datetime(2016, 9, 30, 15, 0)

    # tomorrow morning
    results = chrono.parse("tomorrow morning", ref_date)
    assert len(results) == 1
    assert results[0].text == "tomorrow morning"
    assert results[0].datetime() == datetime.datetime(2016, 10, 2, 6, 0)
