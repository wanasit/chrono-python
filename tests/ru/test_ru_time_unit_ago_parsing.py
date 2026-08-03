import datetime
from chrono_python.locales import ru


def test_ru_single_time_ago():
    ref_date = datetime.datetime(2012, 7, 10)

    results = ru.parse("5 дней назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 дней назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 5)

    results = ru.parse("5 минут назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 минут назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 9, 23, 55)

    results = ru.parse("полчаса назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "полчаса назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 9, 23, 30)


def test_ru_nested_time_ago():
    ref_date = datetime.datetime(2012, 7, 10)

    results = ru.parse("5 дней 2 часа назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 дней 2 часа назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 4, 22)

    results = ru.parse("5 минут 20 секунд назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 минут 20 секунд назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 9, 23, 54, 40)

    results = ru.parse("2 часа 5 минут назад что-то было", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "2 часа 5 минут назад"
    assert results[0].moment.datetime() == datetime.datetime(2012, 7, 9, 21, 55)


def test_ru_time_ago_negative():
    assert len(ru.parse("15 часов 29 мин")) == 0
    assert len(ru.parse("несколько часов")) == 0
    assert len(ru.parse("5 дней")) == 0
