import datetime
from chrono_python.locales import ru


def test_ru_month_year():
    results = ru.parse("Сентябрь 2012")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Сентябрь 2012"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 1, 12)

    results = ru.parse("сен 2012")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "сен 2012"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 1, 12)

    results = ru.parse("сен. 2012")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "сен. 2012"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 1, 12)

    results = ru.parse("сен-2012")
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "сен-2012"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 1, 12)


def test_ru_month_only():
    ref_date = datetime.datetime(2020, 11, 22)

    results = ru.parse("в январе", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в январе"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2021, 1, 1, 12)

    results = ru.parse("в янв", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в янв"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2021, 1, 1, 12)

    results = ru.parse("май", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "май"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2021, 5, 1, 12)


def test_ru_month_in_context():
    results = ru.parse("Это было в сентябре 2012 перед новым годом")
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "в сентябре 2012"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 1, 12)


def test_ru_year_90s():
    ref_date = datetime.datetime(2012, 8, 10)
    results = ru.parse("авг 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "авг 96"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(1996, 8, 1, 12)

    results = ru.parse("96 авг 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "авг 96"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(1996, 8, 1, 12)
