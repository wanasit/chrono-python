import datetime
from chrono_python.locales import fi


def test_fi_casual_time_alone():
    ref_date = datetime.datetime(2012, 8, 10, 14, 0)

    # aamulla
    results = fi.parse("aamulla", ref_date)
    assert len(results) == 1
    assert results[0].text == "aamulla"
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert dt.minute == 0

    # aamuna
    results = fi.parse("aamuna", ref_date)
    assert len(results) == 1
    assert results[0].text == "aamuna"
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert dt.minute == 0

    # aamupäivällä
    results = fi.parse("aamupäivällä", ref_date)
    assert len(results) == 1
    assert results[0].text == "aamupäivällä"
    dt = results[0].moment.datetime()
    assert dt.hour == 9
    assert dt.minute == 0

    # päivällä
    results = fi.parse("päivällä", ref_date)
    assert len(results) == 1
    assert results[0].text == "päivällä"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 0

    # iltapäivällä
    results = fi.parse("iltapäivällä", ref_date)
    assert len(results) == 1
    assert results[0].text == "iltapäivällä"
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 0

    # illalla
    results = fi.parse("illalla", ref_date)
    assert len(results) == 1
    assert results[0].text == "illalla"
    dt = results[0].moment.datetime()
    assert dt.hour == 18
    assert dt.minute == 0

    # yöllä
    results = fi.parse("yöllä", ref_date)
    assert len(results) == 1
    assert results[0].text == "yöllä"
    dt = results[0].moment.datetime()
    assert dt.hour == 22
    assert dt.minute == 0

    # keskiyöllä
    results = fi.parse("keskiyöllä", ref_date)
    assert len(results) == 1
    assert results[0].text == "keskiyöllä"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 0


def test_fi_casual_time_last_night():
    ref_date = datetime.datetime(2012, 8, 10, 14, 0)

    results = fi.parse("viime yönä", ref_date)
    assert len(results) == 1
    assert results[0].text == "viime yönä"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 0
