__all__ = ["parse_string_to_view", "parse_view_to_string"]
from typing import Optional

from pyetr.atoms.terms import Function
from pyetr.view import View

from .parse_string import parse_string as ps
from .parse_view import parse_pv
from .unparse_view import unparse_view


def parse_string_to_view(
    s: str, custom_functions: Optional[list[Function]] = None
) -> View:
    if custom_functions is None:
        custom_functions = []
    return parse_pv(ps(s), custom_functions)


def parse_view_to_string(v: View) -> str:
    return unparse_view(v).to_string()
