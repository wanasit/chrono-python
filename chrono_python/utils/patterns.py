import re

PATTERN_CAPTURE_GROUP_OPENING_COMPILED = re.compile(r'\((?!\?:)')


def repeat(
        pattern: str,
        prefix: str = '',
        pattern_connector: str = '\\s{0,5},?\\s{0,5}'
) -> str:
    # Remove the capture groups by replacing them with non-capture groups.
    pattern = PATTERN_CAPTURE_GROUP_OPENING_COMPILED.sub('(?:', pattern)
    return f'{prefix}{pattern}(?:{pattern_connector}{pattern}){{0,10}}'


def match_any(dictionary: dict[str, any]) -> str:
    joined_terms = '|'.join(sorted(dictionary.keys(), reverse=True)).replace('.', '\\.')
    return f'(?:{joined_terms})'
