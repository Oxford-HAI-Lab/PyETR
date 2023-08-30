from dataclasses import dataclass
from typing import Literal, cast

from pyetr.add_new_emphasis import add_new_emphasis
from pyetr.dependency import Dependency, DependencyRelation, dependencies_from_sets
from pyetr.stateset import SetOfStates, State
from pyetr.term import ArbitraryObject, Emphasis, Function, Term
from pyetr.view import View

from ..atom import Atom, Predicate
from .parse_string import (
    AtomicItem,
    BoolAnd,
    BoolNot,
    BoolOr,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
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
        elif isinstance(item, LogicEmphasis):
            inner = _parse_term(item.arg)
            if isinstance(inner, Emphasis):
                raise ValueError(f"Second emphasis found in {inner}")
            return Emphasis(inner)
        elif isinstance(item, LogicPredicate):
            if item.name in maps.constant_map:
                return Term(maps.constant_map[item.name])
            elif item.name in maps.function_map:
                terms: list[Term | ArbitraryObject | Emphasis] = [
                    _parse_term(item) for item in item.args
                ]
                if len(terms) == 0:
                    new_terms = None
                else:
                    new_terms = tuple(terms)
                return Term(maps.function_map[item.name], new_terms)
            else:
                raise ValueError(f"Item: {item} not found in constant or function maps")
        else:
            raise ValueError(f"Invalid item {item}")

    terms: list[Term | ArbitraryObject | Emphasis] = [
        _parse_term(item) for item in predicate.args
    ]
    if predicate.name not in maps.predicate_map:
        raise ValueError(f"{predicate} not found in predicate map")
    return maps.predicate_map[predicate.name](tuple(terms))


def _parse_item(item: Item, maps: Maps) -> SetOfStates:
    # Based on definition 4.16
    if isinstance(item, BoolOr):
        # based on (i)
        new_set = SetOfStates(set())
        for operand in item.operands:
            parsed_item: SetOfStates = _parse_item(operand, maps)
            new_set |= parsed_item
        return new_set

    elif isinstance(item, BoolAnd):
        # based on (ii)
        new_set = SetOfStates({State(set())})
        for operand in item.operands:
            parsed_item: SetOfStates = _parse_item(operand, maps)
            new_set *= parsed_item
        return new_set

    elif isinstance(item, BoolNot):
        # based on (iii)
        new_arg = _parse_item(item.arg, maps)
        return new_arg.negation()
    elif isinstance(item, Truth):
        # based on (iv)
        return SetOfStates({State({})})

    elif isinstance(item, Falsum):
        # based on (v)
        return SetOfStates({})

    elif isinstance(item, LogicPredicate):
        # based on (vi)
        return SetOfStates({State({_parse_predicate(item, maps)})})

    elif isinstance(item, LogicEmphasis):
        raise ValueError(f"Logic emphasis {item} found outside of logic predicate")

    elif isinstance(item, Variable):
        raise ValueError(f"Variable {item} found outside of logic predicate")

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
    add_emphasis: bool,
) -> View:
    if isinstance(view_item, Implies):
        supposition = view_item.left
        stage = view_item.right
    else:
        supposition = Truth()
        stage = view_item
    parsed_supposition = _parse_item(supposition, maps)
    parsed_stage = _parse_item(stage, maps)
    if (
        parsed_stage.emphasis_count + parsed_supposition.emphasis_count == 0
        and add_emphasis
    ):
        parsed_stage, parsed_supposition = add_new_emphasis(
            parsed_stage, parsed_supposition, dependency_relation
        )
    return View.from_integrated_emp(
        stage=parsed_stage,
        supposition=parsed_supposition,
        dependency_relation=dependency_relation,
    )


Universal = ArbitraryObject
Existential = ArbitraryObject


def get_variable_map_and_dependencies(
    quantifieds: list[Quantified],
) -> tuple[dict[str, ArbitraryObject], DependencyRelation]:
    variable_map: dict[str, ArbitraryObject] = {}
    encountered_universals: list[tuple[Universal, set[Existential]]] = []
    existentials: set[Existential] = set()
    universals: set[Universal] = set()
    for quantified in quantifieds:
        if quantified.quantifier == "∃":
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            existentials.add(arb_obj)
            for _, exi_set in encountered_universals:
                exi_set.add(arb_obj)
        else:
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            universals.add(arb_obj)
            encountered_universals.append((arb_obj, set()))

        if quantified.variable.name not in variable_map:
            variable_map[quantified.variable.name] = arb_obj
        else:
            raise ValueError(
                f"Variable {quantified.variable.name} appears twice in quantifiers"
            )

    return variable_map, DependencyRelation(
        universals=universals,
        existentials=existentials,
        dependencies=dependencies_from_sets(encountered_universals),
    )


def gather_atomic_item(
    item: AtomicItem, object_type: Literal["Function"] | Literal["Constant"]
) -> list[LogicPredicate]:
    out = []

    if (
        object_type == "Constant"
        and isinstance(item, LogicPredicate)
        and len(item.args) == 0
    ):
        out.append(item)
    elif (
        object_type == "Function"
        and isinstance(item, LogicPredicate)
        and len(item.args) >= 0
    ):
        out.append(item)

    if isinstance(item, LogicPredicate):
        for arg in item.args:
            out += gather_atomic_item(cast(AtomicItem, arg), object_type)
    elif isinstance(item, BoolNot) or isinstance(item, LogicEmphasis):
        out += gather_atomic_item(cast(AtomicItem, item.arg), object_type)
    else:
        pass
    return out


def gather_item(
    item: Item,
    object_type: Literal["Predicate"] | Literal["Function"] | Literal["Constant"],
) -> list[LogicPredicate]:
    out = []

    if object_type == "Predicate" and isinstance(item, LogicPredicate):
        out.append(item)

    if isinstance(item, LogicPredicate) and not object_type == "Predicate":
        for arg in item.args:
            out += gather_atomic_item(cast(AtomicItem, arg), object_type)
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
    logic_predicates = gather_item(item, "Predicate")
    logic_functions = gather_item(item, "Function")
    constants = gather_item(item, "Constant")

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


def parse_items(expr: list[Item], add_emphasis: bool) -> View:
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

    variable_map, dep_relation = get_variable_map_and_dependencies(quantifieds)
    predicate_map, function_map, constant_map = build_maps(view_item)
    maps = Maps(variable_map, predicate_map, function_map, constant_map)
    return _parse_view(view_item, dep_relation, maps, add_emphasis)
