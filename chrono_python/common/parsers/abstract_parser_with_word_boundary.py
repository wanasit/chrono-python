import re
from abc import abstractmethod

from chrono_python import chrono
from chrono_python.types import Moment


# noinspection PyMethodMayBeStatic
class AbstractParserWithWordBoundary(chrono.Parser):
    """A parser that checks and skip word boundaries to applies the 'inner' pattern for actual extraction."""

    @abstractmethod
    def inner_pattern(self) -> re.Pattern:
        """Implement this method to return the inner pattern to apply after the boundary check."""
        raise NotImplementedError()

    @abstractmethod
    def inner_extract(self, context: chrono.ParsingContext, match: re.Match) -> chrono.ParsedResult | Moment | None:
        """Implement this method to extract the result from the inner pattern match."""
        raise NotImplementedError()

    def left_word_boundary(self) -> str:
        """Override this method to return a different left word boundary."""
        return '(\\W|^)'

    def has_inner_pattern_change(self) -> bool:
        """Override this method to return True when the inner pattern has changed.

        By default, the class assumes that the inner pattern never change.
        """
        return False

    def __init__(self):
        self._cached_pattern = None
        self._cached_inner_pattern = None

    def pattern(self) -> re.Pattern:
        if self.has_inner_pattern_change() or self._cached_pattern is None:
            inner_pattern = self.inner_pattern()
            left_word_boundary = self.left_word_boundary()
            self._cached_pattern = re.compile(
                f'{left_word_boundary}{inner_pattern.pattern}', inner_pattern.flags)

        return self._cached_pattern

    # noinspection PyProtectedMember
    def extract(self, context: chrono.ParsingContext, match: chrono.Match):
        inner_match = _create_inner_match_remove_group(match)
        return self.inner_extract(context, inner_match)


# noinspection PyProtectedMember
def _create_inner_match_remove_group(match: chrono.Match, left_boundary_group_index=1):
    """Create a new match with the left boundary group removed."""
    boundary = match.group(left_boundary_group_index)
    inner_group_spans = [(match._group_spans[0][0] + len(boundary), match._group_spans[0][1])]
    inner_group_spans += [g for i, g in enumerate(match._group_spans) if i != left_boundary_group_index]
    inner_group_name_to_index = {name: index - 1 for name, index in match._group_name_to_index.items() if
                                 index != left_boundary_group_index}

    return chrono.Match(match.string, inner_group_spans, inner_group_name_to_index)
