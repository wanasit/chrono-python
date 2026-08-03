import datetime
from chrono_python.locales import ru


def test_ru_time_unit_within():
    ref_date = datetime.datetime(2012, 8, 10)

    results = ru.parse("будет сделано в течение минуты", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "в течение минуты"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 0, 1)

    results = ru.parse("будет сделано в течение 2 часов.", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "в течение 2 часов"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 2)
