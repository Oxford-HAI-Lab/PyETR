from pyetr.atom import Atom
from pyetr.dependency import Dependency, dependencies_to_sets
from pyetr.parsing.parse_string import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Comma,
    Constant,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicFunction,
    LogicPredicate,
    Quantified,
    Truth,
    Variable,
)
from pyetr.stateset import SetOfStates
from pyetr.term import ArbitraryObject, Emphasis, Term
from pyetr.view import View


def convert_term(term: Term | ArbitraryObject | Emphasis) -> Item:
    if isinstance(term, Term):
        if term.t is None:
            return Constant([[term.f.name]])
        else:
            return LogicFunction(
                [
                    [
                        "f_",
                        term.f.name,
                        Comma([[convert_term(subterm) for subterm in term.t]]),
                    ]
                ]
            )

    elif isinstance(term, ArbitraryObject):
        return Variable([term.name])
    elif isinstance(term, Emphasis):
        return LogicEmphasis([[convert_term(term.term)]])
    else:
        raise ValueError(f"Invalid term {term} provided")


def convert_atom(atom: Atom):
    inner = LogicPredicate(
        [[atom.predicate.name, Comma([[convert_term(term) for term in atom.terms]])]]
    )
    if atom.predicate.verifier:
        return inner
    else:
        return BoolNot([[inner]])


def unparse_set_of_states(s: SetOfStates) -> Item:
    if s.is_falsum:
        return Falsum([])
    elif s.is_verum:
        return Truth([])
    else:
        assert len(s) > 0
        if len(s) == 1:
            state = next(iter(s))
            assert len(state) > 0
            if len(state) == 1:
                atom = next(iter(state))
                return convert_atom(atom)
            else:
                return BoolAnd([[convert_atom(atom) for atom in state]])
        else:
            new_ands: list[LogicPredicate | BoolNot | BoolAnd] = []
            for state in s:
                assert len(state) > 0
                if len(state) == 1:
                    atom = next(iter(state))
                    new_ands.append(convert_atom(atom))
                else:
                    new_ands.append(BoolAnd([[convert_atom(atom) for atom in state]]))
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
    arb_objects: set[ArbitraryObject], dependencies: frozenset[Dependency]
) -> list[Quantified]:
    unordered_quantifieds: dict[str, Quantified] = {}
    for arb_object in arb_objects:
        if arb_object.name not in unordered_quantifieds:
            if arb_object.is_existential:
                quant = "∃"
            else:
                quant = "∀"
            unordered_quantifieds[arb_object.name] = Quantified(
                [QuantList([Variable([arb_object.name])], quantifier=quant)]
            )
    return order_quantifieds(unordered_quantifieds, dependencies)


def unparse_view(v: View) -> list[Item]:
    main_item: Item
    if v.supposition.is_verum:
        main_item = unparse_set_of_states(v.stage)
    else:
        stage = unparse_set_of_states(v.stage)
        supposition = unparse_set_of_states(v.supposition)
        main_item = Implies([[supposition, stage]])
    all_arb = v.stage.arb_objects | v.supposition.arb_objects
    output: list[Quantified] = get_quantifiers(
        all_arb, v.dependency_relation.dependencies
    )
    return [*output, main_item]
