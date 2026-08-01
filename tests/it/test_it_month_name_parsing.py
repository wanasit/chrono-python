import datetime
from chrono_python.locales import it


def test_it_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10)

    # 10 agosto 2012
    results = it.parse("10 agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 agosto 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # 3 febbraio 82
    results = it.parse("3 febbraio 82", ref_date)
    assert len(results) == 1
    assert results[0].text == "3 febbraio 82"
    dt = results[0].moment.datetime()
    assert dt.year == 1982
    assert dt.month == 2
    assert dt.day == 3

    # il 10 agosto
    results = it.parse("La scadenza è il 10 agosto", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "il 10 agosto"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # settembre 2012
    results = it.parse("settembre 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "settembre 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 9
    assert dt.day == 1

    # Sarà a settembre
    results = it.parse("Sarà a settembre", ref_date)
    assert len(results) == 1
    assert results[0].index == 7
    assert results[0].text == "settembre"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 9
    assert dt.day == 1

    # agosto 10, 2012
    results = it.parse("agosto 10, 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "agosto 10, 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10


def test_it_month_name_ordinal():
    ref_date = datetime.datetime(2012, 8, 10)

    results = it.parse("primo maggio", ref_date)
    assert len(results) == 1
    assert results[0].text == "primo maggio"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 5
    assert dt.day == 1

    results = it.parse("secondo agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "secondo agosto 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 2
