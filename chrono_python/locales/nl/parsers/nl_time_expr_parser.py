import re
from chrono_python import chrono
from chrono_python.common.parsers.abstract_time_expr_parser import AbstractTimeExprParser
from chrono_python.common.types import ParsingCivilTimeMoment
from chrono_python.utils.re import Match


class NLTimeExprParser(AbstractTimeExprParser):
    def primary_prefix(self) -> str:
        return r"(^|\s|T|\b)(?:(?:om)\s*)??"

    def following_phase(self) -> str:
        return r"\s*(?:\-|\–|\~|\〜|om|\?)\s*"

    def primary_suffix(self) -> str:
        return r"(?:\s*(?:uur))?(?!/)(?=\W|$)"

    def extract_primary_time_components(
        self, context: chrono.ParsingContext, match: Match
    ) -> ParsingCivilTimeMoment | None:
        # This looks more like a year e.g. 2020
        if re.match(r"^\s*\d{4}\s*$", match.group(0)):
            return None
        return super().extract_primary_time_components(context, match)
