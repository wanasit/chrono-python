import datetime
from chrono_python.locales import it


def test_it_time_unit_later():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    results = it.parse("tra 5 giorni faremo qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "tra 5 giorni"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    results = it.parse("fra 10 giorni faremo qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].text == "fra 10 giorni"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 20

    results = it.parse("tra 15 minuti", ref_date)
    assert len(results) == 1
    assert results[0].text == "tra 15 minuti"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = it.parse("5 minuti dopo", ref_date)
    assert len(results) == 1
    assert results[0].text == "5 minuti dopo"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = it.parse("5 minuti più tardi", ref_date)
    assert len(results) == 1
    assert results[0].text == "5 minuti più tardi"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19
