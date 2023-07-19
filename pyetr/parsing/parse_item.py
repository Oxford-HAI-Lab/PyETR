from typing import TypeVar

from pyetr.term import ArbitraryObject
from pyetr.tools import ArbitraryObjectGenerator

from .parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Equals,
    Implies,
    Item,
    Predicate,
    Quantified,
    Variable,
)

# from ..atom import Predicate as NewPredicate


def gather_variables(expr: list[Item]) -> list[Variable]:
    out: list[Variable] = []
    for item in expr:
        if isinstance(item, Variable):
            out.append(item)
        elif isinstance(item, Predicate):
            out += item.variables
        elif isinstance(item, Quantified):
            out.append(item.variable)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_variables(item.operands)
        elif isinstance(item, BoolNot):
            out += gather_variables([item.arg])
        elif isinstance(item, Equals) or isinstance(item, Implies):
            out += gather_variables([item.left, item.right])
        else:
            assert False
    return out


Gatherable = TypeVar("Gatherable", bound=Predicate | Quantified)


def gather_predicate_or_quantifier(
    expr: list[Item], object_type: type[Gatherable]
) -> list[Gatherable]:
    out: list[Gatherable] = []
    for item in expr:
        if isinstance(item, object_type):
            out.append(item)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_predicate_or_quantifier(item.operands, object_type)
        elif isinstance(item, BoolNot):
            out += gather_predicate_or_quantifier([item.arg], object_type)
        elif isinstance(item, Equals) or isinstance(item, Implies):
            out += gather_predicate_or_quantifier([item.left, item.right], object_type)
        else:
            pass
    return out


def parse_items(expr: list[Item]):
    variables = gather_variables(expr)
    arb_object_generator = ArbitraryObjectGenerator(is_existential=True)

    variable_map: dict[str, ArbitraryObject] = {}
    for variable in variables:
        if variable.name not in variable_map:
            arb_obj = next(arb_object_generator)
            variable_map[variable.name] = arb_obj

    predicates = gather_predicate_or_quantifier(expr, Predicate)
    for predicate in predicates:
        print(predicate.variables)
    print(variable_map)
