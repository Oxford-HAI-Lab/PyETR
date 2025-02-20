__all__ = ["smt_lib_to_views", "views_to_smt_lib"]

import typing
from typing import Optional

from pysmt.environment import Environment

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.parsing.smt_lib_parser.view_to_smt_lib import views_to_smt_lib

from .parsing.smt_lib_parser import smt_lib_to_view_stores
from .view import View


def smt_lib_to_views(
    smt_lib: str,
    custom_functions: Optional[list[NumFunc | Function]] = None,
    env: typing.Optional[Environment] = None,
) -> list[View]:
    return [
        View._from_view_storage(i)
        for i in smt_lib_to_view_stores(smt_lib, custom_functions, env)
    ]
