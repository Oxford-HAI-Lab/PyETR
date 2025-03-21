import typing

from pysmt.environment import Environment
from pysmt.fnode import FNode

if typing.TYPE_CHECKING:
    from pyetr.view import View

from io import StringIO

from pysmt.smtlib.script import SmtPrinter
from pysmt.typing import _TypeDecl


def convert_symbol(fnode: FNode):
    t = fnode.get_type()
    if t.is_function_type():
        return (
            f"(declare-fun {fnode.symbol_name()} "
            + "("
            + " ".join(str(arg) for arg in t.param_types)
            + ") "
            + str(t.return_type)
            + ")"
        )
    elif t.is_custom_type():
        return f"(declare-const {fnode.symbol_name()} {t.name})"
    elif t.is_bool_type():
        return f"(declare-const {fnode.symbol_name()} {t.name})"
    else:
        return None


def convert_type(fnode: _TypeDecl):
    if fnode.custom_type:
        return f"(declare-sort {fnode.name} {fnode.arity})"
    return


def format_brackets(text, indent_size=2):
    indent_level = 0
    result = ""
    indent = " " * indent_size
    i = 0
    while i < len(text):
        char = text[i]
        if char == "(":
            if indent_level == 0:
                result += "("
            else:
                result += "\n" + indent * indent_level + "("
            indent_level += 1
        elif char == ")":
            indent_level = max(0, indent_level - 1)
            result += ")"
        else:
            result += char
        i += 1
    return result


def get_main_string(formula):
    buf = StringIO()
    p = SmtPrinter(buf)
    p.printer(formula)
    res = buf.getvalue()
    buf.close()
    return res


def _with_setup(statements: list[str], env: Environment):
    ret = []
    for x in env.type_manager._custom_types_decl.values():
        out = convert_type(x)
        if out is not None:
            ret.append(out)

    for x in env.formula_manager.get_all_symbols():
        out = convert_symbol(x)
        if out is not None:
            ret.append(out)
    for statement in statements:
        ret.append(f"(assert {format_brackets(statement)} )")
    return "\n".join(ret)


def smt_to_smt_lib(smt: FNode, env: Environment) -> str:
    main_string = get_main_string(smt)
    return _with_setup([main_string], env)


def smts_to_smt_lib(smts: list[FNode], env: Environment) -> str:
    statements = [get_main_string(smt) for smt in smts]
    return _with_setup(statements, env)


def view_to_smt_lib(v: "View", env: typing.Optional[Environment] = None):
    if env is None:
        env = Environment()
    return smt_to_smt_lib(v.to_smt(env), env)


def views_to_smt_lib(
    views: list["View"], env: typing.Optional[Environment] = None
) -> str:
    """
    Convert multiple views into a single smt lib string.

    Args:
        views (list[View]): A list of views to convert.
        env (typing.Optional[Environment], optional): The pysmt environment to embed
            parsed variables. If None will use a fresh environment to avoid clashes.
            Defaults to None.

    Returns:
        str: The smt lib string containing multiple views.
    """
    if env is None:
        env = Environment()
    return smts_to_smt_lib([v.to_smt(env) for v in views], env)
