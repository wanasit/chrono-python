import datetime
from chrono_python.locales import ru


def test_ru_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9)

    results = ru.parse("понедельник", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "понедельник"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 6, 12)

    results = ru.parse("Дедлайн в пятницу...", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в пятницу"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("Дедлайн в прошлый четверг!", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в прошлый четверг"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 2, 12)

    ref_date = datetime.datetime(2015, 4, 18)
    results = ru.parse("Дедлайн в следующий вторник", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в следующий вторник"
    assert results[0].moment.datetime() == datetime.datetime(2015, 4, 21, 12)


def test_ru_weekday_casual_time():
    ref_date = datetime.datetime(2015, 4, 18)
    results = ru.parse("Позвони в среду утром", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в среду утром"
    assert results[0].moment.datetime() == datetime.datetime(2015, 4, 15, 6)


def test_ru_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9)
    results = ru.parse("воскресенье, 7 декабря 2014", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "воскресенье, 7 декабря 2014"
    assert results[0].moment.datetime() == datetime.datetime(2014, 12, 7, 12)
