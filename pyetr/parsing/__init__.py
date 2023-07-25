__all__ = ["parse_string_to_view", "parse_view_to_string"]


from ..view import View
from .parse_item import parse_items
from .parse_string import parse_string
from .unparse_item import unparse_items
from .unparse_view import unparse_view


def parse_string_to_view(s: str) -> View:
    return parse_items(parse_string(s))


def parse_view_to_string(v: View) -> str:
    return unparse_items(unparse_view(v))
