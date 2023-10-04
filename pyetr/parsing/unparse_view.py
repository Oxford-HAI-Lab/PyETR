from typing import cast

from pyetr.atoms import OpenPredicateAtom, PredicateAtom
from pyetr.atoms.terms import (
    ArbitraryObject,
    FunctionalTerm,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    Term,
)
from pyetr.common_parsing import get_quantifiers
from pyetr.dependency import Dependency, DependencyRelation, dependencies_to_sets
from pyetr.issues import IssueStructure
from pyetr.parsing.parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Comma,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicPredicate,
    Quantified,
    Truth,
    Variable,
)
from pyetr.stateset import SetOfStates
from pyetr.view import View


def convert_term(term: Term, open_terms: list[tuple[Term, OpenTerm]]) -> Item:
    if any([isinstance(o, QuestionMark) for _, o in open_terms]):
        remaining_terms = [
            (t, o) for t, o in open_terms if not isinstance(o, QuestionMark)
        ]
        return LogicEmphasis([[convert_term(term, remaining_terms)]])
    if isinstance(term, FunctionalTerm):
        new_subterms: list[Item] = []
        for i, subterm in enumerate(term.t):
            rel_open_terms: list[tuple[Term, OpenTerm]] = []
            for t, o in open_terms:
                assert isinstance(o, OpenFunctionalTerm)
                rel_open_terms.append((t, o.t[i]))
            new_subterms.append(convert_term(subterm, rel_open_terms))
        return LogicPredicate(
            [
                [
                    term.f.name,
                    Comma([new_subterms]),
                ]
            ]
        )

    elif isinstance(term, ArbitraryObject):
        return Variable([term.name])
    else:
        raise ValueError(f"Invalid term {term} provided")


def _convert_atom(
    atom: PredicateAtom, open_atoms: list[tuple[Term, OpenPredicateAtom]]
):
    new_terms: list[Item] = []
    for i, term in enumerate(atom.terms):
        open_terms = [(t, o.terms[i]) for t, o in open_atoms]
        new_terms.append(convert_term(term, open_terms))
    inner = LogicPredicate([[atom.predicate.name, Comma([new_terms])]])
    if atom.predicate.verifier:
        return inner
    else:
        return BoolNot([[inner]])


def convert_atom(
    atom: PredicateAtom,
    issue_structure: IssueStructure,
    issue_atoms: list[PredicateAtom],
):
    open_atoms: list[tuple[Term, OpenPredicateAtom]] = []
    for i, (term, open_atom) in enumerate(issue_structure):
        issue_atom = issue_atoms[i]
        if issue_atom == atom:
            assert isinstance(open_atom, OpenPredicateAtom)
            open_atoms.append((term, open_atom))
    return _convert_atom(atom, open_atoms)


def unparse_set_of_states(s: SetOfStates, issue_structure: IssueStructure) -> Item:
    if s.is_falsum:
        return Falsum([])
    elif s.is_verum:
        return Truth([])
    else:
        assert len(s) > 0
        issue_atoms = cast(list[PredicateAtom], [o(t) for t, o in issue_structure])
        if len(s) == 1:
            state = next(iter(s))
            assert len(state) > 0
            if len(state) == 1:
                # TODO: Fix for doatoms
                atom = next(iter(state))
                assert isinstance(atom, PredicateAtom)
                return convert_atom(atom, issue_structure, issue_atoms)
            else:
                new_atoms: list[LogicPredicate | BoolNot] = []
                for atom in state:
                    # TODO: Fix for doatoms
                    assert isinstance(atom, PredicateAtom)
                    new_atoms.append(convert_atom(atom, issue_structure, issue_atoms))
                return BoolAnd([new_atoms])
        else:
            new_ands: list[LogicPredicate | BoolNot | BoolAnd | Truth] = []
            for state in s:
                if len(state) == 0:
                    new_ands.append(Truth([]))
                elif len(state) == 1:
                    atom = next(iter(state))
                    # TODO: Fix for doatoms
                    assert isinstance(atom, PredicateAtom)
                    new_ands.append(convert_atom(atom, issue_structure, issue_atoms))
                else:
                    # TODO: Fix for doatoms
                    new_ands.append(
                        BoolAnd(
                            [
                                [
                                    convert_atom(atom, issue_structure, issue_atoms)
                                    for atom in state
                                    if isinstance(atom, PredicateAtom)
                                ]
                            ]
                        )
                    )
            return BoolOr([new_ands])


def unparse_view(v: View) -> list[Item]:
    main_item: Item
    if v.supposition.is_verum:
        main_item = unparse_set_of_states(v.stage, v.issue_structure)
    else:
        stage = unparse_set_of_states(v.stage, v.issue_structure)
        supposition = unparse_set_of_states(v.supposition, v.issue_structure)
        main_item = Implies([[supposition, stage]])
    all_arb = v.stage.arb_objects | v.supposition.arb_objects
    output: list[Quantified] = get_quantifiers(all_arb, v.dependency_relation)

    return [*output, main_item]
