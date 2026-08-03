import datetime
from chrono_python.locales import uk


def test_uk_time_units_ago():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 5 днів тому
    results = uk.parse("5 днів тому", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 днів тому"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 5, 12, 0)

    # 5 днів 12 годин тому
    results = uk.parse("5 днів 12 годин тому", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 днів 12 годин тому"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 5, 0, 0)

    # півгодини тому
    results = uk.parse("півгодини тому", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "півгодини тому"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 30)

    # декілька днів тому
    results = uk.parse("декілька днів тому", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "декілька днів тому"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 8, 12, 0)

    # декілька секунд тому
    results = uk.parse("декілька секунд тому", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "декілька секунд тому"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 59, 58)
