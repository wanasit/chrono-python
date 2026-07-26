import datetime
from chrono_python.locales import fr


def test_fr_time_unit_relative():
    ref_date = datetime.datetime(2017, 5, 12, 12, 0)

    # la semaine prochaine
    results = fr.parse("la semaine prochaine", ref_date)
    assert len(results) == 1
    assert results[0].text == "la semaine prochaine"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 5
    assert dt.day == 19

    # les 2 prochaines semaines
    results = fr.parse("les 2 prochaines semaines", datetime.datetime(2017, 5, 12, 18, 11))
    assert len(results) == 1
    assert results[0].text == "les 2 prochaines semaines"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 5
    assert dt.day == 26
    assert dt.hour == 18
    assert dt.minute == 11

    # les trois prochaines semaines
    results = fr.parse("les trois prochaines semaines", ref_date)
    assert len(results) == 1
    assert results[0].text == "les trois prochaines semaines"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 6
    assert dt.day == 2

    # le mois dernier
    results = fr.parse("le mois dernier", ref_date)
    assert len(results) == 1
    assert results[0].text == "le mois dernier"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 4
    assert dt.day == 12

    # les 30 jours précédents
    results = fr.parse("les 30 jours précédents", ref_date)
    assert len(results) == 1
    assert results[0].text == "les 30 jours précédents"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 4
    assert dt.day == 12

    # les 24 heures passées
    results = fr.parse("les 24 heures passées", datetime.datetime(2017, 5, 12, 11, 27))
    assert len(results) == 1
    assert results[0].text == "les 24 heures passées"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 5
    assert dt.day == 11
    assert dt.hour == 11
    assert dt.minute == 27

    # les 90 secondes suivantes
    results = fr.parse("les 90 secondes suivantes", datetime.datetime(2017, 5, 12, 11, 27, 3))
    assert len(results) == 1
    assert results[0].text == "les 90 secondes suivantes"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 28
    assert dt.second == 33

    # les huit dernieres minutes
    results = fr.parse("les huit dernieres minutes", datetime.datetime(2017, 5, 12, 11, 27))
    assert len(results) == 1
    assert results[0].text == "les huit dernieres minutes"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    # le dernier trimestre
    results = fr.parse("le dernier trimestre", datetime.datetime(2017, 5, 12, 11, 27))
    assert len(results) == 1
    assert results[0].text == "le dernier trimestre"
    dt = results[0].moment.datetime()
    assert dt.month == 2

    # l'année prochaine
    results = fr.parse("l'année prochaine", datetime.datetime(2017, 5, 12, 11, 27))
    assert len(results) == 1
    assert results[0].text == "l'année prochaine"
    dt = results[0].moment.datetime()
    assert dt.year == 2018


def test_fr_time_unit_relative_negative():
    ref_date = datetime.datetime(2017, 5, 12)
    assert len(fr.parse("le mois d'avril", ref_date)) == 0
    assert len(fr.parse("la derniere homme", ref_date)) == 0
