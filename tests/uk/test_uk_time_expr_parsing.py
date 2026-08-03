import datetime
from chrono_python.locales import uk


def test_uk_time_expression():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # 20:32:13
    results = uk.parse("20:32:13", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "20:32:13"
    dt = results[0].start.datetime()
    assert dt == datetime.datetime(2016, 10, 1, 20, 32, 13)

    # 10:00:00 - 21:45:01
    results = uk.parse("10:00:00 - 21:45:01", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10:00:00 - 21:45:01"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 10, 0, 0)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 21, 45, 1)

    # об 11 ранку
    results = uk.parse("об 11 ранку", ref_date)
    assert len(results) == 1
    assert results[0].text == "об 11 ранку"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 11, 0)

    # в 11 вечора
    results = uk.parse("в 11 вечора", ref_date)
    assert len(results) == 1
    assert results[0].text == "в 11 вечора"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 23, 0)

    # з 10 до 11 ранку
    results = uk.parse("з 10 до 11 ранку", ref_date)
    assert len(results) == 1
    assert results[0].text == "з 10 до 11 ранку"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 10, 0)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 11, 0)

    # із 10 до 11 вечора
    results = uk.parse("із 10 до 11 вечора", ref_date)
    assert len(results) == 1
    assert results[0].text == "із 10 до 11 вечора"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 22, 0)
    assert results[0].end.datetime() == datetime.datetime(2016, 10, 1, 23, 0)


def test_uk_casual_time_expression():
    results = uk.casual.parse("в 1")
    assert len(results) == 1
    assert results[0].text == "в 1"
    assert results[0].start.get("hour") == 1

    results = uk.casual.parse("о 12")
    assert len(results) == 1
    assert results[0].text == "о 12"
    assert results[0].start.get("hour") == 12

    results = uk.casual.parse("в 12.30")
    assert len(results) == 1
    assert results[0].text == "в 12.30"
    assert results[0].start.get("hour") == 12
    assert results[0].start.get("minute") == 30


def test_uk_time_expression_negative_cases():
    assert len(uk.parse("2020")) == 0
    assert len(uk.parse("2020  ")) == 0

    assert len(uk.parse("Температура 101,194 градусів!")) == 0
    assert len(uk.parse("Температура 101 градусів!")) == 0
    assert len(uk.parse("Температура 10.1")) == 0

    assert len(uk.parse("Це в 10.1 - 10.12")) == 0
    assert len(uk.parse("Це в 10 - 10.1")) == 0


def test_uk_time_expression_negative_cases_strict():
    assert len(uk.strict.parse("Це в 101,194 телефон!")) == 0
    assert len(uk.strict.parse("Це в 101 стіл!")) == 0
    assert len(uk.strict.parse("Це в 10.1")) == 0
    assert len(uk.strict.parse("Це в 10")) == 0
    assert len(uk.strict.parse("2020")) == 0

    assert len(uk.strict.parse("Це в 10.1 - 10.12")) == 0
    assert len(uk.strict.parse("Це в 10 - 10.1")) == 0
    assert len(uk.strict.parse("Це в 10 - 20")) == 0
    assert len(uk.strict.parse("7-730")) == 0
