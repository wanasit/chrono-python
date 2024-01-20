import re


def match_any(dictionary: dict[str, any]) -> str:
    joined_terms = '|'.join(sorted(dictionary.keys())).replace('.', '\\.')
    return f'(?:{joined_terms})'
