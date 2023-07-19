from typing import TypeVar

from pyetr.stateset import set_of_states, state
from pyetr.term import ArbitraryObject
from pyetr.tools import ArbitraryObjectGenerator

from ..atom import Atom
from ..atom import Predicate as NewPredicate
from .parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Equals,
    Falsum,
    Implies,
    Item,
    Predicate,
    Quantified,
    Truth,
    Variable,
)


def gather_variables(expr: list[Item]) -> list[Variable]:
    out: list[Variable] = []
    for item in expr:
        if isinstance(item, Variable):
            out.append(item)
        elif isinstance(item, Predicate):
            out += gather_variables(item.args)
        elif isinstance(item, Quantified):
            out.append(item.variable)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_variables(item.operands)
        elif isinstance(item, BoolNot):
            out += gather_variables([item.arg])
        elif isinstance(item, Equals) or isinstance(item, Implies):
            out += gather_variables([item.left, item.right])
        elif isinstance(item, Truth) or isinstance(item, Falsum):
            pass
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


def _parse_item(
    item: Item,
    variable_map: dict[str, ArbitraryObject],
    predicate_map: dict[str, NewPredicate],
) -> set_of_states:
    # Based on definition 4.16
    if isinstance(item, BoolOr):
        # based on (i)
        new_set = set_of_states(set())
        for operand in item.operands:
            parsed_item: set_of_states = _parse_item(
                operand, variable_map, predicate_map
            )
            new_set |= parsed_item
        return new_set

    elif isinstance(item, BoolAnd):
        # based on (ii)
        new_set = set_of_states(set())
        for operand in item.operands:
            parsed_item: set_of_states = _parse_item(
                operand, variable_map, predicate_map
            )
            new_set *= parsed_item
        return new_set

    elif isinstance(item, BoolNot):
        # based on (iii)
        new_arg = _parse_item(item.arg, variable_map, predicate_map)
        return new_arg.negation()
    elif isinstance(item, Truth):
        # based on (iv)
        return set_of_states({state({})})

    elif isinstance(item, Falsum):
        # based on (v)
        return set_of_states({})

    elif isinstance(item, Predicate):
        # based on (vi)
        new_pred = predicate_map[item.name]
        [_parse_item(i, variable_map, predicate_map) for i in item.args]
        raise NotImplementedError
        new_term = tuple([variable_map[v.name] for v in item.args])
        atom: Atom = new_pred(new_term)
        return set_of_states({state({atom})})

    elif isinstance(item, Variable):
        variable_map[item.name]
        raise NotImplementedError

    elif isinstance(item, Equals):
        _parse_item(item.left, variable_map, predicate_map)
        _parse_item(item.right, variable_map, predicate_map)
        raise NotImplementedError

    elif isinstance(item, Implies):
        _parse_item(item.left, variable_map, predicate_map)
        _parse_item(item.right, variable_map, predicate_map)
        raise NotImplementedError

    elif isinstance(item, Quantified):
        assert False  # Quantified should not be present here

    else:
        assert False


def parse_items(expr: list[Item]) -> set_of_states:
    variables = gather_variables(expr)
    print(variables)
    arb_object_generator = ArbitraryObjectGenerator(is_existential=True)

    # Build maps
    variable_map: dict[str, ArbitraryObject] = {}
    for variable in variables:
        if variable.name not in variable_map:
            arb_obj = next(arb_object_generator)
            variable_map[variable.name] = arb_obj

    predicates = gather_predicate_or_quantifier(expr, Predicate)
    predicate_map: dict[str, NewPredicate] = {}
    for predicate in predicates:
        if predicate.name not in predicate_map:
            predicate_map[predicate.name] = NewPredicate(
                name=predicate.name, arity=len(predicate.args)
            )
        else:
            existing_predicate = predicate_map[predicate.name]
            if existing_predicate.arity != len(predicate.args):
                raise ValueError(
                    f"Parsing predicate {predicate} has different arity than existing {existing_predicate}"
                )
    # Parse items
    # Ignore quantified
    new_item = None
    for item in expr:
        if not isinstance(item, Quantified):
            assert new_item is None  # There must only be one valid term
            new_item = _parse_item(item, variable_map, predicate_map)
    assert new_item is not None
    return new_item
