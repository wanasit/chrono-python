import datetime
from chrono_python.locales import ru


def test_ru_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 17, 10)

    # heute / сегодня
    results = ru.parse("Дедлайн сегодня", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "сегодня"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 17, 10)

    # завтра
    results = ru.parse("Дедлайн завтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "завтра"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 11, 17, 10)

    # послезавтра
    results = ru.parse("Дедлайн послезавтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "послезавтра"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 12, 17, 10)

    # послепослезавтра
    results = ru.parse("Дедлайн послепослезавтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "послепослезавтра"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 13, 17, 10)

    # вчера
    results = ru.parse("Дедлайн вчера", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "вчера"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 9, 17, 10)

    # позавчера
    results = ru.parse("Дедлайн позавчера", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "позавчера"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 8, 17, 10)

    # позапозавчера
    results = ru.parse("Дедлайн позапозавчера", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "позапозавчера"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 7, 17, 10)


def test_ru_casual_time_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)

    # сейчас
    results = ru.parse("Дедлайн сейчас", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "сейчас"
    dt = results[0].moment.datetime()
    assert dt == ref_date.replace(microsecond=0)

    # утром
    results = ru.parse("Дедлайн утром", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "утром"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 6, 0, 0, 0)

    # этим утром
    results = ru.parse("Дедлайн этим утром", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "этим утром"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 6, 0, 0, 0)

    # в полдень
    results = ru.parse("Дедлайн в полдень", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в полдень"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 12, 0, 0, 0)

    # прошлым вечером
    results = ru.parse("Дедлайн прошлым вечером", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "прошлым вечером"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 9, 20, 0, 0, 0)

    # вечером
    results = ru.parse("Дедлайн вечером", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "вечером"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 20, 0, 0, 0)

    # прошлой ночью (hour 8 > 6)
    results = ru.parse("Дедлайн прошлой ночью", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "прошлой ночью"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 0, 0, 0, 0)

    # прошлой ночью (hour 2 <= 6)
    ref_date_night = datetime.datetime(2012, 8, 10, 2, 9, 10, 11)
    results = ru.parse("Дедлайн прошлой ночью", ref_date_night)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "прошлой ночью"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 9, 0, 0, 0, 0)

    # в полночь
    results = ru.parse("Дедлайн в полночь", ref_date_night)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "в полночь"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 10, 0, 0, 0, 0)


def test_ru_casual_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12)

    results = ru.parse("Дедлайн вчера вечером", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "вчера вечером"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 8, 9, 20)

    ref_date = datetime.datetime(2012, 9, 10, 14)
    results = ru.parse("Дедлайн завтра утром", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "завтра утром"
    dt = results[0].moment.datetime()
    assert dt == datetime.datetime(2012, 9, 11, 6)


def test_ru_casual_range():
    ref_date = datetime.datetime(2012, 8, 4, 12)
    results = ru.parse("Событие с сегодня и до послезавтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "с сегодня и до послезавтра"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 4, 12)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 6, 12)

    ref_date = datetime.datetime(2012, 8, 10, 12)
    results = ru.parse("Событие сегодня-завтра", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "сегодня-завтра"
    assert results[0].start.datetime() == datetime.datetime(2012, 8, 10, 12)
    assert results[0].end.datetime() == datetime.datetime(2012, 8, 11, 12)


def test_ru_casual_negative():
    assert len(ru.parse("несегодня")) == 0
    assert len(ru.parse("зявтра")) == 0
    assert len(ru.parse("вчеера")) == 0
