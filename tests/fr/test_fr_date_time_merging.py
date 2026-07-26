import datetime
from chrono_python.locales import fr


def test_fr_date_time_merging():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 12 juillet à 19:00
    results = fr.parse("12 juillet à 19:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "12 juillet à 19:00"
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.day == 12
    assert dt.hour == 19
    assert dt.minute == 0

    # 5 mai 12:00
    results = fr.parse("5 mai 12:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "5 mai 12:00"
    dt = results[0].moment.datetime()
    assert dt.month == 5
    assert dt.day == 5
    assert dt.hour == 12

    # aujourd'hui 17:00
    results = fr.parse("La deadline est aujourd'hui 17:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "aujourd'hui 17:00"
    dt = results[0].moment.datetime()
    assert dt.day == 10
    assert dt.hour == 17

    # demain 17:00
    results = fr.parse("La deadline est demain 17:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "demain 17:00"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 17

    # demain matin 11h
    results = fr.parse("La deadline est demain matin 11h", ref_date)
    assert len(results) == 1
    assert results[0].text == "demain matin 11h"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 11

    # après-midi à 5
    results = fr.parse("après-midi à 5", datetime.datetime(2016, 8, 10, 12, 0))
    assert len(results) == 1
    assert results[0].text == "après-midi à 5"
    assert results[0].moment.datetime().hour == 17

    # soir à 8
    results = fr.parse("soir à 8", datetime.datetime(2016, 8, 10, 12, 0))
    assert len(results) == 1
    assert results[0].text == "soir à 8"
    assert results[0].moment.datetime().hour == 20

    # 2014-04-18 à 3h00
    results = fr.parse("Quelque chose se passe le 2014-04-18 à 3h00", ref_date)
    assert len(results) == 1
    assert results[0].text == "2014-04-18 à 3h00"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 4
    assert dt.day == 18
    assert dt.hour == 3

    # 10 Août 2012 à 10:12:59
    results = fr.parse("Quelque chose se passe le 10 Août 2012 à 10:12:59", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Août 2012 à 10:12:59"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 10
    assert dt.minute == 12
    assert dt.second == 59

    # 15juin 2016 20h
    results = fr.parse("Quelque chose se passe le 15juin 2016 20h", datetime.datetime(2016, 7, 10))
    assert len(results) == 1
    assert results[0].text == "15juin 2016 20h"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 20

    # 2014-04-18 7:00 - 8h00
    results = fr.parse("Quelque chose se passe le 2014-04-18 7:00 - 8h00 ...", ref_date)
    assert len(results) == 1
    assert results[0].text == "2014-04-18 7:00 - 8h00"
    assert results[0].start.datetime().hour == 7
    assert results[0].end.datetime().hour == 8

    # 2014-04-18 de 7:00 à 20:00
    results = fr.parse("Quelque chose se passe le 2014-04-18 de 7:00 à 20:00 ...", ref_date)
    assert len(results) == 1
    assert results[0].text == "2014-04-18 de 7:00 à 20:00"
    assert results[0].start.datetime().hour == 7
    assert results[0].end.datetime().hour == 20
