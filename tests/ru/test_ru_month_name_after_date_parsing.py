import datetime
from chrono_python.locales import ru


def test_ru_single_expression():
    ref_date = datetime.datetime(2012, 8, 10)

    results = ru.parse("10.08.2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10.08.2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("10 августа 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 августа 2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("третье фев 82", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "третье фев 82"
    assert results[0].moment.datetime() == datetime.datetime(1982, 2, 3, 12)

    results = ru.parse("Дедлайн 10 августа", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "10 августа"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("Дедлайн Четверг, 10 января", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "Четверг, 10 января"
    assert results[0].moment.datetime() == datetime.datetime(2013, 1, 10, 12)


def test_ru_separators():
    ref_date = datetime.datetime(2012, 8, 8)

    results = ru.parse("10-августа 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10-августа 2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("10-августа-2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10-августа-2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("10/августа 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10/августа 2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("10/августа/2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10/августа/2012"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12)


def test_ru_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = ru.parse("10 - 22 августа 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 - 22 августа 2012"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 22, 12)

    results = ru.parse("с 10 по 22 августа 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "с 10 по 22 августа 2012"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 22, 12)

    results = ru.parse("10 августа - 12 сентября", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 августа - 12 сентября"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12)
    assert results[0].end.datetime() == datetime.datetime(2012, 9, 12, 12)

    results = ru.parse("10 августа - 12 сентября 2013", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 августа - 12 сентября 2013"
    assert results[0].start.datetime() == datetime.datetime(2013, 8, 10, 12)
    assert results[0].end.datetime() == datetime.datetime(2013, 9, 12, 12)


def test_ru_combined():
    ref_date = datetime.datetime(2012, 8, 10)
    results = ru.parse("5 мая 12:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 мая 12:00"
    assert results[0].moment.datetime() == datetime.datetime(2012, 5, 5, 12, 0)


def test_ru_ordinal_words():
    ref_date = datetime.datetime(2012, 2, 10)
    results = ru.parse("двадцать пятое мая", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "двадцать пятое мая"
    assert results[0].moment.datetime() == datetime.datetime(2012, 5, 25, 12, 0)

    results = ru.parse("двадцать пятое мая 2020 года", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "двадцать пятое мая 2020 года"
    assert results[0].moment.datetime() == datetime.datetime(2020, 5, 25, 12, 0)


def test_ru_followed_by_time():
    ref_date = datetime.datetime(2017, 7, 7, 15)
    results = ru.parse("24го октября, 9:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "24го октября, 9:00"
    assert results[0].moment.datetime() == datetime.datetime(2017, 10, 24, 9)


def test_ru_year_90s():
    ref_date = datetime.datetime(2012, 8, 10)
    results = ru.parse("03 авг 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "03 авг 96"
    assert results[0].moment.datetime() == datetime.datetime(1996, 8, 3, 12)


def test_ru_strict_impossible_dates():
    ref_date = datetime.datetime(2012, 8, 10)
    assert len(ru.strict.parse("32 августа 2014", ref_date)) == 0
    assert len(ru.strict.parse("29 февраля 2014", ref_date)) == 0
    assert len(ru.strict.parse("32 августа", ref_date)) == 0
    assert len(ru.strict.parse("29 февраля", datetime.datetime(2013, 8, 10))) == 0
