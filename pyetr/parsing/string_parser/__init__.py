__all__ = ["string_to_view", "view_to_string"]

from typing import Optional

from pyetr.atoms.terms import Function
from pyetr.atoms.terms.function import NumFunc
from pyetr.parsing.common import funcs_converter
from pyetr.view import View

from .parse_string import parse_string as ps
from .parse_view import parse_pv
from .unparse_view import unparse_view


def string_to_view(
    s: str, custom_functions: Optional[list[NumFunc | Function]] = None
) -> View:
    """
    Parses from view string form to view form.

    Args:
        s (str): view string
        custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
            string. It assumes the name of the function is that used in the string. Useful
            for using func callers. Defaults to None.

    Returns:
        View: The output view
    """
    if custom_functions is None:
        custom_functions = []
    return parse_pv(ps(s), funcs_converter(custom_functions))


def view_to_string(v: View, **string_conversion_kwargs) -> str:
    """
    Parses from View form to view string form

    Args:
        v (View): The view to convert to string

    Returns:
        str: The view string
    """
    return unparse_view(v).to_string(**string_conversion_kwargs)
