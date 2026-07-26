import datetime
from chrono_python.locales import fr
from chrono_python.common.types import CivilTimeComponent


def test_fr_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)

    # maintenant
    results = fr.parse("La deadline est maintenant", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "maintenant"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9
    assert dt.second == 10

    # aujourd'hui
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = fr.parse("La deadline est aujourd'hui", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "aujourd'hui"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # demain
    results = fr.parse("La deadline est demain", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "demain"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # hier
    results = fr.parse("La deadline était hier", ref_date)
    assert len(results) == 1
    assert results[0].index == 18
    assert results[0].text == "hier"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # la veille
    results = fr.parse("La deadline était la veille", ref_date)
    assert len(results) == 1
    assert results[0].index == 18
    assert results[0].text == "la veille"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 0
