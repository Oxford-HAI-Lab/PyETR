from __future__ import annotations

__all__ = ["fol_to_view", "view_to_fol"]

import typing
from typing import Optional, Unpack

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.parsing.common import StringConversion, funcs_converter
from pyetr.parsing.view_storage import ViewStorage

if typing.TYPE_CHECKING:
    from pyetr.view import View

from ..fol_items import items_to_view, view_to_items
from .parse_string import parse_string
from .unparse_item import unparse_items


def fol_to_view(
    s: str, custom_functions: Optional[list[NumFunc | Function]] = None
) -> ViewStorage:
    """
    Parses from first order logic string form to View form.
    Args:
        s (str): A first order logic string
        custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
            string. It assumes the name of the function is that used in the string. Useful
            for using func callers. Defaults to None.

    Returns:
        ViewStorage: The parsed view
    """
    if custom_functions is None:
        custom_functions = []
    return items_to_view(
        parse_string(s), custom_functions=funcs_converter(custom_functions)
    )


def view_to_fol(v: View, **string_conversion_kwargs: Unpack[StringConversion]) -> str:
    """
    Parses from View form to first order logic string form.

    Args:
        v (View): The View object

    Returns:
        str: The first order logic string form.
    """
    return unparse_items(view_to_items(v), **string_conversion_kwargs)
