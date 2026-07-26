import datetime
from chrono_python.locales import fr


def test_fr_time_unit_ago_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # il y a 5 jours
    results = fr.parse("il y a 5 jours, on a fait quelque chose", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "il y a 5 jours"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 5

    # il y a 10 jours
    results = fr.parse("il y a 10 jours, on a fait quelque chose", datetime.datetime(2012, 8, 10, 13, 30))
    assert len(results) == 1
    assert results[0].text == "il y a 10 jours"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 31

    # il y a 15 minutes
    results = fr.parse("il y a 15 minutes", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "il y a 15 minutes"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    # il y a 12 heures
    results = fr.parse("   il y a    12 heures", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "il y a    12 heures"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 14

    # il y a 5 mois
    results = fr.parse("il y a 5 mois, on a fait quelque chose", datetime.datetime(2012, 10, 10))
    assert len(results) == 1
    assert results[0].text == "il y a 5 mois"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 5
    assert dt.day == 10

    # il y a 5 ans
    results = fr.parse("il y a 5 ans, on a fait quelque chose", datetime.datetime(2012, 8, 10, 22, 22))
    assert len(results) == 1
    assert results[0].text == "il y a 5 ans"
    dt = results[0].moment.datetime()
    assert dt.year == 2007
    assert dt.month == 8
    assert dt.day == 10

    # il y a une semaine
    results = fr.parse("il y a une semaine, on a fait quelque chose", datetime.datetime(2012, 8, 3, 8, 34))
    assert len(results) == 1
    assert results[0].text == "il y a une semaine"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 27
