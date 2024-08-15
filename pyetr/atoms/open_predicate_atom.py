from pyetr.atoms.terms.open_term import get_open_equivalent

from .abstract import AbstractAtom, Atom
from .atom_likes import PredicateAtomLike
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, OpenTerm, Term


class OpenPredicateAtom(PredicateAtomLike[OpenTerm], AbstractAtom):
    def __call__(self, term: Term) -> PredicateAtom:
        return PredicateAtom(
            predicate=self.predicate, terms=tuple([t(term) for t in self.terms])
        )

    def question_count(self) -> int:
        question_count = 0
        for term in self.terms:
            question_count += term.question_count()
        return question_count

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenPredicateAtom":
        new_terms = tuple([term.replace(replacements) for term in self.terms])
        return OpenPredicateAtom(predicate=self.predicate, terms=new_terms)

    def __invert__(self) -> "OpenPredicateAtom":
        return OpenPredicateAtom(~self.predicate, self.terms)

    def context_equals(self, atom: "Atom", question_term: "Term") -> bool:
        if not isinstance(atom, PredicateAtom):
            return False
        if self.predicate != atom.predicate or len(self.terms) != len(atom.terms):
            return False

        return all(
            t.context_equals(atom.terms[i], question_term)
            for i, t in enumerate(self.terms)
        )


def get_open_atom_equivalent(atom: PredicateAtom) -> OpenPredicateAtom:
    return OpenPredicateAtom(
        predicate=atom.predicate,
        terms=tuple([get_open_equivalent(t) for t in atom.terms]),
    )
