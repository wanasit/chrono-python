import datetime
from chrono_python.locales import ru
from chrono_python.common.types import CivilTimeComponent


def test_ru_this_expressions():
    ref_date = datetime.datetime(2017, 11, 19, 12)

    results = ru.parse("на этой неделе", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на этой неделе"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 11
    assert dt.day == 19
    assert dt.hour == 12

    results = ru.parse("в этом месяце", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в этом месяце"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 11
    assert dt.day == 1
    assert dt.hour == 12

    results = ru.parse("в этом году", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в этом году"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12


def test_ru_past_relative():
    ref_date = datetime.datetime(2016, 10, 1, 12)

    results = ru.parse("на прошлой неделе", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на прошлой неделе"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 24
    assert dt.hour == 12

    results = ru.parse("в прошлом месяце", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в прошлом месяце"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 1
    assert dt.hour == 12

    results = ru.parse("в прошлом году", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в прошлом году"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 12


def test_ru_future_relative():
    ref_date = datetime.datetime(2016, 10, 1, 12)

    results = ru.parse("на следующей неделе", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на следующей неделе"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 8
    assert dt.hour == 12

    results = ru.parse("в следующем месяце", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в следующем месяце"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1
    assert dt.hour == 12

    results = ru.parse("в следующем квартале", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в следующем квартале"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12

    results = ru.parse("в следующем году", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в следующем году"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 12
