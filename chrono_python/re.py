import re

class Match:
    """A class represents the result of a regular expression match.

    Chrono uses this class internally instead of `re.Match` to enable modifying or augmenting the result.
    Every method follows the re.Match's method of the same name.

    Ref: https://docs.python.org/3/library/re.html#match-objects
    """

    def __init__(self, string: str,
                 group_spans: list[tuple[int, int]],
                 group_name_to_index: dict[str, int]):
        self._string = string
        self._group_spans = group_spans
        self._group_name_to_index = group_name_to_index

    @staticmethod
    def from_re_match(match: re.Match) -> 'Match':
        group_spans = [match.span(i) for i in range(match.re.groups + 1)]
        group_name_to_index = {name: i for name, i in match.re.groupindex.items()}
        return Match(match.string, group_spans, group_name_to_index)

    @property
    def string(self) -> str:
        return self._string

    def __getitem__(self, item):
        return self.group(item)

    def groups(self) -> list[str | None]:
        return [self.group(i) for i in range(len(self._group_spans))]

    def group(self, index: int | str) -> str | None:
        if isinstance(index, str):
            index = self._group_name_to_index[index]
        if index < 0 or index >= len(self._group_spans):
            raise IndexError(f'Group index {index} out of range')

        span = self._group_spans[index]
        if span == (-1, -1):
            return None

        return self._string[span[0]:span[1]]

    def start(self, group=0) -> int:
        return self._group_spans[group][0]

    def end(self, group=0) -> int:
        return self._group_spans[group][1]
