from __future__ import annotations

import typing
from typing import cast

import pyetr.parsing.string_parser.parse_string as parsing
from pyetr.atoms import Atom, DoAtom, OpenPredicateAtom, PredicateAtom
from pyetr.atoms.open_predicate_atom import get_open_atom_equivalent
from pyetr.atoms.terms import (
    ArbitraryObject,
    FunctionalTerm,
    Multiset,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    RealNumber,
    Summation,
    Term,
    XBar,
)
from pyetr.issues import IssueStructure
from pyetr.parsing.common import Variable, get_quantifiers
from pyetr.stateset import State, Supposition

if typing.TYPE_CHECKING:
    from pyetr.view import View

from pyetr.weight import Weight, Weights


def unparse_term(
    term: Term, open_terms: list[tuple[Term, OpenTerm]]
) -> parsing.Term | Variable:
    """
    Converts a term and associated open terms to a parsing term.

    Args:
        term (Term): A view term
        open_terms (list[tuple[Term, OpenTerm]]): The term's associated
            open terms.

    Returns:
        parsing.Term | Variable: The parsing term.
    """
    if any([isinstance(o, QuestionMark) for _, o in open_terms]):
        remaining_terms = [
            (t, o) for t, o in open_terms if not isinstance(o, QuestionMark)
        ]
        return parsing.Emphasis([[unparse_term(term, remaining_terms)]])
    if isinstance(term, FunctionalTerm):
        # Insert term back in - if it matches, it's a term to pass
        new_subterms: list[parsing.Term | Variable] = []
        for subterm in term.t:
            rel_open_terms: list[tuple[Term, OpenTerm]] = []
            for t, o in open_terms:
                assert isinstance(o, OpenFunctionalTerm)
                for o_subterm in o.t:
                    if subterm == o_subterm(t):
                        rel_open_terms.append((t, o_subterm))
            new_subterms.append(unparse_term(subterm, rel_open_terms))

        if isinstance(term.f, RealNumber):
            return parsing.Real([term.f.num])
        elif term.f == XBar:
            return parsing.Xbar([new_subterms])
        elif term.f == Summation:
            return parsing.Summation([term.f.name, *new_subterms])
        else:
            return parsing.Function([term.f.name, *new_subterms])

    elif isinstance(term, ArbitraryObject):
        return Variable([term.name])
    else:
        raise ValueError(f"Invalid term {term} provided")


def unparse_multiset(multiset: Multiset[Term]) -> list[parsing.Term | Variable]:
    """
    Converts a multiset of terms to a list of parsing terms.

    Args:
        multiset (Multiset[Term]): A multiset of terms

    Returns:
        list[parsing.Term | Variable]: A list of parsing terms
    """
    return [unparse_term(subterm, []) for subterm in multiset]


def unparse_predicate_atom(
    predicate_atom: PredicateAtom, open_atoms: list[tuple[Term, OpenPredicateAtom]]
) -> parsing.Atom:
    """
    Converts a predicate atom to parsing atom form.

    Args:
        predicate_atom (PredicateAtom): The atom to be parsed
        open_atoms (list[tuple[Term, OpenPredicateAtom]]): The associated open atoms.

    Returns:
        parsing.Atom: The atom in parsing form.
    """
    new_terms: list[parsing.Term | Variable] = [
        unparse_term(term, [(t, o.terms[i]) for t, o in open_atoms])
        for i, term in enumerate(predicate_atom.terms)
    ]
    items = [] if predicate_atom.predicate.verifier else ["~"]

    items.append(predicate_atom.predicate.name)
    return parsing.Atom(items + new_terms)


def unparse_do_atom(
    do_atom: DoAtom, open_atoms: list[tuple[Term, OpenPredicateAtom]]
) -> parsing.DoAtom:
    """
    Converts a do atom to parsing atom form.

    Args:
        do_atom (DoAtom): The do atom to convert
        open_do_atoms (list[tuple[Term, OpenPredicateAtom]]): The associated open
            do atoms.

    Returns:
        parsing.DoAtom: The parsing do atom.
    """

    def open_atom_corresponds(
        open_atom: OpenPredicateAtom, atom: PredicateAtom, term: Term
    ) -> bool:
        closed_atom = open_atom(term)
        if closed_atom == atom:
            basic_open_atom = get_open_atom_equivalent(closed_atom)
            return open_atom != basic_open_atom
        return False

    new_atoms: list[parsing.Atom] = []
    for atom in do_atom.atoms:
        # For each atom in the do atom
        assoc_open_atoms: list[tuple[Term, OpenPredicateAtom]] = []
        for t, o in open_atoms:
            # Check each of the open do atoms
            if open_atom_corresponds(o, atom, t):
                assoc_open_atoms.append((t, o))

        new_atom = unparse_predicate_atom(atom, assoc_open_atoms)
        new_atoms.append(new_atom)

    items = [] if do_atom.polarity else ["~"]

    return parsing.DoAtom(items + new_atoms)


def unparse_atom(
    atom: Atom, issue_structure: IssueStructure
) -> parsing.Atom | parsing.DoAtom:
    """
    Converts an atom to the parsing form.

    Args:
        atom (Atom): The atom to convert
        issue_structure (IssueStructure): The issue structure of the view.

    Returns:
        parsing.Atom | parsing.DoAtom: The atom in parsing form.
    """
    open_atoms = [
        (term, open_atom)
        for term, open_atom in issue_structure
        if (
            open_atom(term) == atom
            or (isinstance(atom, DoAtom) and (open_atom(term) in atom.atoms))
        )
    ]
    if isinstance(atom, PredicateAtom):
        return unparse_predicate_atom(
            atom, cast(list[tuple[Term, OpenPredicateAtom]], open_atoms)
        )
    elif isinstance(atom, DoAtom):
        return unparse_do_atom(atom, open_atoms)
    else:
        assert False


def unparse_state(state: State, issue_structure: IssueStructure) -> parsing.State:
    """
    Converts a state to parsing form.

    Args:
        state (State): The state to convert.
        issue_structure (IssueStructure): The issue structure of the view.

    Returns:
        parsing.State: The parsing form of the state.
    """
    return parsing.State([unparse_atom(atom, issue_structure) for atom in state])


def unparse_weighted_state(
    state: State, weight: Weight, issue_structure: IssueStructure
) -> parsing.WeightedState:
    """
    Converts a state and weight to weighted state parsing form.

    Args:
        state (State): The state to convert.
        weight (Weight): The weight to convert.
        issue_structure (IssueStructure): The issue structure of the view.

    Returns:
        parsing.WeightedState: The weighted state parsing form.
    """
    items: list[
        parsing.State | parsing.AdditiveWeight | parsing.MultiplicativeWeight
    ] = [unparse_state(state, issue_structure)]
    if len(weight.additive) > 0:
        items.append(parsing.AdditiveWeight(unparse_multiset(weight.additive)))
    if len(weight.multiplicative) > 0:
        items.append(
            parsing.MultiplicativeWeight(unparse_multiset(weight.multiplicative))
        )
    return parsing.WeightedState(items)


def unparse_stage(weights: Weights, issue_structure: IssueStructure) -> parsing.Stage:
    """
    Converts the stage in weights form to parsing form.

    Args:
        weights (Weights): The weighted stage.
        issue_structure (IssueStructure): The issue structure of the view.

    Returns:
        parsing.Stage: The stage in parsing form.
    """
    return parsing.Stage(
        [
            unparse_weighted_state(state, weight, issue_structure)
            for state, weight in weights.items()
        ]
    )


def unparse_supposition(
    supposition: Supposition, issue_structure: IssueStructure
) -> parsing.Supposition:
    """
    Converts the supposition to parsing form.

    Args:
        supposition (Supposition): The supposition of the view.
        issue_structure (IssueStructure): The issue structure for the view.

    Returns:
        parsing.Supposition: The supposition in parsing form.
    """
    return parsing.Supposition(
        [unparse_state(state, issue_structure=issue_structure) for state in supposition]
    )


def unparse_view(v: View) -> parsing.ParserView:
    """
    Convert the view to parsing form.

    Args:
        v (View): The input view.

    Returns:
        parsing.ParserView: The parsing form of the view.
    """
    quantifiers = get_quantifiers(
        dependency_relation=v.dependency_relation,
    )
    stage = unparse_stage(v.weights, v.issue_structure)
    if v.supposition.is_verum:
        supposition = None
    else:
        supposition = unparse_supposition(v.supposition, v.issue_structure)

    return parsing.ParserView(
        quantifiers=quantifiers, stage=stage, supposition=supposition
    )
