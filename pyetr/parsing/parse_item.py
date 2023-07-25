from dataclasses import dataclass
from typing import overload

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


@dataclass
class Maps:
    variable_map: dict[str, ArbitraryObject]
    predicate_map: dict[str, Predicate]
    function_map: dict[str, Function]
    constant_map: dict[str, Function]


def _parse_predicate(predicate: LogicPredicate, maps: Maps) -> Atom:
    def _parse_term(item: Item) -> Term | ArbitraryObject | Emphasis:
        if isinstance(item, Variable):
            return maps.variable_map[item.name]
        elif isinstance(item, LogicFunction):
            return _parse_function(item)
        elif isinstance(item, LogicEmphasis):
            inner = _parse_term(item.arg)
            if isinstance(inner, Emphasis):
                raise ValueError(f"Second emphasis found in {inner}")
            return Emphasis(inner)
        elif isinstance(item, Constant):
            return _parse_constant(item)
        else:
            raise ValueError(f"Invalid item {item}")

    def _parse_constant(constant: Constant) -> Term:
        if constant.name not in maps.constant_map:
            raise ValueError(f"{constant} not found in constant map")
        return Term(maps.constant_map[constant.name])

    def _parse_function(function: LogicFunction) -> Term:
        if function.name not in maps.function_map:
            raise ValueError(f"{function} not found in function map")
        terms: list[Term | ArbitraryObject | Emphasis] = [
            _parse_term(item) for item in function.args
        ]
        if len(terms) == 0:
            new_terms = None
        else:
            new_terms = tuple(terms)
        return Term(maps.function_map[function.name], new_terms)

    terms: list[Term | ArbitraryObject | Emphasis] = [
        _parse_term(item) for item in predicate.args
    ]
    if predicate.name not in maps.predicate_map:
        raise ValueError(f"{predicate} not found in predicate map")
    return maps.predicate_map[predicate.name](tuple(terms))


def _parse_item(item: Item, maps: Maps) -> set_of_states:
    # Based on definition 4.16
    if isinstance(item, BoolOr):
        # based on (i)
        new_set = set_of_states(set())
        for operand in item.operands:
            parsed_item: set_of_states = _parse_item(operand, maps)
            new_set |= parsed_item
        return new_set

    elif isinstance(item, BoolAnd):
        # based on (ii)
        new_set = set_of_states({state(set())})
        for operand in item.operands:
            parsed_item: set_of_states = _parse_item(operand, maps)
            new_set *= parsed_item
        return new_set

    elif isinstance(item, BoolNot):
        # based on (iii)
        new_arg = _parse_item(item.arg, maps)
        return new_arg.negation()
    elif isinstance(item, Truth):
        # based on (iv)
        return set_of_states({state({})})

    elif isinstance(item, Falsum):
        # based on (v)
        return set_of_states({})

    elif isinstance(item, LogicPredicate):
        # based on (vi)
        return set_of_states({state({_parse_predicate(item, maps)})})

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
    maps: Maps,
) -> View:
    if isinstance(view_item, Implies):
        supposition = view_item.left
        stage = view_item.right
    else:
        supposition = Truth()
        stage = view_item
    parsed_supposition = _parse_item(supposition, maps)
    parsed_stage = _parse_item(stage, maps)
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


@overload
def gather_item(item: Item, object_type: type[LogicPredicate]) -> list[LogicPredicate]:
    ...


@overload
def gather_item(item: Item, object_type: type[LogicFunction]) -> list[LogicFunction]:
    ...


@overload
def gather_item(item: Item, object_type: type[Constant]) -> list[Constant]:
    ...


def gather_item(
    item: Item, object_type: type[LogicPredicate] | type[LogicFunction] | type[Constant]
) -> list[LogicPredicate] | list[LogicFunction] | list[Constant]:
    out = []

    if isinstance(item, object_type):
        out.append(item)

    if isinstance(item, LogicPredicate) or isinstance(item, LogicFunction):
        for arg in item.args:
            out += gather_item(arg, object_type)
    elif isinstance(item, BoolAnd) or isinstance(item, BoolOr):
        for operand in item.operands:
            out += gather_item(operand, object_type)
    elif isinstance(item, BoolNot) or isinstance(item, LogicEmphasis):
        out += gather_item(item.arg, object_type)
    elif isinstance(item, Implies):
        out += gather_item(item.left, object_type) + gather_item(
            item.right, object_type
        )
    else:
        pass
    return out


def build_maps(
    item: Item,
) -> tuple[dict[str, Predicate], dict[str, Function], dict[str, Function]]:
    logic_predicates = gather_item(item, LogicPredicate)
    logic_functions = gather_item(item, LogicFunction)
    constants = gather_item(item, Constant)

    predicate_map: dict[str, Predicate] = {}
    for predicate in logic_predicates:
        if predicate.name not in predicate_map:
            predicate_map[predicate.name] = Predicate(
                name=predicate.name, arity=len(predicate.args)
            )
        else:
            exising_predicate = predicate_map[predicate.name]
            if exising_predicate.arity != len(predicate.args):
                raise ValueError(
                    f"Parsing predicate {predicate} has different arity than existing {predicate_map[predicate.name]}"
                )

    function_map: dict[str, Function] = {}
    for function in logic_functions:
        if function.name not in function_map:
            function_map[function.name] = Function(
                name=function.name, arity=len(function.args)
            )
        else:
            exising_function = function_map[function.name]
            if exising_function.arity != len(function.args):
                raise ValueError(
                    f"Parsing function {function} has different arity than existing {function_map[function.name]}"
                )

    constant_map: dict[str, Function] = {}
    for constant in constants:
        if constant.name not in constant_map:
            constant_map[constant.name] = Function(name=constant.name, arity=0)
    return predicate_map, function_map, constant_map


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
    predicate_map, function_map, constant_map = build_maps(view_item)
    maps = Maps(variable_map, predicate_map, function_map, constant_map)
    return _parse_view(view_item, dependency_relation, maps)
