import datetime
from chrono_python.locales import it


def test_it_unlikely_format_filtering():
    # Negative cases - Should not parse non-date text
    assert len(it.parse("Questo è solo testo senza date")) == 0
    assert len(it.parse("Ciao come stai")) == 0
    assert len(it.parse("Il prezzo è 1000 euro")) == 0
    assert len(it.parse("Articolo numero 12345")) == 0
    assert len(it.parse("nonoggi")) == 0
    assert len(it.parse("xieri")) == 0
    assert len(it.parse("domaniX")) == 0

    # Numbers that look like dates
    assert len(it.parse("Chiamami al 123456789")) == 0
    assert len(it.parse("Costa 1000")) == 0
    assert len(it.parse("Versione 2.0.1")) == 0
    assert len(it.parse("informazioni")) == 0

    # Strict vs Casual
    assert len(it.parse("venerdì")) > 0
    assert len(it.strict.parse("venerdì")) == 0
