__all__ = ["smt_lib_to_views", "views_to_smt_lib"]

from typing import Optional

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.parsing.smt_lib_parser.view_to_smt_lib import views_to_smt_lib

from .parsing.smt_lib_parser import smt_lib_to_view_stores
from .view import View


def smt_lib_to_views(
    smt_lib: str,
    custom_functions: Optional[list[NumFunc | Function]] = None,
) -> list[View]:
    """
    Convert one smt lib string containing multiple Views into a series of Views.

    Args:
        smt_lib (str): The smt lib string
        custom_functions (Optional[list[NumFunc  |  Function]], optional): Custom functions used in the
            string. It assumes the name of the function is that used in the string. Useful
            for using func callers. Defaults to None.

    Returns:
        list[View]: _description_
    """
    return [
        View._from_view_storage(i)
        for i in smt_lib_to_view_stores(smt_lib, custom_functions)
    ]
