FULL_MONTH_NAME_DICTIONARY = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

PATTERN_ORDINAL_NUMBER: str = r'[0-9]{1,2}(?:st|nd|rd|th)?'

PATTERN_YEAR: str = r'(?:[1-9][0-9]{0,3}\\s{0,2}(?:BE|AD|BC|BCE|CE)|[1-2][0-9]{3}|[5-9][0-9]|2[0-5])'


def parse_ordinal_number(match_text: str) -> int:
    num = match_text.lower()

    num = num.replace('st', '')
    num = num.replace('nd', '')
    num = num.replace('rd', '')
    num = num.replace('th', '')
    return int(num)


def parse_year(match_text: str) -> int:
    year = match_text.lower()

    year = year.replace('be', '')
    year = year.replace('ad', '')
    year = year.replace('bc', '')
    year = year.replace('bce', '')
    year = year.replace('ce', '')
    return int(year)
