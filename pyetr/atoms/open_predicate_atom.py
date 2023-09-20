from typing import Self

from .abstract import AbstractOpen
from .atom_likes import PredicateAtomLike
from .predicate import Predicate
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, OpenTerm, Term


class OpenPredicateAtom(PredicateAtomLike[OpenTerm], AbstractOpen):
    def __init__(self, predicate: Predicate, terms: tuple[OpenTerm, ...]) -> None:
        super().__init__(predicate=predicate, terms=terms)
        self.validate()

    def __call__(self, term: Term) -> PredicateAtom:
        return PredicateAtom(
            predicate=self.predicate, terms=tuple([t(term) for t in self.terms])
        )

    def question_count(self) -> int:
        question_count = 0
        for term in self.terms:
            question_count += term.question_count()
        return question_count

    def validate(self):
        if self.question_count() != 1:
            raise ValueError(f"Open atom {self} must contain exactly one question mark")

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        new_terms = tuple([term.replace(replacements) for term in self.terms])
        return OpenPredicateAtom(predicate=self.predicate, terms=new_terms)

    def __invert__(self) -> Self:
        return OpenPredicateAtom(~self.predicate, self.terms)
