from typing import TypeVar

from pyetr.dependency import DependencyRelation
from pyetr.stateset import set_of_states, state
from pyetr.term import ArbitraryObject, Emphasis, Function, Term
from pyetr.tools import ArbitraryObjectGenerator
from pyetr.view import View

from ..atom import Atom, Predicate
from .parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Constant,
    Equals,
    Falsum,
    Implies,
    Item,
    LogicFunction,
    LogicPredicate,
    Quantified,
    Truth,
    Variable,
)


def gather_variables(expr: list[Item]) -> list[Variable]:
    out: list[Variable] = []
    for item in expr:
        if isinstance(item, Variable):
            out.append(item)
        elif isinstance(item, LogicPredicate):
            out += gather_variables(item.args)
        elif isinstance(item, LogicFunction):
            out += gather_variables(item.args)
        elif isinstance(item, Quantified):
            out.append(item.variable)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_variables(item.operands)
        elif isinstance(item, BoolNot):
            out += gather_variables([item.arg])
        elif isinstance(item, Equals) or isinstance(item, Implies):
            out += gather_variables([item.left, item.right])
        elif (
            isinstance(item, Truth)
            or isinstance(item, Falsum)
            or isinstance(item, Constant)
        ):
            pass
        else:
            assert False
    return out


Gatherable = TypeVar("Gatherable", bound=LogicPredicate | Quantified)


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


def _parse_function(
    function: LogicFunction, variable_map: dict[str, ArbitraryObject]
) -> Term:
    new_function = Function(function.name, len(function.args))
    terms: list[Term | ArbitraryObject | Emphasis] = []
    for item in function.args:
        if isinstance(item, Variable):
            terms.append(variable_map[item.name])
        elif isinstance(item, LogicFunction):
            terms.append(_parse_function(item, variable_map))
        # elif isinstance(item, LogicEmphasis):
        #     raise NotImplementedError
        elif isinstance(item, Constant):
            terms.append(Term(Function(item.name, 0)))
        else:
            raise ValueError(f"Invalid item {item}")

    return Term(new_function, tuple(terms))


def _parse_predicate(
    predicate: LogicPredicate, variable_map: dict[str, ArbitraryObject]
) -> Atom:
    new_pred = Predicate(name=predicate.name, arity=len(predicate.args))
    new_items: list[Term | ArbitraryObject | Emphasis] = []
    for item in predicate.args:
        if isinstance(item, Variable):
            new_items.append(variable_map[item.name])
        elif isinstance(item, LogicFunction):
            new_items.append(_parse_function(item, variable_map))
        # elif isinstance(item, LogicEmphasis):
        #     raise NotImplementedError
        elif isinstance(item, Constant):
            new_items.append(Term(Function(item.name, 0)))
        else:
            raise ValueError(f"Invalid item {item}")
    return new_pred(tuple(new_items))


def _parse_item(
    item: Item,
    variable_map: dict[str, ArbitraryObject],
    predicate_map: dict[str, Predicate],
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

    elif isinstance(item, LogicPredicate):
        # based on (vi)
        return set_of_states({state({_parse_predicate(item, variable_map)})})

    elif isinstance(item, LogicFunction):
        raise ValueError(f"Logic function {item} found outside of logic predicate")

    elif isinstance(item, Variable):
        raise ValueError(f"Variable {item} found outside of logic predicate")

    elif isinstance(item, Equals):
        # use equals predicate
        _parse_item(item.left, variable_map, predicate_map)
        _parse_item(item.right, variable_map, predicate_map)
        raise NotImplementedError

    elif isinstance(item, Implies):
        raise ValueError(f"Implies statement {item} found at lower level than top")

    elif isinstance(item, Quantified):
        assert False  # Quantified should not be present here
    else:
        assert False


def _parse_view(
    expr: Item,
    variable_map: dict[str, ArbitraryObject],
    predicate_map: dict[str, Predicate],
) -> View:
    if isinstance(expr, Implies):
        supposition = expr.left
        stage = expr.right
    else:
        supposition = Truth([])
        stage = expr
    parsed_supposition = _parse_item(supposition, variable_map, predicate_map)
    parsed_stage = _parse_item(stage, variable_map, predicate_map)
    return View(parsed_supposition, parsed_stage, DependencyRelation(frozenset({})))


def parse_items(expr: list[Item]) -> View:
    variables = gather_variables(expr)
    arb_object_generator = ArbitraryObjectGenerator(is_existential=True)

    # Build maps
    variable_map: dict[str, ArbitraryObject] = {}
    for variable in variables:
        if variable.name not in variable_map:
            arb_obj = next(arb_object_generator)
            variable_map[variable.name] = arb_obj

    predicates = gather_predicate_or_quantifier(expr, LogicPredicate)
    predicate_map: dict[str, Predicate] = {}
    for predicate in predicates:
        if predicate.name not in predicate_map:
            # predicate name is f_ use Function or arity is 0
            predicate_map[predicate.name] = Predicate(
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
    view = None
    for item in expr:
        if not isinstance(item, Quantified):
            assert view is None  # There must only be one valid view
            view = _parse_view(item, variable_map, predicate_map)
    assert view is not None
    return view
