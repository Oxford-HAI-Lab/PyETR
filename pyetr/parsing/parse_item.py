from typing import TypeVar

from pyetr.dependency import Dependency, DependencyRelation
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
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicFunction,
    LogicPredicate,
    Quantified,
    Truth,
    Variable,
)


def _parse_predicate(
    predicate: LogicPredicate,
    variable_map: dict[str, ArbitraryObject],
    predicate_map: dict[str, Predicate],
) -> Atom:
    def _parse_term(item: Item) -> Term | ArbitraryObject | Emphasis:
        if isinstance(item, Variable):
            return variable_map[item.name]
        elif isinstance(item, LogicFunction):
            return _parse_function(item)
        elif isinstance(item, LogicEmphasis):
            inner = _parse_term(item.arg)
            if isinstance(inner, Emphasis):
                raise ValueError(f"Second emphasis found in {inner}")
            return Emphasis(inner)
        elif isinstance(item, Constant):
            return Term(Function(item.name, 0))
        else:
            raise ValueError(f"Invalid item {item}")

    def _parse_function(function: LogicFunction) -> Term:
        new_function = Function(function.name, len(function.args))
        terms: list[Term | ArbitraryObject | Emphasis] = [
            _parse_term(item) for item in function.args
        ]
        return Term(new_function, tuple(terms))

    terms: list[Term | ArbitraryObject | Emphasis] = [
        _parse_term(item) for item in predicate.args
    ]
    if predicate.name not in predicate_map:
        raise ValueError(f"{predicate} not found in predicate map")
    return predicate_map[predicate.name](tuple(terms))


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
        return set_of_states(
            {state({_parse_predicate(item, variable_map, predicate_map)})}
        )

    elif isinstance(item, LogicEmphasis):
        # TODO: Is this correct?
        raise ValueError(f"Logic emphasis {item} found outside of logic predicate")

    elif isinstance(item, LogicFunction):
        raise ValueError(f"Logic function {item} found outside of logic predicate")

    elif isinstance(item, Variable):
        raise ValueError(f"Variable {item} found outside of logic predicate")

    elif isinstance(item, Constant):
        raise ValueError(f"Constant {item} found outside of logic predicate")

    elif isinstance(item, Implies):
        raise ValueError(f"Implies statement {item} found at lower level than top")

    elif isinstance(item, Quantified):
        raise ValueError(f"Quantified {item} found at lower level than top")
    else:
        assert False


def _parse_view(
    view_item: Item,
    dependency_relation: DependencyRelation,
    variable_map: dict[str, ArbitraryObject],
    predicate_map: dict[str, Predicate],
) -> View:
    if isinstance(view_item, Implies):
        supposition = view_item.left
        stage = view_item.right
    else:
        supposition = Truth()
        stage = view_item
    parsed_supposition = _parse_item(supposition, variable_map, predicate_map)
    parsed_stage = _parse_item(stage, variable_map, predicate_map)
    return View(parsed_supposition, parsed_stage, dependency_relation)


Universal = ArbitraryObject
Existential = ArbitraryObject


def get_variable_map_and_dependency_relation(
    quantifieds: list[Quantified],
) -> tuple[dict[str, ArbitraryObject], DependencyRelation]:
    exi_generator = ArbitraryObjectGenerator(is_existential=True)
    uni_generator = ArbitraryObjectGenerator(is_existential=False)
    variable_map: dict[str, ArbitraryObject] = {}
    encountered_universals: list[tuple[Universal, set[Existential]]] = []
    for quantified in quantifieds:
        if quantified.quantifier == "∃":
            arb_obj = next(exi_generator)
            for _, exi_set in encountered_universals:
                exi_set.add(arb_obj)
        else:
            arb_obj = next(uni_generator)
            encountered_universals.append((arb_obj, set()))

        if quantified.variable.name not in variable_map:
            variable_map[quantified.variable.name] = arb_obj
        else:
            raise ValueError(
                f"Variable {quantified.variable.name} appears twice in quantifiers"
            )
    dependencies = [
        Dependency(universal, frozenset(existentials))
        for universal, existentials in encountered_universals
        if len(existentials) > 0
    ]
    return variable_map, DependencyRelation(frozenset(dependencies))


Gatherable = TypeVar("Gatherable", bound=LogicPredicate | LogicFunction | Constant)


# Restructure to be of Item
def gather_item(expr: list[Item], object_type: type[Gatherable]) -> list[Gatherable]:
    out: list[Gatherable] = []
    for item in expr:
        if isinstance(item, object_type):
            out.append(item)
        elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
            out += gather_item(item.operands, object_type)
        elif isinstance(item, BoolNot) or isinstance(item, LogicEmphasis):
            out += gather_item([item.arg], object_type)
        elif isinstance(item, Implies):
            out += gather_item([item.left, item.right], object_type)
        else:
            pass
    return out


def parse_items(expr: list[Item]) -> View:
    view_item = None
    quantifieds: list[Quantified] = []
    for item in expr:
        if isinstance(item, Quantified):
            quantifieds.append(item)
        else:
            assert view_item is None  # There must only be one valid view
            view_item = item
    if view_item is None:
        raise ValueError(f"Main section not found")

    variable_map, dependency_relation = get_variable_map_and_dependency_relation(
        quantifieds
    )

    predicates = gather_item(expr, LogicPredicate)
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
    return _parse_view(view_item, dependency_relation, variable_map, predicate_map)
