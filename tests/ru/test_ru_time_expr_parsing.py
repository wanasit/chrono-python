import datetime
from chrono_python.common.types import CivilTimeComponent
from chrono_python.locales import ru


def test_ru_time_expression():
    ref_date = datetime.datetime(2016, 10, 1, 8)

    results = ru.parse("20:32:13", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "20:32:13"
    dt = results[0].moment.datetime()
    assert dt.hour == 20
    assert dt.minute == 32
    assert dt.second == 13


def test_ru_time_range():
    ref_date = datetime.datetime(2016, 10, 1, 8)

    results = ru.parse("10:00:00 - 21:45:01", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10:00:00 - 21:45:01"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 10, 0, 0)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 21, 45, 1)


def test_ru_casual_time_number():
    ref_date = datetime.datetime(2016, 10, 1, 8)

    results = ru.parse("в 11 утра", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в 11 утра"
    dt = results[0].moment.datetime()
    assert dt.hour == 11

    results = ru.parse("в 11 вечера", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в 11 вечера"
    dt = results[0].moment.datetime()
    assert dt.hour == 23


def test_ru_time_range_meridiem():
    ref_date = datetime.datetime(2016, 10, 1, 8)

    results = ru.parse("с 10 до 11 утра", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "с 10 до 11 утра"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 10)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 11)

    results = ru.parse("с 10 до 11 вечера", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "с 10 до 11 вечера"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 22)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 23)


def test_ru_casual_time_positive():
    results = ru.parse("в 1")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в 1"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1

    results = ru.parse("в 12")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в 12"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 12

    results = ru.parse("в 12.30")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в 12.30"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 12
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30


def test_ru_time_negative():
    assert len(ru.parse("2020")) == 0
    assert len(ru.parse("2020  ")) == 0
    assert len(ru.parse("Температура 101,194 градусов!")) == 0
    assert len(ru.parse("Температура 101 градусов!")) == 0
    assert len(ru.parse("Температура 10.1")) == 0
    assert len(ru.parse("Это в 10.1 - 10.12")) == 0
    assert len(ru.parse("Это в 10 - 10.1")) == 0


def test_ru_time_strict_negative():
    assert len(ru.strict.parse("Это в 101,194 телефон!")) == 0
    assert len(ru.strict.parse("Это в 101 стул!")) == 0
    assert len(ru.strict.parse("Это в 10.1")) == 0
    assert len(ru.strict.parse("Это в 10")) == 0
    assert len(ru.strict.parse("2020")) == 0
    assert len(ru.strict.parse("Это в 10.1 - 10.12")) == 0
    assert len(ru.strict.parse("Это в 10 - 10.1")) == 0
    assert len(ru.strict.parse("Это в 10 - 20")) == 0
    assert len(ru.strict.parse("7-730")) == 0
