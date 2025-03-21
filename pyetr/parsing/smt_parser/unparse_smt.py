import typing

from pysmt.environment import Environment
from pysmt.fnode import FNode
from pysmt.formula import FormulaManager
from pysmt.typing import BOOL, PySMTType, TypeManager

from pyetr.parsing.common import Quantified, Variable
from pyetr.parsing.fol_items import (
    BoolAnd,
    BoolOr,
    Implies,
    Item,
    LogicPredicate,
    view_to_items,
)
from pyetr.parsing.fol_items.items import (
    BoolNot,
    Falsum,
    LogicEmphasis,
    LogicReal,
    Truth,
)

if typing.TYPE_CHECKING:
    from pyetr.view import View


def items_to_smt(
    items: list[Item],
    formula_manager: FormulaManager,
    u_type: PySMTType,
    type_manager: TypeManager,
):
    def atomic_item_to_smt(item: Item) -> FNode:
        if isinstance(item, Variable):
            return formula_manager.Symbol(item.name, typename=u_type)
        elif isinstance(item, LogicEmphasis):
            return atomic_item_to_smt(item.arg)
        elif isinstance(item, LogicReal):
            return formula_manager.Real(item.num)
        elif isinstance(item, LogicPredicate):
            name = item.name
            assert name != "=="
            params = [atomic_item_to_smt(i) for i in item.args]
            param_types = [param.get_type() for param in params]
            vname = formula_manager.Symbol(
                name=name,
                typename=type_manager.FunctionType(
                    return_type=u_type, param_types=param_types
                ),
            )
            return formula_manager.Function(vname=vname, params=params)
        else:
            raise NotImplementedError(f"{item}, {item.__class__}")

    def item_to_smt(item: Item) -> FNode:
        if isinstance(item, Implies):
            left = item_to_smt(item.left)
            right = item_to_smt(item.right)
            return formula_manager.Implies(left=left, right=right)

        elif isinstance(item, LogicPredicate):
            name = item.name
            if name == "==":
                assert len(item.args) == 2
                is_real = [isinstance(i, LogicReal) for i in item.args]
                if any(is_real) and not all(is_real):
                    if isinstance(item.args[0], LogicReal):
                        new_args = [
                            LogicPredicate("real2const", [item.args[0]]),
                            item.args[1],
                        ]
                    else:
                        new_args = [
                            item.args[0],
                            LogicPredicate("real2const", [item.args[1]]),
                        ]
                else:
                    new_args = item.args
                return formula_manager.Equals(
                    atomic_item_to_smt(new_args[0]), atomic_item_to_smt(new_args[1])
                )
            else:
                params = [atomic_item_to_smt(i) for i in item.args]
                param_types = [param.get_type() for param in params]
                vname = formula_manager.Symbol(
                    name=name,
                    typename=type_manager.FunctionType(
                        return_type=BOOL, param_types=param_types
                    ),
                )
                return formula_manager.Function(vname=vname, params=params)

        elif isinstance(item, BoolAnd):
            return formula_manager.And(*[item_to_smt(i) for i in item.operands])
        elif isinstance(item, BoolOr):
            return formula_manager.Or(*[item_to_smt(i) for i in item.operands])
        elif isinstance(item, BoolNot):
            return formula_manager.Not(item_to_smt(item.arg))
        elif isinstance(item, Truth):
            return formula_manager.TRUE()
        elif isinstance(item, Falsum):
            return formula_manager.FALSE()

        else:
            raise NotImplementedError(f"{item}, {item.__class__}")

    # First separate quantifieds
    view_item = None
    quantifieds: list[Quantified] = []
    for item in items:
        if isinstance(item, Quantified):
            quantifieds.append(item)
        else:
            assert view_item is None  # There must only be one valid view
            view_item = item
    if view_item is None:
        raise ValueError(f"Main section not found")

    # parse main item
    out = item_to_smt(view_item)
    current_quants = []
    last_quantifier = None
    for quant in reversed(quantifieds):
        if last_quantifier is not None and quant.quantifier != last_quantifier:
            if last_quantifier == "∀":
                out = formula_manager.ForAll(current_quants, out)
            else:
                out = formula_manager.Exists(current_quants, out)
            current_quants = []
        current_quants.insert(0, atomic_item_to_smt(quant.variable))
        last_quantifier = quant.quantifier
    if current_quants:
        if last_quantifier == "∀":
            out = formula_manager.ForAll(current_quants, out)
        else:
            out = formula_manager.Exists(current_quants, out)
    return out


def view_to_smt(v: "View", env: typing.Optional[Environment] = None) -> FNode:
    if env is None:
        env = Environment()
    formula_manager = env.formula_manager
    u_type: PySMTType = typing.cast(PySMTType, env.type_manager.Type(name="U"))
    type_manager = env.type_manager
    return items_to_smt(view_to_items(v), formula_manager, u_type, type_manager)
