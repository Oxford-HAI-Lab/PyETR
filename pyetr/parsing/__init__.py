__all__ = ["parse_string_to_view"]

from ..view import View
from .parse_item import parse_items
from .parse_string import parse_string


def parse_string_to_view(s: str) -> View:
    return parse_items(parse_string(s))
