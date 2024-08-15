from typing import Generic, TypeVar

from pyetr.atoms.terms.multiset import Multiset

from .abstract import AbstractAtom
from .predicate import Predicate
from .terms.abstract_term import TermType

AtomType = TypeVar("AtomType", bound=AbstractAtom)


class PredicateAtomLike(Generic[TermType]):
    """
    This "AtomLike" is a mixin for the predicate-like properties associated
    with PredicateAtom and PredicateOpenAtom
    """

    predicate: Predicate
    terms: tuple[TermType, ...]

    def __init__(
        self,
        predicate: Predicate,
        terms: tuple[TermType, ...],
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError(
                f"Inconsistent - number of terms does not equal arity in {terms} for predicate {predicate}"
            )
        self.predicate = predicate
        self.terms = terms

    @property
    def detailed(self) -> str:
        return f"<{type(self).__name__} predicate={self.predicate.detailed} terms=({','.join(t.detailed for t in self.terms)})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.predicate == other.predicate and self.terms == other.terms

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.predicate, self.terms))

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self.terms])
        if self.predicate.verifier:
            tilde = ""
        else:
            tilde = "~"
        return f"{tilde}{self.predicate.name}({terms})"
