__all__ = ["parse_string_to_view", "parse_view_to_string"]
from pyetr.view import View

from .parse_string import parse_string as ps
from .parse_view import parse_pv
from .unparse_view import unparse_view


def parse_string_to_view(s: str) -> View:
    return parse_pv(ps(s))


def parse_view_to_string(v: View) -> str:
    return unparse_view(v).to_string()
