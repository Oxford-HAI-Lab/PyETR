from pyetr.atom import Atom
from pyetr.dependency import Dependency, DependencyRelation, dependencies_to_sets
from pyetr.issues import IssueStructure
from pyetr.open_atom import OpenAtom
from pyetr.open_term import OpenFunctionalTerm, OpenTerm, QuestionMark
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
from pyetr.term import ArbitraryObject, FunctionalTerm, Term
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


def _convert_atom(atom: Atom, open_atoms: list[tuple[Term, OpenAtom]]):
    new_terms: list[Item] = []
    for i, term in enumerate(atom.terms):
        open_terms = [(t, o.terms[i]) for t, o in open_atoms]
        new_terms.append(convert_term(term, open_terms))
    inner = LogicPredicate([[atom.predicate.name, Comma([new_terms])]])
    if atom.predicate.verifier:
        return inner
    else:
        return BoolNot([[inner]])


def convert_atom(atom: Atom, issue_structure: IssueStructure, issue_atoms: list[Atom]):
    open_atoms: list[tuple[Term, OpenAtom]] = []
    for i, atom_pair in enumerate(issue_structure):
        issue_atom = issue_atoms[i]
        if issue_atom == atom:
            open_atoms.append(atom_pair)
    return _convert_atom(atom, open_atoms)


def unparse_set_of_states(s: SetOfStates, issue_structure: IssueStructure) -> Item:
    if s.is_falsum:
        return Falsum([])
    elif s.is_verum:
        return Truth([])
    else:
        assert len(s) > 0
        issue_atoms = [o(t) for t, o in issue_structure]
        if len(s) == 1:
            state = next(iter(s))
            assert len(state) > 0
            if len(state) == 1:
                return convert_atom(next(iter(state)), issue_structure, issue_atoms)
            else:
                new_atoms: list[LogicPredicate | BoolNot] = []
                for atom in state:
                    new_atoms.append(convert_atom(atom, issue_structure, issue_atoms))
                return BoolAnd([new_atoms])
        else:
            new_ands: list[LogicPredicate | BoolNot | BoolAnd | Truth] = []
            for state in s:
                if len(state) == 0:
                    new_ands.append(Truth([]))
                elif len(state) == 1:
                    atom = next(iter(state))
                    new_ands.append(convert_atom(atom, issue_structure, issue_atoms))
                else:
                    new_ands.append(
                        BoolAnd(
                            [
                                [
                                    convert_atom(atom, issue_structure, issue_atoms)
                                    for atom in state
                                ]
                            ]
                        )
                    )
            return BoolOr([new_ands])


class QuantList:
    variables: list[Variable]
    quantifier: str

    def __init__(self, variables: list[Variable], quantifier: str) -> None:
        self.variables = variables
        self.quantifier = quantifier


def order_quantifieds(
    unordered_quantifieds: dict[str, Quantified], dependencies: frozenset[Dependency]
) -> list[Quantified]:
    # All unspecified exis get put to the front
    # The ordering is based on the right most having the least
    # restrictions, then moving left with more and more deps
    # Therefore, we must start with the smallest exi sets
    exis_used: list[str] = []
    univs_used: list[str] = []
    dep_sets = dependencies_to_sets(dependencies)
    sorted_universals: list[tuple[int, ArbitraryObject, set[ArbitraryObject]]] = sorted(
        [(len(exi_set), uni, exi_set) for uni, exi_set in dep_sets]
    )
    final_out: list[Quantified] = []
    for _, uni, exi_set in sorted_universals:
        # Fill list from the front
        new_exis: list[Quantified] = []
        for exi in exi_set:
            if exi.name not in exis_used:
                exis_used.append(exi.name)
                new_exis.append(unordered_quantifieds[exi.name])
        univs_used.append(uni.name)
        final_out = [unordered_quantifieds[uni.name], *new_exis, *final_out]

    for name, quantified in unordered_quantifieds.items():
        if quantified.quantifier == "∃":
            if name not in exis_used:
                final_out.insert(0, quantified)
        elif quantified.quantifier == "∀":
            if name not in univs_used:
                final_out.append(quantified)
        else:
            assert False

    return final_out


def get_quantifiers(
    arb_objects: set[ArbitraryObject], dependency_relation: DependencyRelation
) -> list[Quantified]:
    unordered_quantifieds: dict[str, Quantified] = {}
    for arb_object in arb_objects:
        if arb_object.name not in unordered_quantifieds:
            if dependency_relation.is_existential(arb_object):
                quant = "∃"
            else:
                quant = "∀"
            unordered_quantifieds[arb_object.name] = Quantified(
                [QuantList([Variable([arb_object.name])], quantifier=quant)]
            )
    return order_quantifieds(unordered_quantifieds, dependency_relation.dependencies)


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
