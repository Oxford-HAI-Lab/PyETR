from typing import TypeVar

from pyetr.term import ArbitraryObject
from pyetr.tools import ArbitraryObjectGenerator

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

# from ..atom import Predicate as NewPredicate


def gather_atoms(expr: list[Item]) -> list[Atom]:
    out: list[Atom] = []
    for item in expr:
        if isinstance(item, Atom):
            out.append(item)
        elif isinstance(item, Predicate):
            out += item.atom
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
            pass
    return out


def parse_items(expr: list[Item]):
    atoms = gather_atoms(expr)
    arb_object_generator = ArbitraryObjectGenerator(is_existential=True)

    atom_map: dict[str, ArbitraryObject] = {}
    for atom in atoms:
        if atom.var not in atom_map:
            arb_obj = next(arb_object_generator)
            atom_map[atom.var] = arb_obj

    predicates = gather_predicate_or_quantifier(expr, Predicate)
    for predicate in predicates:
        print(predicate.atom)
    print(atom_map)
