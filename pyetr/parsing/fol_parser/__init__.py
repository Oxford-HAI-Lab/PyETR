__all__ = ["fol_to_view", "view_to_fol"]


from pyetr.view import View

from .parse_item import parse_items
from .parse_string import parse_string
from .unparse_item import unparse_items
from .unparse_view import unparse_view


def fol_to_view(s: str, add_emphasis: bool = False) -> View:
    return parse_items(parse_string(s), add_emphasis=add_emphasis)


def view_to_fol(v: View) -> str:
    return unparse_items(unparse_view(v))
