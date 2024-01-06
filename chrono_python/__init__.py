from chrono_python.locales import en
from chrono_python import types

casual = en.casual
strict = en.strict


def parse(text: str, reference: types.Moment | None = None):
    return casual.parse(text, reference)


def parse_date(text: str, reference: types.Moment | None = None):
    return casual.parse_date(text, reference)
