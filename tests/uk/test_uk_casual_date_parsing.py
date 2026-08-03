import datetime
from chrono_python.locales import uk


def test_uk_casual_date_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # сьогодні
    results = uk.parse("сьогодні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "сьогодні"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # вчора
    results = uk.parse("вчора", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "вчора"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # завтра
    results = uk.parse("завтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "завтра"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # післязавтра
    results = uk.parse("післязавтра", ref_date)
    assert len(results) == 1
    assert results[0].text == "післязавтра"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12

    # післяпіслязавтра
    results = uk.parse("післяпіслязавтра", ref_date)
    assert len(results) == 1
    assert results[0].text == "післяпіслязавтра"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13

    # позавчора
    results = uk.parse("позавчора", ref_date)
    assert len(results) == 1
    assert results[0].text == "позавчора"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 8

    # позапозавчора
    results = uk.parse("позапозавчора", ref_date)
    assert len(results) == 1
    assert results[0].text == "позапозавчора"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 7


def test_uk_casual_time_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    # зараз
    results = uk.parse("зараз", ref_date)
    assert len(results) == 1
    assert results[0].text == "зараз"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 12
    assert dt.minute == 14

    # ввечері
    ref_date_noon = datetime.datetime(2012, 8, 10, 12, 0)
    results = uk.parse("ввечері", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "ввечері"
    dt = results[0].moment.datetime()
    assert dt.hour == 20

    # вранці
    results = uk.parse("вранці", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "вранці"
    dt = results[0].moment.datetime()
    assert dt.hour == 6

    # зранку
    results = uk.parse("зранку", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "зранку"
    dt = results[0].moment.datetime()
    assert dt.hour == 6

    # опівдні
    results = uk.parse("опівдні", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "опівдні"
    dt = results[0].moment.datetime()
    assert dt.hour == 12

    # минулої ночі
    results = uk.parse("минулої ночі", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "минулої ночі"
    dt = results[0].moment.datetime()
    assert dt.day == 9
    assert dt.hour == 0

    # минулого вечора
    results = uk.parse("минулого вечора", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "минулого вечора"
    dt = results[0].moment.datetime()
    assert dt.day == 9
    assert dt.hour == 20

    # наступної ночі
    results = uk.parse("наступної ночі", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "наступної ночі"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 1

    # цієї ночі
    results = uk.parse("цієї ночі", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "цієї ночі"
    dt = results[0].moment.datetime()
    assert dt.hour == 0

    # опівночі
    results = uk.parse("опівночі", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "опівночі"
    dt = results[0].moment.datetime()
    assert dt.hour == 0

    # вночі
    results = uk.parse("вночі", ref_date_noon)
    assert len(results) == 1
    assert results[0].text == "вночі"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
