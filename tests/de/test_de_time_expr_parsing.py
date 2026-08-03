import datetime
from chrono_python.locales import de


def test_de_time_expr_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 15:00
    results = de.parse("15:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "15:00"
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 0

    # 15 Uhr
    results = de.parse("15 Uhr", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 Uhr"
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 0

    # 15 Uhr 30
    results = de.parse("15 Uhr 30", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 30

    # 15.30 Uhr
    results = de.parse("15.30 Uhr", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 30

    # um 15 Uhr
    results = de.parse("um 15 Uhr", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 0


def test_de_time_expr_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 15:00 - 16:30
    results = de.parse("15:00 - 16:30", ref_date)
    assert len(results) == 1
    dt1 = results[0].moment.datetime()
    assert dt1.hour == 15
    assert dt1.minute == 0
    dt2 = results[0].end.datetime()
    assert dt2.hour == 16
    assert dt2.minute == 30

    # 8:00 Uhr bis 17:00 Uhr
    results = de.parse("8:00 Uhr bis 17:00 Uhr", ref_date)
    assert len(results) == 1
    dt1 = results[0].moment.datetime()
    assert dt1.hour == 8
    assert dt1.minute == 0
    dt2 = results[0].end.datetime()
    assert dt2.hour == 17
    assert dt2.minute == 0
