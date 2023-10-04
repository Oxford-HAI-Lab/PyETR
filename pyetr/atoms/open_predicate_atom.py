from typing import Self

from pyetr.atoms.terms.open_term import get_open_equivalent

from .abstract import OpenAtom
from .atom_likes import PredicateAtomLike
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, OpenTerm, Term


class OpenPredicateAtom(PredicateAtomLike[OpenTerm], OpenAtom):
    def __call__(self, term: Term) -> PredicateAtom:
        return PredicateAtom(
            predicate=self.predicate, terms=tuple([t(term) for t in self.terms])
        )

    def question_count(self) -> int:
        question_count = 0
        for term in self.terms:
            question_count += term.question_count()
        return question_count

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        new_terms = tuple([term.replace(replacements) for term in self.terms])
        return OpenPredicateAtom(predicate=self.predicate, terms=new_terms)

    def __invert__(self) -> Self:
        return OpenPredicateAtom(~self.predicate, self.terms)


def get_open_atom_equivalent(atom: PredicateAtom) -> OpenPredicateAtom:
    return OpenPredicateAtom(
        predicate=atom.predicate,
        terms=tuple([get_open_equivalent(t) for t in atom.terms]),
    )
