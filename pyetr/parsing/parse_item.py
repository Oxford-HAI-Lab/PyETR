from typing import TypeVar

from .parse_string import (
    Atom,
    BoolAnd,
    BoolNot,
    BoolOr,
    Equals,
    Implies,
    Item,
    Predicate,
    Quantified,
)


def gather_atoms(expr: list[Item]) -> list[Atom]:
    out: list[Atom] = []
    for item in expr:
        if isinstance(item, Atom):
            out.append(item)
        elif isinstance(item, Predicate):
            out.append(item.atom)
        elif isinstance(item, Quantified):
            out.append(item.atom)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_atoms(item.operands)
        elif isinstance(item, BoolNot):
            out += gather_atoms([item.arg])
        elif isinstance(item, Equals) or isinstance(item, Implies):
            out += gather_atoms([item.left, item.right])
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
            assert False
    return out
