import datetime
from chrono_python.locales import uk


def test_uk_month_name_after_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10.08.2012
    results = uk.parse("10.08.2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10.08.2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # 10 серпня 2012
    results = uk.parse("10 серпня 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 серпня 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # 3 лют 82
    results = uk.parse("3 лют 82", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "3 лют 82"
    dt = results[0].moment.datetime()
    assert dt.year == 1982
    assert dt.month == 2
    assert dt.day == 3

    # Дедлайн 10 серпня
    results = uk.parse("Дедлайн 10 серпня", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "10 серпня"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # Дедлайн Четвер, 10 січня
    results = uk.parse("Дедлайн Четвер, 10 січня", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "Четвер, 10 січня"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 1
    assert dt.day == 10


def test_uk_month_name_after_date_separators():
    ref_date = datetime.datetime(2012, 8, 8, 12, 0)

    for text in ["10-серпня 2012", "10-серпня-2012", "10/серпня 2012", "10/серпня/2012"]:
        results = uk.parse(text, ref_date)
        assert len(results) == 1
        assert results[0].text == text
        dt = results[0].moment.datetime()
        assert dt.year == 2012
        assert dt.month == 8
        assert dt.day == 10


def test_uk_month_name_after_date_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10 - 22 серпня 2012
    results = uk.parse("10 - 22 серпня 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 - 22 серпня 2012"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 22, 12, 0)

    # із 10 по 22 серпня 2012
    results = uk.parse("із 10 по 22 серпня 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "із 10 по 22 серпня 2012"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 22, 12, 0)

    # 10 серпня - 12 вересня
    results = uk.parse("10 серпня - 12 вересня", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 серпня - 12 вересня"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2012, 9, 12, 12, 0)

    # 10 серпня - 12 вересня 2013
    results = uk.parse("10 серпня - 12 вересня 2013", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 серпня - 12 вересня 2013"
    assert results[0].start.datetime() == datetime.datetime(2013, 8, 10, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2013, 9, 12, 12, 0)


def test_uk_month_name_after_date_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 5 травня 12:00
    results = uk.parse("5 травня 12:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 травня 12:00"
    assert results[0].start.datetime() == datetime.datetime(2012, 5, 5, 12, 0)


def test_uk_month_name_after_date_ordinals():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # п'яте травня
    results = uk.parse("п'яте травня", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "п'яте травня"
    assert results[0].start.datetime() == datetime.datetime(2012, 5, 5, 12, 0)

    # двадцять п'яте травня
    ref_date_feb = datetime.datetime(2012, 2, 10, 12, 0)
    results = uk.parse("двадцять п'яте травня", ref_date_feb)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "двадцять п'яте травня"
    assert results[0].start.datetime() == datetime.datetime(2012, 5, 25, 12, 0)


def test_uk_month_name_after_date_followed_by_time():
    ref_date = datetime.datetime(2017, 7, 7, 15, 0)

    # 24го жовтня, 9:00
    results = uk.parse("24го жовтня, 9:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "24го жовтня, 9:00"
    assert results[0].start.datetime() == datetime.datetime(2017, 10, 24, 9, 0)


def test_uk_month_name_after_date_year_90s():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 03 сер 96
    results = uk.parse("03 сер 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "03 сер 96"
    assert results[0].start.datetime() == datetime.datetime(1996, 8, 3, 12, 0)


def test_uk_month_name_after_date_impossible_dates():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = uk.strict.parse("32 серпня 2014", ref_date)
    assert len(results) == 0

    results = uk.strict.parse("29 лютого 2014", ref_date)
    assert len(results) == 0

    results = uk.strict.parse("32 серпня", ref_date)
    assert len(results) == 0

    ref_date_2013 = datetime.datetime(2013, 8, 10, 12, 0)
    results = uk.strict.parse("29 лютого", ref_date_2013)
    assert len(results) == 0
