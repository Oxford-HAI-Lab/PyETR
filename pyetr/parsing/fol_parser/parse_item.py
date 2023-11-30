from dataclasses import dataclass
from typing import Literal, TypeVar, cast

from pyetr.atoms import OpenPredicateAtom, Predicate, PredicateAtom
from pyetr.atoms.terms import (
    ArbitraryObject,
    Function,
    FunctionalTerm,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    Term,
)
from pyetr.dependency import DependencyRelation
from pyetr.issues import IssueStructure
from pyetr.parsing.common import (
    ParsingError,
    get_variable_map_and_dependencies,
    merge_terms_with_opens,
)
from pyetr.stateset import SetOfStates, State
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
    """
    A store for all the maps, which go from name of object
    to object
    """

    variable_map: dict[str, ArbitraryObject]
    predicate_map: dict[str, Predicate]
    function_map: dict[str, Function]
    constant_map: dict[str, Function]


T = TypeVar("T")


def _parse_predicate(
    predicate: LogicPredicate, maps: Maps
) -> tuple[PredicateAtom, list[tuple[Term, OpenPredicateAtom]]]:
    """
    Parse a logic predicate to a predicate atom

    Args:
        predicate (LogicPredicate): The predicate to convert
        maps (Maps): The maps of object name to object.

    Returns:
        tuple[PredicateAtom, list[tuple[Term, OpenPredicateAtom]]]: The predicate atom,
            and a list of its associated open atoms.
    """

    def _parse_term(item: Item) -> tuple[Term, list[tuple[Term, OpenTerm]]]:
        if isinstance(item, Variable):
            if item.name not in maps.variable_map:
                raise ParsingError(
                    f"Arbitrary object {item.name} not found in quantifiers"
                )
            return maps.variable_map[item.name], []
        elif isinstance(item, LogicEmphasis):
            parsed_term, open_terms = _parse_term(item.arg)
            return parsed_term, [*open_terms, (parsed_term, QuestionMark())]
        elif isinstance(item, LogicPredicate):
            if item.name in maps.constant_map:
                return FunctionalTerm(maps.constant_map[item.name], t=()), []
            elif item.name in maps.function_map:
                # These represent a list in term order, where each element is a list of derived open atom pairs
                f = maps.function_map[item.name]

                terms: list[Term] = []
                open_term_sets: list[list[tuple[Term, OpenTerm]]] = []
                for arg in item.args:
                    term, open_terms = _parse_term(arg)
                    terms.append(term)
                    open_term_sets.append(open_terms)
                new_open_terms_sets = merge_terms_with_opens(terms, open_term_sets)

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
        (t, OpenPredicateAtom(predicate=f_predicate, terms=tuple(open_terms)))
        for t, open_terms in new_open_terms_sets
    ]
    return PredicateAtom(predicate=f_predicate, terms=tuple(terms)), open_atoms


def _parse_item_with_issue(
    item: Item, maps: Maps
) -> tuple[SetOfStates, list[tuple[Term, OpenPredicateAtom]]]:
    """
    Parses the items with the issues built in.

    Args:
        item (Item): Parsed Item
        maps (Maps): The maps of object name to object.

    Returns:
        tuple[SetOfStates, list[tuple[Term, OpenPredicateAtom]]]: The resultant set of states,
            and a list of the issues associated.
    """

    def _parse_item(
        item: Item, maps: Maps, open_atoms: list[tuple[Term, OpenPredicateAtom]]
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

        elif isinstance(item, LogicEmphasis):  # pragma: not covered
            raise ParsingError(
                f"Logic emphasis {item} found outside of logic predicate"
            )

        elif isinstance(item, Variable):  # pragma: not covered
            raise ParsingError(f"Variable {item} found outside of logic predicate")

        elif isinstance(item, Implies):  # pragma: not covered
            raise ParsingError(
                f"Implies statement {item} found at lower level than top"
            )

        else:  # pragma: not covered
            assert isinstance(item, Quantified)
            raise ParsingError(f"Quantified {item} found at lower level than top")

    open_atoms: list[tuple[Term, OpenPredicateAtom]] = []
    return _parse_item(item, maps, open_atoms), open_atoms


def _parse_view(
    view_item: Item,
    dependency_relation: DependencyRelation,
    maps: Maps,
) -> View:
    """
    Parses the view item and dep rel, with the maps

    Args:
        view_item (Item): The item representing the view
        dependency_relation (DependencyRelation): The dependency relation fully formed
        maps (Maps): The maps of object name to object.

    Returns:
        View: the parsed view
    """
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
        weights=None,
    )


Universal = ArbitraryObject
Existential = ArbitraryObject


def gather_atomic_item(
    item: AtomicItem, object_type: Literal["Function"] | Literal["Constant"]
) -> list[LogicPredicate]:
    """
    Gathers the items of a given object type found in an atom.

    Args:
        item (AtomicItem): The atomic item
        object_type (Literal["Function"] | Literal["Constant"]): The type of object being gathered

    Returns:
        list[LogicPredicate]: The list of items that match the object type
    """
    out: list[LogicPredicate] = []

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
    """
    Gathers the items of a given object type found in an atom.

    Args:
        item (Item): The item
        object_type (Literal["Predicate"] | Literal["Function"] | Literal["Constant"]): The type
            of object being gathered

    Returns:
        list[LogicPredicate]: The list of items that match the object type
    """
    out: list[LogicPredicate] = []

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
    view_item: Item, custom_functions: list[Function]
) -> tuple[dict[str, Predicate], dict[str, Function], dict[str, Function]]:
    """
    Builds the predicate, function and constant maps.

    Args:
        view_item (Item): The item containing the whole view.
        custom_functions (list[Function]): A list of custom functions to use in the view.

    Returns:
        tuple[dict[str, Predicate], dict[str, Function], dict[str, Function]]: The various
            maps in tuple form.
    """
    logic_predicates = gather_item(view_item, "Predicate")
    logic_functions = gather_item(view_item, "Function")
    constants = gather_item(view_item, "Constant")

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

    function_map: dict[str, Function] = {f.name: f for f in custom_functions}
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


def parse_items(expr: list[Item], custom_functions: list[Function]) -> View:
    """
    Converts the items parsed from the string to a view.

    Args:
        expr (list[Item]): The list of items from the string.
        custom_functions (list[Function]): A list of custom functions to use in the view.

    Returns:
        View: The parsed view.
    """
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
    predicate_map, function_map, constant_map = build_maps(view_item, custom_functions)
    maps = Maps(variable_map, predicate_map, function_map, constant_map)
    return _parse_view(view_item, dep_relation, maps)
