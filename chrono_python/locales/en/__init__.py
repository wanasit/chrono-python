from chrono_python import chrono
from chrono_python.common import parsers as common_parsers

configuration = chrono.Configuration(
    parsers=[common_parsers.ISOFormatParser()],
    refiners=[])
casual = chrono.Chrono(configuration)
strict = chrono.Chrono(configuration)


def parse(text: str, reference, options):
    return casual.parse(text, reference, options)
