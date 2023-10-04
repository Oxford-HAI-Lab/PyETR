__all__ = ["parse_string_to_view"]
from pyetr.view import View

from .parse_string import parse_string as ps
from .parse_view import parse_pv


def parse_string_to_view(s: str) -> View:
    return parse_pv(ps(s))
