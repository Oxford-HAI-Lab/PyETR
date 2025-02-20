import typing
from io import StringIO
from typing import Optional

from pysmt.environment import Environment
from pysmt.smtlib.parser import SmtLibParser

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.parsing.smt_parser import smt_to_view
from pyetr.parsing.view_storage import ViewStorage


def smt_lib_to_view(
    smt_lib: str,
    custom_functions: Optional[list[NumFunc | Function]] = None,
    env: typing.Optional[Environment] = None,
) -> ViewStorage:
    if env is None:
        env = Environment()
    parser = SmtLibParser(env)
    script = parser.get_script(StringIO(smt_lib))
    formula = script.get_last_formula()
    return smt_to_view(formula, custom_functions=custom_functions)


def smt_lib_to_view_stores(
    smt_lib: str,
    custom_functions: Optional[list[NumFunc | Function]] = None,
    env: typing.Optional[Environment] = None,
) -> list[ViewStorage]:
    if env is None:
        env = Environment()
    parser = SmtLibParser(Environment())
    script = parser.get_script(StringIO(smt_lib))
    current = script.get_last_formula()
    if current.is_and():
        return [smt_to_view(i, custom_functions) for i in current.args()]
    else:
        return [smt_to_view(current, custom_functions)]
