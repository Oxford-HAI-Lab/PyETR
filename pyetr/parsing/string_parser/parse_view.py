from typing import Optional, cast

import pyetr.parsing.string_parser.parse_string as parsing
from pyetr.atoms import Atom, OpenAtom, OpenPredicateAtom, Predicate, PredicateAtom
from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_doatom import OpenDoAtom
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
from pyetr.atoms.terms.function import RealNumber
from pyetr.atoms.terms.special_funcs import Summation, XBar
from pyetr.issues import IssueStructure
from pyetr.parsing.common import (
    Variable,
    get_variable_map_and_dependencies,
    merge_atoms_with_opens,
    merge_terms_with_opens,
)
from pyetr.stateset import SetOfStates, State
from pyetr.view import View
from pyetr.weight import Weight, Weights


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
    elif isinstance(t, parsing.Real):
        return FunctionalTerm(RealNumber(t.num), ()), []
    elif isinstance(t, parsing.Xbar):
        new_left, new_issues1 = parse_term(
            t.left, variable_map=variable_map, function_map=function_map
        )
        new_right, new_issues2 = parse_term(
            t.right, variable_map=variable_map, function_map=function_map
        )
        return FunctionalTerm(XBar, (new_left, new_right)), new_issues1 + new_issues2
    elif isinstance(t, parsing.Summation):
        issues: list[tuple[Term, OpenTerm]] = []
        new_args: list[Term] = []
        for arg in t.args:
            new_arg, new_issues = parse_term(
                arg, variable_map=variable_map, function_map=function_map
            )
            new_args.append(new_arg)
            issues += new_issues
        return FunctionalTerm(Summation, Multiset(new_args)), issues
    else:
        raise ValueError(f"Invalid term {t}")


def parse_predicate_atom(
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


def parse_do_atom(
    atom: parsing.DoAtom,
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[DoAtom, list[tuple[Term, OpenDoAtom]]]:
    atoms: list[PredicateAtom] = []
    open_atom_sets: list[list[tuple[Term, OpenPredicateAtom]]] = []
    for a in atom.atoms:
        parsed_a, open_atoms = parse_predicate_atom(
            a, variable_map=variable_map, function_map=function_map
        )
        atoms.append(parsed_a)
        open_atom_sets.append(open_atoms)

    new_open_terms_sets = merge_atoms_with_opens(atoms, open_atom_sets)

    open_do_atoms = [
        (t, OpenDoAtom(atoms=set(open_atoms), polarity=atom.polarity))
        for t, open_atoms in new_open_terms_sets
    ]

    return DoAtom(polarity=atom.polarity, atoms=set(atoms)), open_do_atoms


def parse_state(
    s: parsing.State,
    variable_map: dict[str, ArbitraryObject],
    function_map: dict[str, Function],
) -> tuple[State, list[tuple[Term, OpenAtom]]]:
    issues: list[tuple[Term, OpenAtom]] = []
    new_atoms: list[Atom] = []
    for atom in s.atoms:
        if isinstance(atom, parsing.Atom):
            parsed_atom, new_issues = parse_predicate_atom(
                atom, variable_map=variable_map, function_map=function_map
            )
        else:
            parsed_atom, new_issues = parse_do_atom(
                atom, variable_map=variable_map, function_map=function_map
            )
        new_atoms.append(parsed_atom)
        issues += new_issues
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


def gather_funcs(term: parsing.Term) -> list[Function]:
    funcs: list[Function] = []
    if isinstance(term, parsing.Real):
        funcs.append(RealNumber(term.num))
    elif isinstance(term, parsing.Xbar):
        funcs += gather_funcs(term.left)
        funcs += gather_funcs(term.right)
        funcs.append(XBar)
    elif isinstance(term, parsing.Emphasis):
        funcs += gather_funcs(term.arg)
    elif isinstance(term, parsing.Summation):
        for arg in term.args:
            funcs += gather_funcs(arg)
        funcs.append(Summation)
    elif isinstance(term, parsing.Function):
        for arg in term.args:
            funcs += gather_funcs(arg)
        funcs.append(Function(term.name, arity=len(term.args)))
    elif isinstance(term, Variable):
        pass
    else:
        raise TypeError(f"term type {term} not recognised")
    return list(set(funcs))


def get_function_map(
    stage: parsing.Stage,
    supposition: Optional[parsing.Supposition],
    custom_functions: list[Function],
) -> dict[str, Function]:
    terms_to_scan: list[parsing.Term] = []
    for state in stage.states:
        if state.additive is not None:
            terms_to_scan += state.additive.multiset
        if state.multiplicative is not None:
            terms_to_scan += state.multiplicative.multiset
        for atom in state.state.atoms:
            if isinstance(atom, parsing.Atom):
                terms_to_scan += atom.terms
            else:
                for a in atom.atoms:
                    terms_to_scan += a.terms

    if supposition is not None:
        for state in supposition.states:
            for atom in state.atoms:
                if isinstance(atom, parsing.Atom):
                    terms_to_scan += atom.terms
                else:
                    for a in atom.atoms:
                        terms_to_scan += a.terms

    func_map: dict[str, Function] = {f.name: f for f in custom_functions}
    new_funcs: list[Function] = []
    for term in terms_to_scan:
        new_funcs += gather_funcs(term)

    for new_func in new_funcs:
        if new_func.name not in func_map:
            func_map[new_func.name] = new_func
    return func_map


def parse_pv(pv: parsing.ParserView, custom_functions: list[Function]) -> View:
    variable_map, dep_rel = get_variable_map_and_dependencies(pv.quantifiers)
    function_map = get_function_map(pv.stage, pv.supposition, custom_functions)
    w_stage, issues = parse_weighted_states(
        pv.stage.states, variable_map=variable_map, function_map=function_map
    )
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
