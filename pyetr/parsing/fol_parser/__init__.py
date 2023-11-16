__all__ = ["fol_to_view", "view_to_fol"]


from typing import Optional

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.parsing.common import funcs_converter
from pyetr.view import View

from .parse_item import parse_items
from .parse_string import parse_string
from .unparse_item import unparse_items
from .unparse_view import unparse_view


def fol_to_view(
    s: str, custom_functions: Optional[list[NumFunc | Function]] = None
) -> View:
    """
    Parses from first order logic string form to View form.
    Args:
        s (str): A first order logic string
        custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
            string. It assumes the name of the function is that used in the string. Useful
            for using func callers. Defaults to None.

    Returns:
        View: The parsed view
    """
    if custom_functions is None:
        custom_functions = []
    return parse_items(
        parse_string(s), custom_functions=funcs_converter(custom_functions)
    )


def view_to_fol(v: View) -> str:
    """
    Parses from View form to first order logic string form.

    Args:
        v (View): The View object

    Returns:
        str: The first order logic string form.
    """
    return unparse_items(unparse_view(v))
