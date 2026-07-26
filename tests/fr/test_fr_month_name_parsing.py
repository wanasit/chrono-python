import datetime
from chrono_python.locales import fr


def test_fr_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10 Août 2012
    results = fr.parse("10 Août 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Août 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # 8 Février
    results = fr.parse("8 Février", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8 Février"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 2
    assert dt.day == 8

    # 1er Août 2012
    results = fr.parse("1er Août 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "1er Août 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 1

    # 10 Août 234 AC
    results = fr.parse("10 Août 234 AC", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Août 234 AC"
    from chrono_python.common.types import CivilTimeComponent
    assert results[0].moment.get(CivilTimeComponent.YEAR) == -234
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    # 10 Août 88 p. Chr. n.
    results = fr.parse("10 Août 88 p. Chr. n.", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Août 88 p. Chr. n."
    dt = results[0].moment.datetime()
    assert dt.year == 88
    assert dt.month == 8
    assert dt.day == 10

    # Dim 15 Sept
    results = fr.parse("Dim 15 Sept", datetime.datetime(2013, 8, 10))
    assert len(results) == 1
    assert results[0].text == "Dim 15 Sept"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 9
    assert dt.day == 15

    # 31 mars 2016
    results = fr.parse("31 mars 2016", ref_date)
    assert len(results) == 1
    assert results[0].text == "31 mars 2016"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 3
    assert dt.day == 31


def test_fr_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10 - 22 août 2012
    results = fr.parse("10 - 22 août 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 - 22 août 2012"
    start_dt = results[0].start.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 10
    end_dt = results[0].end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 22

    # 10 au 22 août 2012
    results = fr.parse("10 au 22 août 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 au 22 août 2012"
    start_dt = results[0].start.datetime()
    assert start_dt.day == 10
    end_dt = results[0].end.datetime()
    assert end_dt.day == 22


def test_fr_month_name_unaccentuated():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = fr.parse("10 Aout 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Aout 2012"
    assert results[0].moment.datetime().month == 8

    results = fr.parse("10 Fevrier 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Fevrier 2012"
    assert results[0].moment.datetime().month == 2

    results = fr.parse("10 Decembre 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 Decembre 2012"
    assert results[0].moment.datetime().month == 12


def test_fr_month_name_abbreviated():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = fr.parse("12 juil. 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "12 juil. 2012"
    assert results[0].moment.datetime().month == 7

    results = fr.parse("15 déc. 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 déc. 2012"
    assert results[0].moment.datetime().month == 12

    results = fr.parse("15 déc 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 déc 2012"
    assert results[0].moment.datetime().month == 12

    results = fr.parse("1 janv. 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "1 janv. 2012"
    assert results[0].moment.datetime().month == 1

    results = fr.parse("22 févr. 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "22 févr. 2012"
    assert results[0].moment.datetime().month == 2


def test_fr_month_name_impossible():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    assert len(fr.parse("32 Août 2014", ref_date)) == 0
    assert len(fr.parse("29 Février 2014", ref_date)) == 0
    assert len(fr.parse("32 Aout", ref_date)) == 0
    assert len(fr.parse("29 Fevrier", datetime.datetime(2013, 8, 10))) == 0
