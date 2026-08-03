import datetime
from chrono_python.locales import uk


def test_uk_month_name_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # січень 2012
    results = uk.parse("січень 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "січень 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1

    # Січень 2012 року
    results = uk.parse("Січень 2012 року", ref_date)
    assert len(results) == 1
    assert results[0].text == "Січень 2012 року"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1

    # січ. 2012
    results = uk.parse("січ. 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "січ. 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1

    # вересні 2012
    results = uk.parse("вересні 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "вересні 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 9

    # Month-only expression relative to reference
    ref_date_nov = datetime.datetime(2020, 11, 22, 12, 0)

    results = uk.parse("в січні", ref_date_nov)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в січні"
    dt = results[0].moment.datetime()
    assert dt.year == 2021
    assert dt.month == 1
    assert dt.day == 1

    results = uk.parse("в січ", ref_date_nov)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "в січ"
    dt = results[0].moment.datetime()
    assert dt.year == 2021
    assert dt.month == 1

    results = uk.parse("травень", ref_date_nov)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "травень"
    dt = results[0].moment.datetime()
    assert dt.year == 2021
    assert dt.month == 5

    # Month expression in context
    results = uk.parse("Це було у вересні 2012 перед новим роком", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "у вересні 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 9

    # Year 90s parsing
    results = uk.parse("сер 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "сер 96"
    dt = results[0].moment.datetime()
    assert dt.year == 1996
    assert dt.month == 8

    results = uk.parse("96 сер 96", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "сер 96"
    dt = results[0].moment.datetime()
    assert dt.year == 1996
    assert dt.month == 8
