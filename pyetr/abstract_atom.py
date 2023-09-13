__all__ = ["AbstractTerm", "AbstractAtom", "AbstractPredicate"]

from typing import Generic, TypeVar, cast


AbstractTerm = TypeVar("AbstractTerm")

class AbstractAtom(Generic[AbstractTerm]):
    predicate: "AbstractPredicate[AbstractTerm]"
    terms: tuple[AbstractTerm, ...]
    def __init__(
        self,
        predicate: "AbstractPredicate[AbstractTerm]",
        terms: tuple[AbstractTerm, ...],
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError(
                f"Inconsistent - number of terms does not equal arity in {terms} for predicate {predicate}"
            )
        self.predicate = predicate
        self.terms = terms

class AbstractPredicate(Generic[AbstractTerm]):
    name: str
    verifier: bool
    arity: int

    def __init__(self, name: str, arity: int, _verifier: bool = True) -> None:
        self.verifier = _verifier
        self.name = name
        self.arity = arity

    def __invert__(self):
        return AbstractPredicate(name=self.name, arity=self.arity, _verifier=not self.verifier)

    def __repr__(self) -> str:
        return f"<AbstractPredicate name={self.name} arity={self.arity}>"

    @property
    def detailed(self) -> str:
        return repr(self)

    def __call__(
        self, terms: tuple[AbstractTerm, ...]
    ) -> AbstractAtom:
        return AbstractAtom(self, terms)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AbstractPredicate):
            return False
        return (
            self.name == other.name
            and self.arity == other.arity
            and self.verifier == other.verifier
        )

    def __hash__(self) -> int:
        return hash((self.name, self.arity, self.verifier))
