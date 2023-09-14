from copy import copy
from dataclasses import dataclass
from typing import Literal, TypeVar, cast

from pyetr.abstract_atom import Predicate
from pyetr.add_new_emphasis import add_new_emphasis
from pyetr.atom import Atom
from pyetr.dependency import Dependency, DependencyRelation, dependencies_from_sets
from pyetr.issues import IssueStructure
from pyetr.open_atom import OpenAtom
from pyetr.open_term import (
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    get_open_equivalent,
)
from pyetr.stateset import SetOfStates, State
from pyetr.term import ArbitraryObject, Function, FunctionalTerm, Summation, Term
from pyetr.view import View

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


def merge_terms_with_opens(
    terms: list[Term], open_term_sets: list[list[tuple[Term, OpenTerm]]]
) -> list[tuple[Term, list[OpenTerm]]]:
    new_terms = [get_open_equivalent(t) for t in terms]
    new_terms_sets: list[tuple[Term, list[OpenTerm]]] = []
    for i, open_terms in enumerate(open_term_sets):
        if len(open_terms) > 0:
            for t, open_term in open_terms:
                fresh_terms = copy(new_terms)
                fresh_terms[i] = open_term
                new_terms_sets.append((t, fresh_terms))
    return new_terms_sets


T = TypeVar("T")


def _parse_predicate(
    predicate: LogicPredicate, maps: Maps
) -> tuple[Atom, list[tuple[Term, OpenAtom]]]:
    def _parse_term(item: Item) -> tuple[Term, list[tuple[Term, OpenTerm]]]:
        if isinstance(item, Variable):
            return maps.variable_map[item.name], []
        elif isinstance(item, LogicEmphasis):
            parsed_term, open_terms = _parse_term(item.arg)
            return parsed_term, [*open_terms, (parsed_term, QuestionMark())]
        elif isinstance(item, LogicPredicate):
            if item.name in maps.constant_map:
                return FunctionalTerm(maps.constant_map[item.name], t=()), []
            elif item.name in maps.function_map:
                terms: list[Term] = []
                # These represent a list in term order, where each element is a list of derived open atom pairs
                open_term_sets: list[list[tuple[Term, OpenTerm]]] = []
                for arg in item.args:
                    term, open_terms = _parse_term(arg)
                    terms.append(term)
                    open_term_sets.append(open_terms)
                new_open_terms_sets = merge_terms_with_opens(terms, open_term_sets)
                f = maps.function_map[item.name]
                functional_opens = [
                    (t, OpenFunctionalTerm(f=f, t=tuple(open_terms)))
                    for t, open_terms in new_open_terms_sets
                ]
                return FunctionalTerm(f, tuple(terms)), cast(
                    list[tuple[Term, OpenTerm]], functional_opens
                )
            else:
                raise ValueError(f"Item: {item} not found in constant or function maps")
        else:
            raise ValueError(f"Invalid item {item}")

    terms: list[Term] = []
    open_term_sets: list[list[tuple[Term, OpenTerm]]] = []
    for item in predicate.args:
        term, open_terms = _parse_term(item)
        terms.append(term)
        open_term_sets.append(open_terms)
    new_open_terms_sets = merge_terms_with_opens(terms, open_term_sets)
    if predicate.name not in maps.predicate_map:
        raise ValueError(f"{predicate} not found in predicate map")
    f_predicate = maps.predicate_map[predicate.name]
    open_atoms = [
        (t, OpenAtom(predicate=f_predicate, terms=tuple(open_terms)))
        for t, open_terms in new_open_terms_sets
    ]
    return Atom(predicate=f_predicate, terms=tuple(terms)), open_atoms


def _parse_item_with_issue(
    item: Item, maps: Maps
) -> tuple[SetOfStates, list[tuple[Term, OpenAtom]]]:
    def _parse_item(
        item: Item, maps: Maps, open_atoms: list[tuple[Term, OpenAtom]]
    ) -> SetOfStates:
        # Based on definition 4.16
        if isinstance(item, BoolOr):
            # based on (i)
            new_set = SetOfStates(set())
            for operand in item.operands:
                parsed_item: SetOfStates = _parse_item(operand, maps, open_atoms)
                new_set |= parsed_item
            return new_set

        elif isinstance(item, BoolAnd):
            # based on (ii)
            new_set = SetOfStates({State(set())})
            for operand in item.operands:
                parsed_item: SetOfStates = _parse_item(operand, maps, open_atoms)
                new_set *= parsed_item
            return new_set

        elif isinstance(item, BoolNot):
            # based on (iii)
            new_arg = _parse_item(item.arg, maps, open_atoms)
            for i, (t, o) in enumerate(open_atoms):
                new_atom = o(t)
                if new_atom in new_arg.atoms:
                    open_atoms[i] = (t, ~o)
            return new_arg.negation()
        elif isinstance(item, Truth):
            # based on (iv)
            return SetOfStates({State({})})

        elif isinstance(item, Falsum):
            # based on (v)
            return SetOfStates({})

        elif isinstance(item, LogicPredicate):
            # based on (vi)
            atom, o_atoms = _parse_predicate(item, maps)
            for o_atom in o_atoms:
                open_atoms.append(o_atom)
            return SetOfStates({State({atom})})

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

    open_atoms: list[tuple[Term, OpenAtom]] = []
    return _parse_item(item, maps, open_atoms), open_atoms


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
    parsed_supposition, open_atoms_supp = _parse_item_with_issue(supposition, maps)
    parsed_stage, open_atoms_stage = _parse_item_with_issue(stage, maps)
    issue_structure = IssueStructure(open_atoms_supp + open_atoms_stage)
    # if (
    #     parsed_stage.emphasis_count + parsed_supposition.emphasis_count == 0
    #     and add_emphasis
    # ):
    #     parsed_stage, parsed_supposition = add_new_emphasis(
    #         parsed_stage, parsed_supposition, dependency_relation
    #     )
    return View(
        stage=parsed_stage,
        supposition=parsed_supposition,
        dependency_relation=dependency_relation,
        issue_structure=issue_structure,
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
