import datetime
from chrono_python.locales import de


def test_de_time_unit_relative():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # vor 3 Tagen
    results = de.parse("vor 3 Tagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "vor 3 Tagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 7

    # vor 2 Stunden
    results = de.parse("vor 2 Stunden", ref_date)
    assert len(results) == 1
    assert results[0].text == "vor 2 Stunden"
    dt = results[0].moment.datetime()
    assert dt.hour == 10

    # in 3 Tagen
    results = de.parse("in 3 Tagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "in 3 Tagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13

    # in 2 Stunden
    results = de.parse("in 2 Stunden", ref_date)
    assert len(results) == 1
    assert results[0].text == "in 2 Stunden"
    dt = results[0].moment.datetime()
    assert dt.hour == 14

    # 3 Tage später
    results = de.parse("3 Tage später", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 13

    # letzten Monat
    results = de.parse("letzten Monat", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7

    # nächste Woche
    results = de.parse("nächste Woche", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 17
