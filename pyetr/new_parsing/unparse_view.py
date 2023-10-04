from typing import cast

import pyetr.new_parsing.parse_string as parsing
from pyetr.atoms.abstract import Atom
from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_doatom import OpenDoAtom
from pyetr.atoms.open_predicate_atom import OpenPredicateAtom
from pyetr.atoms.predicate_atom import PredicateAtom
from pyetr.atoms.terms.open_term import OpenTerm
from pyetr.atoms.terms.term import Term
from pyetr.common_parsing import get_quantifiers
from pyetr.issues import IssueStructure
from pyetr.stateset import State, Supposition
from pyetr.view import View
from pyetr.weight import Weight, Weights


def unparse_term(term: Term, open_terms: list[tuple[Term, OpenTerm]]) -> parsing.Term:
    raise NotImplementedError


def unparse_predicate_atom(
    predicate_atom: PredicateAtom, open_atoms: list[tuple[Term, OpenPredicateAtom]]
) -> parsing.Atom:
    new_terms: list[parsing.Term] = []
    for i, term in enumerate(predicate_atom.terms):
        open_terms = [(t, o.terms[i]) for t, o in open_atoms]
        new_terms.append(unparse_term(term, open_terms))
    if predicate_atom.predicate.verifier:
        items = []
    else:
        items = ["~"]
    items.append(predicate_atom.predicate.name)
    return parsing.Atom(items + new_terms)


def unparse_do_atom(
    do_atom: DoAtom, open_do_atoms: list[tuple[Term, OpenDoAtom]]
) -> parsing.DoAtom:
    new_atoms: list[parsing.Atom] = []
    for i, atom in enumerate(do_atom.atoms):
        open_atoms = [(t, list(o.atoms)[i]) for t, o in open_do_atoms]
        new_atoms.append(unparse_predicate_atom(atom, open_atoms))
    if do_atom.polarity:
        items = []
    else:
        items = ["~"]

    return parsing.DoAtom(items + new_atoms)


def unparse_atom(
    atom: Atom, issue_structure: IssueStructure
) -> parsing.Atom | parsing.DoAtom:
    open_atoms = [
        (term, open_atom)
        for term, open_atom in issue_structure
        if (open_atom(term) == atom)
    ]
    if isinstance(atom, PredicateAtom):
        return unparse_predicate_atom(
            atom, cast(list[tuple[Term, OpenPredicateAtom]], open_atoms)
        )
    elif isinstance(atom, DoAtom):
        return unparse_do_atom(atom, cast(list[tuple[Term, OpenDoAtom]], open_atoms))
    else:
        assert False


def unparse_state(state: State, issue_structure: IssueStructure) -> parsing.State:
    return parsing.State([unparse_atom(atom, issue_structure) for atom in state])


def unparse_weighted_state(
    state: State, weight: Weight, issue_structure: IssueStructure
) -> parsing.WeightedState:
    items: list[
        parsing.State | parsing.AdditiveWeight | parsing.MultiplicativeWeight
    ] = [unparse_state(state, issue_structure)]
    if len(weight.additive) > 0:
        items.append(parsing.AdditiveWeight(weight.additive))
    if len(weight.multiplicative) > 0:
        items.append(parsing.MultiplicativeWeight(weight.additive))
    return parsing.WeightedState(items)


def unparse_stage(weights: Weights, issue_structure: IssueStructure) -> parsing.Stage:
    return parsing.Stage(
        [
            unparse_weighted_state(state, weight, issue_structure)
            for state, weight in weights.items()
        ]
    )


def unparse_supposition(
    supposition: Supposition, issue_structure: IssueStructure
) -> parsing.Supposition:
    return parsing.Supposition(
        [unparse_state(state, issue_structure=issue_structure) for state in supposition]
    )


def unparse_view(v: View) -> parsing.ParserView:
    quantifiers = get_quantifiers(
        arb_objects=v.stage.arb_objects
        | v.supposition.arb_objects
        | v.weights.arb_objects,
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
