from pyetr.multiset import Multiset
from pyetr.term import ArbitraryObject, FunctionalTerm, Summation, Term

from .abstract_atom import AbstractAtom, Predicate
from .atom import Atom
from .function import Function
from .open_term import OpenTerm


class OpenAtom(AbstractAtom[OpenTerm]):
    def __init__(self, predicate: Predicate, terms: tuple[OpenTerm, ...]) -> None:
        super().__init__(predicate=predicate, terms=terms)
        self.validate()

    def __call__(self, term: Term) -> Atom:
        return Atom(
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OpenAtom):
            return False
        return self.predicate == other.predicate and self.terms == other.terms

    def __hash__(self) -> int:
        return hash((self.predicate, self.terms))

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenAtom":
        new_terms = tuple([term.replace(replacements) for term in self.terms])
        return OpenAtom(predicate=self.predicate, terms=new_terms)

    def __invert__(self):
        return OpenAtom(~self.predicate, self.terms)

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self.terms])
        if self.predicate.verifier:
            tilda = ""
        else:
            tilda = "~"
        return f"{tilda}{self.predicate.name}({terms})"

    @property
    def detailed(self) -> str:
        return f"<OpenAtom predicate={self.predicate.detailed} terms=({','.join(t.detailed for t in self.terms)})>"
