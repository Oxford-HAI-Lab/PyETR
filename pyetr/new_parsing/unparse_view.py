from typing import Optional, cast

import pyetr.new_parsing.parse_string as parsing
from pyetr.atoms import Atom, DoAtom, OpenDoAtom, OpenPredicateAtom, PredicateAtom
from pyetr.atoms.terms import (
    ArbitraryObject,
    FunctionalTerm,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    RealNumber,
    Summation,
    Term,
    XBar,
)
from pyetr.atoms.terms.open_term import OpenMultiset
from pyetr.atoms.terms.term import Multiset
from pyetr.common_parsing import Variable, get_quantifiers
from pyetr.issues import IssueStructure
from pyetr.stateset import State, Supposition
from pyetr.view import View
from pyetr.weight import Weight, Weights


def unparse_multiset(
    multiset: Multiset, open_multisets: Optional[list[tuple[Term, OpenMultiset]]] = None
) -> list[parsing.Term | Variable]:
    if open_multisets is None:
        new_subterms: list[parsing.Term | Variable] = []
        for i, subterm in enumerate(multiset):
            new_subterms.append(unparse_term(subterm, []))
        return new_subterms
    else:
        new_subterms: list[parsing.Term | Variable] = []
        for i, subterm in enumerate(multiset):
            rel_open_terms: list[tuple[Term, OpenTerm]] = []
            for t, o in open_multisets:
                rel_open_terms.append((t, o._items[i]))
            new_subterms.append(unparse_term(subterm, rel_open_terms))
        return new_subterms


def unparse_term(
    term: Term, open_terms: list[tuple[Term, OpenTerm]]
) -> parsing.Term | Variable:
    if any([isinstance(o, QuestionMark) for _, o in open_terms]):
        remaining_terms = [
            (t, o) for t, o in open_terms if not isinstance(o, QuestionMark)
        ]
        return parsing.Emphasis([[unparse_term(term, remaining_terms)]])
    if isinstance(term, FunctionalTerm):
        # Insert term back in - if it matches, it's a term to pass
        if len(term.t) == 1 and isinstance(term.t[0], Multiset):
            multi = term.t[0]
            open_multis: list[tuple[Term, OpenMultiset]] = []
            for t, open_term in open_terms:
                if isinstance(open_term, OpenMultiset):
                    open_multis.append((t, open_term))
            new_subterms = unparse_multiset(multiset=multi, open_multisets=open_multis)
        else:
            new_subterms: list[parsing.Term | Variable] = []
            for i, subterm in enumerate(term.t):
                rel_open_terms: list[tuple[Term, OpenTerm]] = []
                for t, o in open_terms:
                    assert isinstance(o, OpenFunctionalTerm)
                    rel_open_terms.append((t, o.t[i]))
                new_subterms.append(unparse_term(subterm, rel_open_terms))

        if isinstance(term.f, RealNumber):
            return parsing.Real([term.f.num])
        elif term.f == XBar:
            return parsing.Xbar([list(new_subterms)])
        elif term.f == Summation:
            return parsing.Summation([[term.f.name, parsing.Comma([new_subterms])]])
        else:
            return parsing.Function([term.f.name, parsing.Comma([new_subterms])])

    elif isinstance(term, ArbitraryObject):
        return Variable([term.name])
    elif isinstance(term, Multiset):
        assert False
    else:
        raise ValueError(f"Invalid term {term} provided")


def unparse_predicate_atom(
    predicate_atom: PredicateAtom, open_atoms: list[tuple[Term, OpenPredicateAtom]]
) -> parsing.Atom:
    new_terms: list[parsing.Term | Variable] = []
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
        items.append(parsing.AdditiveWeight(unparse_multiset(weight.additive)))
    if len(weight.multiplicative) > 0:
        items.append(
            parsing.MultiplicativeWeight(unparse_multiset(weight.multiplicative))
        )
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
