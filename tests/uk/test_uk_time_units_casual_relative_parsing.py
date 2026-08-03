import datetime
from chrono_python.locales import uk


def test_uk_time_units_casual_relative():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # через декілька хвилин
    results = uk.parse("через декілька хвилин", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через декілька хвилин"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 12, 2)

    # через півгодини
    results = uk.parse("через півгодини", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через півгодини"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 12, 30)

    # через 2 години
    results = uk.parse("через 2 години", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через 2 години"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 1, 14, 0)

    # через три місяці
    results = uk.parse("через три місяці", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через три місяці"
    assert results[0].start.datetime() == datetime.datetime(2017, 1, 1, 12, 0)

    # через тиждень
    results = uk.parse("через тиждень", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через тиждень"
    assert results[0].start.datetime() == datetime.datetime(2016, 10, 8, 12, 0)

    # через місяць
    results = uk.parse("через місяць", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через місяць"
    assert results[0].start.datetime() == datetime.datetime(2016, 11, 1, 12, 0)

    # через рік
    ref_date_sec = datetime.datetime(2020, 11, 22, 12, 11, 32)
    results = uk.parse("через рік", ref_date_sec)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "через рік"
    assert results[0].start.datetime() == datetime.datetime(2021, 11, 22, 12, 11, 32)


def test_uk_negative_time_units():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # минулі 2 тижні
    results = uk.parse("минулі 2 тижні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "минулі 2 тижні"
    assert results[0].start.datetime() == datetime.datetime(2016, 9, 17, 12, 0)

    # минулі два дні
    results = uk.parse("минулі два дні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "минулі два дні"
    assert results[0].start.datetime() == datetime.datetime(2016, 9, 29, 12, 0)


def test_uk_plus_sign():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    # +15 хвилин
    results = uk.casual.parse("+15 хвилин", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+15 хвилин"
    assert results[0].start.datetime() == datetime.datetime(2012, 7, 10, 12, 29)

    # +15хв
    results = uk.casual.parse("+15хв", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+15хв"
    assert results[0].start.datetime() == datetime.datetime(2012, 7, 10, 12, 29)

    # +1 день 2 години
    results = uk.casual.parse("+1 день 2 години", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "+1 день 2 години"
    assert results[0].start.datetime() == datetime.datetime(2012, 7, 11, 14, 14)


def test_uk_minus_sign():
    ref_date = datetime.datetime(2015, 7, 10, 12, 14)

    # -3 роки
    results = uk.casual.parse("-3 роки", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "-3 роки"
    assert results[0].start.datetime() == datetime.datetime(2012, 7, 10, 12, 14)
