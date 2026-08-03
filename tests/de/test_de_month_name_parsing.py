import datetime
from chrono_python.locales import de


def test_de_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10. Januar 2012
    results = de.parse("10. Januar 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10. Januar 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 10

    # 10. Jan. 2012
    results = de.parse("10. Jan. 2012", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 10

    # 10. Jänner 2012
    results = de.parse("10. Jänner 2012", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 10

    # 10. März 2012
    results = de.parse("10. März 2012", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 3
    assert dt.day == 10


def test_de_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10. - 12. Januar 2012
    results = de.parse("10. - 12. Januar 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10. - 12. Januar 2012"
    dt1 = results[0].moment.datetime()
    assert dt1.year == 2012
    assert dt1.month == 1
    assert dt1.day == 10
    dt2 = results[0].end.datetime()
    assert dt2.year == 2012
    assert dt2.month == 1
    assert dt2.day == 12

    # 10. bis 12. Januar 2012
    results = de.parse("10. bis 12. Januar 2012", ref_date)
    assert len(results) == 1
    dt1 = results[0].moment.datetime()
    assert dt1.day == 10
    dt2 = results[0].end.datetime()
    assert dt2.day == 12
