import datetime
from chrono_python.locales import it


def test_it_time_unit_within():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    results = it.parse("entro 5 giorni faremo qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "entro 5 giorni"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    results = it.parse("entro 15 minuti", ref_date)
    assert len(results) == 1
    assert results[0].text == "entro 15 minuti"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = it.parse("entro un giorno faremo qualcosa", ref_date)
    assert len(results) == 1
    assert results[0].text == "entro un giorno"
    dt = results[0].moment.datetime()
    assert dt.day == 11
