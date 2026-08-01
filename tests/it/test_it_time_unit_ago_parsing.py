import datetime
from chrono_python.locales import it


def test_it_time_unit_ago():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    results = it.parse("5 giorni fa abbiamo fatto qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 giorni fa"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 5

    results = it.parse("10 giorni fa abbiamo fatto qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 giorni fa"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 31

    results = it.parse("15 minuti fa", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 minuti fa"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    results = it.parse("un giorno fa abbiamo fatto qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].text == "un giorno fa"
    dt = results[0].moment.datetime()
    assert dt.day == 9

    results = it.parse("una settimana fa abbiamo fatto qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].text == "una settimana fa"
    dt = results[0].moment.datetime()
    assert dt.day == 3
