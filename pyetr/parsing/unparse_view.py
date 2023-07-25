from pyetr.atom import Atom
from pyetr.dependency import DependencyRelation
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
from pyetr.stateset import set_of_states
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
        return Variable(term.name)
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


def unparse_set_of_states(s: set_of_states) -> Item:
    if s.is_falsum:
        return Falsum([])
    elif s.is_verum:
        return Truth([])
    else:
        return BoolOr(
            [[BoolAnd([[convert_atom(atom) for atom in or_arg]]) for or_arg in s]]
        )


def get_quantifiers(
    arb_objects: set[ArbitraryObject], dep_rel: DependencyRelation
) -> list[Quantified]:
    raise NotImplementedError


def unparse_view(v: View) -> list[Item]:
    main_item: Item
    if v.stage.is_verum:
        main_item = unparse_set_of_states(v.supposition)
    else:
        stage = unparse_set_of_states(v.stage)
        supposition = unparse_set_of_states(v.supposition)
        main_item = Implies([[supposition, stage]])
    all_arb = v.stage.arb_objects | v.supposition.arb_objects
    output: list[Quantified] = get_quantifiers(all_arb, v.dependency_relation)
    return [*output, main_item]
