__all__ = ["fol_to_view", "view_to_fol"]


from pyetr.view import View

from .parse_item import parse_items
from .parse_string import parse_string
from .unparse_item import unparse_items
from .unparse_view import unparse_view


def fol_to_view(s: str) -> View:
    """
    Parses from first order logic string form to View form.
    Args:
        s (str): A first order logic string

    Returns:
        View: The parsed view
    """
    return parse_items(parse_string(s))


def view_to_fol(v: View) -> str:
    """
    Parses from View form to first order logic string form.

    Args:
        v (View): The View object

    Returns:
        str: The first order logic string form.
    """
    return unparse_items(unparse_view(v))
