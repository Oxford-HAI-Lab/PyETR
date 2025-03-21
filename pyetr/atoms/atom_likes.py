from typing import Generic, TypeVar

from .abstract import AbstractAtom
from .predicate import Predicate
from .terms.abstract_term import TermType

AtomType = TypeVar("AtomType", bound=AbstractAtom)
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: not covered
    from pyetr.types import MatchCallback, MatchItem


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

    def match(
        self,
        old_item: "MatchItem",
        callback: "MatchCallback",
    ):
        new_terms = [
            term.match(old_item=old_item, callback=callback) for term in self.terms
        ]
        if self.predicate == old_item or self.predicate.name == old_item:
            new_predicate = callback(self.predicate)
            assert isinstance(new_predicate, Predicate)
        else:
            new_predicate = self.predicate
        return self.__class__(predicate=new_predicate, terms=tuple(new_terms))
