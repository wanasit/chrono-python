import datetime
from chrono_python.locales import uk


def test_uk_weekday_single():
    # Thursday, Aug 9, 2012
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # понеділок
    results = uk.casual.parse("понеділок", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "понеділок"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 6, 12, 0)

    # Дедлайн у п'ятницю...
    results = uk.casual.parse("Дедлайн у п'ятницю...", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "у п'ятницю"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)

    # Дедлайн в минулий четвер!
    results = uk.casual.parse("Дедлайн в минулий четвер!", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в минулий четвер"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 2, 12, 0)

    # Saturday, Apr 18, 2015
    ref_date_apr = datetime.datetime(2015, 4, 18, 12, 0)
    results = uk.casual.parse("Дедлайн в наступний вівторок!", ref_date_apr)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в наступний вівторок"
    assert results[0].start.datetime() == datetime.datetime(2015, 4, 21, 12, 0)


def test_uk_weekday_with_casual_time():
    ref_date = datetime.datetime(2015, 4, 18, 12, 0)

    # Подзвони в середу вранці
    results = uk.casual.parse("Подзвони в середу вранці", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "в середу вранці"
    assert results[0].start.datetime() == datetime.datetime(2015, 4, 15, 6, 0)


def test_uk_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # неділя, 7 грудня 2014
    results = uk.casual.parse("неділя, 7 грудня 2014", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "неділя, 7 грудня 2014"
    assert results[0].start.datetime() == datetime.datetime(2014, 12, 7, 12, 0)
