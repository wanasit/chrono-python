import datetime
from chrono_python.locales import uk


def test_uk_time_units_within():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # буде зроблено протягом хвилини
    results = uk.parse("буде зроблено протягом хвилини", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "протягом хвилини"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 0, 1)

    # буде виконано на протязі 2 годин.
    results = uk.parse("буде виконано на протязі 2 годин.", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "на протязі 2 годин"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 2, 0)


def test_uk_time_units_within_word_boundary():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    results = uk.parse("купив 5 годинників", ref_date)
    assert len(results) == 0
