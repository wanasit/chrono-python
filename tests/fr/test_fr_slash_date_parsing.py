import datetime
from chrono_python.locales import fr


def test_fr_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 8/2/2016
    results = fr.parse("8/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8/2/2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    # le 8/2/2016
    results = fr.parse("le 8/2/2016", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    # le 8/2
    results = fr.parse("le 8/2", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 2
    assert dt.day == 8


def test_fr_slash_date_weekday():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # lundi 8/2/2016
    results = fr.parse("lundi 8/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].text == "lundi 8/2/2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 2
    assert dt.day == 8

    # samedi 9/2/20
    results = fr.parse("samedi 9/2/20 ", ref_date)
    assert len(results) == 1
    assert results[0].text == "samedi 9/2/20"
    dt = results[0].moment.datetime()
    assert dt.year == 2020
    assert dt.month == 2
    assert dt.day == 9
