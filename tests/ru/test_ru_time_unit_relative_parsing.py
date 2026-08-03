import datetime
from chrono_python.locales import ru


def test_ru_positive_time_units():
    ref_date = datetime.datetime(2016, 10, 1, 12)

    results = ru.parse("следующие 2 недели", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "следующие 2 недели"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 15, 12)

    results = ru.parse("следующие 2 дня", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "следующие 2 дня"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 3, 12)

    results = ru.parse("следующие два года", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "следующие два года"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2018, 10, 1, 12)

    results = ru.parse("следующие 2 недели 3 дня", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "следующие 2 недели 3 дня"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 18, 12)

    results = ru.parse("через пару минут", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через пару минут"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 1, 12, 2)

    results = ru.parse("через полчаса", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через полчаса"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 1, 12, 30)

    results = ru.parse("через 2 часа", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через 2 часа"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 1, 14)

    results = ru.parse("спустя 2 часа", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "спустя 2 часа"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 1, 14)

    results = ru.parse("через три месяца", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через три месяца"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2017, 1, 1, 12)

    results = ru.parse("через неделю", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через неделю"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 10, 8, 12)

    results = ru.parse("через месяц", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через месяц"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 11, 1, 12)

    results = ru.parse("через год", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через год"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2017, 10, 1, 12)


def test_ru_negative_time_units():
    ref_date = datetime.datetime(2016, 10, 1, 12)

    results = ru.parse("прошлые 2 недели", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "прошлые 2 недели"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 9, 17, 12)

    results = ru.parse("прошлые два дня", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "прошлые два дня"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2016, 9, 29, 12)


def test_ru_plus_sign():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    results = ru.parse("+15 минут", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+15 минут"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 7, 10, 12, 29)

    results = ru.parse("+15мин", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+15мин"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 7, 10, 12, 29)

    results = ru.parse("+1 день 2 часа", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+1 день 2 часа"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 7, 11, 14, 14)


def test_ru_minus_sign():
    ref_date = datetime.datetime(2015, 7, 10, 12, 14)

    results = ru.parse("-3 года", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "-3 года"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 7, 10, 12, 14)
