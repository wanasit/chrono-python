import datetime
from chrono_python.locales import de


def test_de_weekday_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)  # Friday (2012-08-10)

    # Freitag
    results = de.parse("Freitag", ref_date)
    assert len(results) == 1
    assert results[0].text == "Freitag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # am Montag
    results = de.parse("am Montag", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13

    # diesen Montag
    results = de.parse("diesen Montag", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13

    # letzten Montag
    results = de.parse("letzten Montag", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6

    # nächsten Montag
    results = de.parse("nächsten Montag", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13
