import sys
import chrono_python as chrono


def test_parse_function_no_result():
    results = chrono.parse("Hello World")
    assert len(results) == 0


def test_parse_function_success():
    results = chrono.parse("Test : 2013-2-27")
    assert len(results) == 1

    result = results[0]
    assert result.index == 7
    assert result.text == "2013-2-27"


def test_lazy_locale_loading():
    import chrono_python

    # Access Japanese locale lazily
    ja = chrono_python.ja
    assert ja is not None
    assert "chrono_python.locales.ja" in sys.modules

    # Verify Japanese parsing works via lazy access
    results = ja.casual.parse("2026年8月2日")
    assert len(results) == 1
    assert results[0].text == "2026年8月2日"

    # Access French locale lazily
    fr = chrono_python.fr
    assert fr is not None
    assert "chrono_python.locales.fr" in sys.modules


def test_top_level_parse():
    import chrono_python

    results = chrono_python.parse("tomorrow")
    assert len(results) == 1

    date = chrono_python.parse_date("2026-08-02")
    assert date is not None
    assert date.year == 2026
    assert date.month == 8
    assert date.day == 2


def test_dir_contains_locales():
    import chrono_python

    dir_contents = dir(chrono_python)
    for locale_code in ["en", "ja", "fr", "it", "zh"]:
        assert locale_code in dir_contents


def test_direct_locales_import():
    from chrono_python.locales import ja

    results = ja.casual.parse("明日")
    assert len(results) == 1
