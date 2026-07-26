import datetime
from chrono_python.locales import fr


def test_fr_time_unit_within_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # dans 5 jours
    results = fr.parse("On doit faire quelque chose dans 5 jours.", ref_date)
    assert len(results) == 1
    assert results[0].index == 28
    assert results[0].text == "dans 5 jours"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # dans cinq jours
    results = fr.parse("On doit faire quelque chose dans cinq jours.", datetime.datetime(2012, 8, 10, 11, 12))
    assert len(results) == 1
    assert results[0].index == 28
    assert results[0].text == "dans cinq jours"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # dans 5 minutes
    results = fr.parse("dans 5 minutes", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "dans 5 minutes"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    # pour 5 minutes
    results = fr.parse("pour 5 minutes", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "pour 5 minutes"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    # en 1 heure
    results = fr.parse("en 1 heure", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "en 1 heure"
    dt = results[0].moment.datetime()
    assert dt.hour == 13

    # de 5 minutes
    results = fr.parse("régler une minuterie de 5 minutes", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].index == 21
    assert results[0].text == "de 5 minutes"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    # dans deux semaines
    results = fr.parse("dans deux semaines", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "dans deux semaines"
    dt = results[0].moment.datetime()
    assert dt.day == 24

    # dans un mois
    results = fr.parse("dans un mois", datetime.datetime(2012, 8, 10, 7, 14))
    assert len(results) == 1
    assert results[0].text == "dans un mois"
    dt = results[0].moment.datetime()
    assert dt.month == 9

    # dans quelques mois
    results = fr.parse("dans quelques mois", datetime.datetime(2012, 7, 10, 22, 14))
    assert len(results) == 1
    assert results[0].text == "dans quelques mois"
    dt = results[0].moment.datetime()
    assert dt.month == 10

    # en une année
    results = fr.parse("en une année", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "en une année"
    dt = results[0].moment.datetime()
    assert dt.year == 2013

    # dans une Année
    results = fr.parse("dans une Année", datetime.datetime(2012, 8, 10, 12, 14))
    assert len(results) == 1
    assert results[0].text == "dans une Année"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
