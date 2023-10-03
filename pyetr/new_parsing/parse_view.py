from typing import cast

from pyetr.atoms import Atom, OpenAtom, OpenPredicateAtom, Predicate, PredicateAtom
from pyetr.atoms.terms import (
    ArbitraryObject,
    Function,
    FunctionalTerm,
    Multiset,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    Term,
)
from pyetr.common_parsing import (
    Variable,
    get_variable_map_and_dependencies,
    merge_terms_with_opens,
)
from pyetr.issues import IssueStructure
from pyetr.stateset import SetOfStates, State
from pyetr.view import View
from pyetr.weight import Weight, Weights

from . import parse_string as parsing


def parse_term(
    t: parsing.Term,
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[Term, list[tuple[Term, OpenTerm]]]:
    if isinstance(t, Variable):
        return variable_map[t.name], []
    elif isinstance(t, parsing.Emphasis):
        parsed_term, open_terms = parse_term(
            t.arg, variable_map=variable_map, function_map=function_map
        )
        return parsed_term, [*open_terms, (parsed_term, QuestionMark())]
    elif isinstance(t, parsing.Function):
        # These represent a list in term order, where each element is a list of derived open atom pairs
        if t.name not in function_map:
            raise ValueError(f"Term: {t} not found in function map")
        f = function_map[t.name]

        terms: list[Term] = []
        open_term_sets: list[list[tuple[Term, OpenTerm]]] = []
        for arg in t.args:
            term, open_terms = parse_term(
                arg, variable_map=variable_map, function_map=function_map
            )
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
        raise ValueError(f"Invalid term {t}")


def parse_atom(
    atom: parsing.Atom,
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[PredicateAtom, list[tuple[Term, OpenPredicateAtom]]]:
    terms: list[Term] = []
    open_term_sets: list[list[tuple[Term, OpenTerm]]] = []
    for item in atom.terms:
        term, open_terms = parse_term(
            item, variable_map=variable_map, function_map=function_map
        )
        terms.append(term)
        open_term_sets.append(open_terms)

    new_open_terms_sets = merge_terms_with_opens(terms, open_term_sets)

    predicate = Predicate(
        name=atom.predicate_name, arity=len(atom.terms), _verifier=atom.verifier
    )
    open_atoms = [
        (t, OpenPredicateAtom(predicate=predicate, terms=tuple(open_terms)))
        for t, open_terms in new_open_terms_sets
    ]
    return PredicateAtom(predicate=predicate, terms=tuple(terms)), open_atoms


def parse_state(
    s: parsing.State,
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[State, list[tuple[Term, OpenAtom]]]:
    issues: list[tuple[Term, OpenAtom]] = []
    new_atoms: list[Atom] = []
    for atom in s.atoms:
        if isinstance(atom, parsing.Atom):
            parsed_atom, new_issues = parse_atom(
                atom, variable_map=variable_map, function_map=function_map
            )
            new_atoms.append(parsed_atom)
            issues += new_issues
        else:
            raise NotImplementedError
    return State(new_atoms), issues


def parse_weighted_states(
    w_states: list[parsing.WeightedState],
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[dict[State, Weight], list[tuple[Term, OpenAtom]]]:
    weights: dict[State, Weight] = {}
    issues: list[tuple[Term, OpenAtom]] = []
    for state in w_states:
        parsed_state, new_issues = parse_state(
            state.state, variable_map=variable_map, function_map=function_map
        )
        issues += new_issues
        if state.additive is not None:
            parsed_terms = [
                parse_term(i, variable_map=variable_map, function_map=function_map)
                for i in state.additive.multiset
            ]
            additive = Multiset([i for i, _ in parsed_terms])
        else:
            additive = Multiset([])

        if state.multiplicative is not None:
            parsed_terms = [
                parse_term(i, variable_map=variable_map, function_map=function_map)
                for i in state.multiplicative.multiset
            ]
            multiplicative = Multiset([i for i, _ in parsed_terms])
        else:
            multiplicative = Multiset([])
        weight = Weight(multiplicative=multiplicative, additive=additive)
        weights[parsed_state] = weight
    return weights, issues


def get_function_map():
    raise NotImplementedError


def parse_pv(pv: parsing.ParserView) -> View:
    variable_map, dep_rel = get_variable_map_and_dependencies(pv.quantifiers)
    function_map = get_function_map()
    w_stage, issues = parse_weighted_states(
        pv.stage.states, variable_map=variable_map, function_map=function_map
    )
    issues: list[tuple[Term, OpenAtom]] = []
    if pv.supposition is not None:
        supp_states: list[State] = []
        for s in pv.supposition.states:
            parsed_state, new_issues = parse_state(
                s, variable_map=variable_map, function_map=function_map
            )
            supp_states.append(parsed_state)
            issues += new_issues
        supp = SetOfStates(supp_states)
    else:
        supp = SetOfStates([State([])])
    stage = SetOfStates(w_stage.keys())
    weights = Weights(w_stage)
    return View(
        stage=stage,
        supposition=supp,
        dependency_relation=dep_rel,
        issue_structure=IssueStructure(issues),
        weights=weights,
    )
