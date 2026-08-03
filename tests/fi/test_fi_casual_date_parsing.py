import datetime
from chrono_python.locales import fi
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_fi_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # tänään
    results = fi.parse("tänään", ref_date)
    assert len(results) == 1
    assert results[0].text == "tänään"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # huomenna
    results = fi.parse("huomenna", ref_date)
    assert len(results) == 1
    assert results[0].text == "huomenna"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # eilen
    results = fi.parse("eilen", ref_date)
    assert len(results) == 1
    assert results[0].text == "eilen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # ylihuomenna
    results = fi.parse("ylihuomenna", ref_date)
    assert len(results) == 1
    assert results[0].text == "ylihuomenna"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12

    # toissapäivänä
    results = fi.parse("toissapäivänä", ref_date)
    assert len(results) == 1
    assert results[0].text == "toissapäivänä"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 8


def test_fi_casual_date_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # tänään aamulla
    results = fi.parse("tänään aamulla", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 6

    # tänään aamupäivällä
    results = fi.parse("tänään aamupäivällä", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 9

    # tänään päivällä
    results = fi.parse("tänään päivällä", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 12

    # tänään iltapäivällä
    results = fi.parse("tänään iltapäivällä", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 15

    # tänään illalla
    results = fi.parse("tänään illalla", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 18

    # tänään yöllä
    results = fi.parse("tänään yöllä", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 22

    # tänään keskiyöllä
    results = fi.parse("tänään keskiyöllä", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 0


def test_fi_casual_time_merged_meridiem():
    ref_date = datetime.datetime(2016, 8, 10, 12, 0)

    results = fi.parse("iltapäivällä klo 5", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 17
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) in (Meridiem.PM, Meridiem.PM.value)

    results = fi.parse("illalla klo 8", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 20
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) in (Meridiem.PM, Meridiem.PM.value)
