import datetime
from chrono_python.locales import uk


def test_uk_this_relative_expressions():
    ref_date = datetime.datetime(2017, 11, 19, 12, 0)

    # на цьому тижні
    results = uk.parse("на цьому тижні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на цьому тижні"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 11
    assert dt.day == 19

    # цього місяця
    ref_date_nov1 = datetime.datetime(2017, 11, 1, 12, 0)
    results = uk.parse("цього місяця", ref_date_nov1)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "цього місяця"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 11
    assert dt.day == 1

    # у цьому році
    results = uk.parse("у цьому році", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "у цьому році"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 1
    assert dt.day == 1


def test_uk_past_relative_expressions():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # на минулому тижні
    results = uk.parse("на минулому тижні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на минулому тижні"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 24

    # минулого місяця
    results = uk.parse("минулого місяця", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "минулого місяця"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 1

    # у минулому році
    results = uk.parse("у минулому році", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "у минулому році"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 10
    assert dt.day == 1


def test_uk_future_relative_expressions():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    # на наступному тижні
    results = uk.parse("на наступному тижні", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "на наступному тижні"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 8

    # наступного місяця
    results = uk.parse("наступного місяця", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "наступного місяця"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1

    # в наступному кварталі
    results = uk.parse("в наступному кварталі", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в наступному кварталі"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 1
    assert dt.day == 1

    # наступного року
    results = uk.parse("наступного року", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "наступного року"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 10
    assert dt.day == 1
