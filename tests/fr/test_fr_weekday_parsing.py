import datetime
from chrono_python.locales import fr


def test_fr_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thursday

    # Lundi
    results = fr.parse("Lundi", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Lundi"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6

    # Jeudi
    results = fr.parse("Jeudi", ref_date)
    assert len(results) == 1
    assert results[0].text == "Jeudi"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # Dimanche
    results = fr.parse("Dimanche", ref_date)
    assert len(results) == 1
    assert results[0].text == "Dimanche"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12

    # vendredi dernier
    results = fr.parse("la deadline était vendredi dernier...", ref_date)
    assert len(results) == 1
    assert results[0].index == 18
    assert results[0].text == "vendredi dernier"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 3

    # vendredi prochain
    ref_date_apr = datetime.datetime(2015, 4, 18, 12, 0)
    results = fr.parse("Planifions une réuinion vendredi prochain", ref_date_apr)
    assert len(results) == 1
    assert results[0].index == 24
    assert results[0].text == "vendredi prochain"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 4
    assert dt.day == 24


def test_fr_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # Dimanche 7 décembre 2014
    results = fr.parse("Dimanche 7 décembre 2014", ref_date)
    assert len(results) == 1
    assert results[0].text == "Dimanche 7 décembre 2014"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 12
    assert dt.day == 7

    # Dimanche 7/12/2014
    results = fr.parse("Dimanche 7/12/2014", ref_date)
    assert len(results) == 1
    assert results[0].text == "Dimanche 7/12/2014"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 12
    assert dt.day == 7
