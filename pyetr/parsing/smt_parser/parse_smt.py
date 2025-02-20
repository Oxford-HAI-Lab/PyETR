from typing import Optional, cast

from pysmt.fnode import FNode

from pyetr.atoms.terms import Function
from pyetr.atoms.terms.function import NumFunc
from pyetr.parsing.common import Quantified, funcs_converter
from pyetr.parsing.fol_items.items import LogicReal
from pyetr.parsing.view_storage import ViewStorage

from ..fol_items import items_to_view
from ..fol_parser.parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Falsum,
    Implies,
    Item,
    LogicPredicate,
    Truth,
    Variable,
)


class UnsupportedSMT(ValueError):
    pass


def fnode_to_view(fnode: FNode, quants_seen: list[str]) -> Item:
    if fnode.is_real_constant():
        return LogicReal(float(fnode.constant_value()))
    elif fnode.is_and():
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]
        return BoolAnd(output_args)
    elif fnode.is_or():
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]
        return BoolOr(output_args)
    elif fnode.is_function_application():
        name: str = str(fnode.function_name())
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]

        return LogicPredicate(name, output_args)
    elif fnode.is_symbol():
        var_name = str(fnode.symbol_name())
        if var_name in quants_seen:
            return Variable(str(fnode.symbol_name()))
        else:
            return LogicPredicate(var_name, [])
    elif fnode.is_implies():
        args = fnode.args()
        return Implies(
            fnode_to_view(args[0], quants_seen), fnode_to_view(args[1], quants_seen)
        )
    elif fnode.is_not():
        return BoolNot(fnode_to_view(fnode.args()[0], quants_seen))
    elif fnode.is_equals() or fnode.is_iff():
        return LogicPredicate(
            name="==", args=[fnode_to_view(i, quants_seen) for i in fnode.args()]
        )
    elif fnode.is_true():
        return Truth()
    elif fnode.is_false():
        return Falsum()
    else:
        opts = dir(fnode)
        output = {}
        for k in opts:
            attr = getattr(fnode, k)
            if callable(attr) and k[0:2] == "is":
                if attr():
                    output[k] = attr()
        raise UnsupportedSMT(fnode, output)


def outer_fnode_to_view(fnode: FNode, quants_seen: list[str]) -> list[Item]:
    if fnode.is_quantifier():
        if fnode.is_exists():
            quant_name = "E"
        elif fnode.is_forall():
            quant_name = "A"
        else:
            assert False
        fnode_args = fnode.args()
        quant_vars: list[Variable] = cast(
            list[Variable],
            [fnode_to_view(i, []) for i in fnode.quantifier_vars()],
        )
        if len(fnode_args) == 1:
            arg = fnode_args[0]
            for q in quant_vars:
                quants_seen.append(q.name)
            new = outer_fnode_to_view(arg, quants_seen)
            return [
                Quantified(variable=i, quantifier=quant_name) for i in quant_vars
            ] + new
        else:
            raise UnsupportedSMT(fnode)
    else:
        return [fnode_to_view(fnode, quants_seen)]


def check_for_multiple(fnode: FNode):
    def _check_sub(sub: FNode):
        if sub.is_quantifier():
            return True
        elif sub.is_implies():
            return True
        else:
            return False

    if fnode.is_and():
        for arg in fnode.args():
            if _check_sub(arg):
                raise UnsupportedSMT(
                    str(fnode)
                    + "\n\n"
                    + "Did you mean to parse multiple views? Please use associated function"
                )


def smt_to_view(
    smt: FNode, custom_functions: Optional[list[NumFunc | Function]] = None
) -> ViewStorage:
    check_for_multiple(smt)
    if custom_functions is None:
        custom_functions = []
    return items_to_view(
        outer_fnode_to_view(smt, []), custom_functions=funcs_converter(custom_functions)
    )
