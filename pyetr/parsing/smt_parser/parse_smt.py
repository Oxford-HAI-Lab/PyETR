from dataclasses import dataclass
from typing import cast

from pysmt.fnode import FNode

from pyetr.parsing.common import Quantified
from pyetr.parsing.view_storage import ViewStorage
from pyetr.stateset import State

from ..fol_parser.parse_item import parse_items
from ..fol_parser.parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Implies,
    Item,
    LogicEmphasis,
    LogicPredicate,
    Variable,
)


class UnsupportedSMT(ValueError):
    pass


@dataclass
class Quant:
    quantifier: str
    variables: list[Variable]


def fnode_to_view(fnode: FNode, quants_seen: list[str]) -> Item:
    if fnode.is_real_constant():
        raise NotImplementedError
    elif fnode.is_and():
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]
        return BoolAnd([output_args])
    elif fnode.is_or():
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]
        return BoolOr([output_args])
    elif fnode.is_function_application():
        name: str = str(fnode.function_name())
        output_args = [fnode_to_view(arg, quants_seen) for arg in fnode.args()]
        return LogicPredicate([name, *output_args])
    elif fnode.is_symbol():
        var_name = str(fnode.symbol_name())
        if var_name in quants_seen:
            return Variable([str(fnode.symbol_name())])
        else:
            return LogicPredicate([var_name])
    elif fnode.is_implies():
        args = fnode.args()
        return Implies(
            [[fnode_to_view(args[0], quants_seen), fnode_to_view(args[1], quants_seen)]]
        )
    elif fnode.is_not():
        return BoolNot([[fnode_to_view(fnode.args()[0], quants_seen)]])
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
            [fnode_to_view(i, quants_seen) for i in fnode.quantifier_vars()],
        )
        if len(fnode_args) == 1:
            arg = fnode_args[0]
            quants_seen.append(quant_vars[0].name)
            new = outer_fnode_to_view(arg, quants_seen)
            quant = Quant(quantifier=quant_name, variables=quant_vars)
            return [Quantified([quant]), *new]
        else:
            raise UnsupportedSMT(fnode)
    else:
        return [fnode_to_view(fnode, quants_seen)]


def smt_to_view(smt: FNode) -> ViewStorage:
    return parse_items(outer_fnode_to_view(smt, []), [])
