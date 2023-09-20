from typing import AbstractSet, Iterable, Optional

from .atoms import AbstractOpen, PredicateAtom
from .atoms.terms import ArbitraryObject, Term
from .stateset import SetOfStates


class IssueStructure(frozenset[tuple[Term, AbstractOpen]]):
    # IssueStructure contains (is) a set of atoms where each has exactly one emphasis
    # Atoms in the stage and supposition have 0 emphasis
    def __new__(
        cls, __iterable: Optional[Iterable[tuple[Term, AbstractOpen]]] = None, /
    ) -> "IssueStructure":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "IssueStructure":
        return IssueStructure(super().copy())

    def difference(self, *s: Iterable[object]) -> "IssueStructure":
        return IssueStructure(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "IssueStructure":
        return IssueStructure(super().intersection(*s))

    def symmetric_difference(
        self, __s: Iterable[tuple[Term, AbstractOpen]]
    ) -> "IssueStructure":
        return IssueStructure(super().symmetric_difference(__s))

    def union(self, *s: Iterable[tuple[Term, AbstractOpen]]) -> "IssueStructure":
        return IssueStructure(super().union(*s))

    def __and__(
        self, __value: AbstractSet[tuple[Term, AbstractOpen]]
    ) -> "IssueStructure":
        return IssueStructure(super().__and__(__value))

    def __or__(
        self, __value: AbstractSet[tuple[Term, AbstractOpen]]
    ) -> "IssueStructure":
        return IssueStructure(super().__or__(__value))

    def __sub__(
        self, __value: AbstractSet[tuple[Term, AbstractOpen]]
    ) -> "IssueStructure":
        return IssueStructure(super().__sub__(__value))

    def __xor__(
        self, __value: AbstractSet[tuple[Term, AbstractOpen]]
    ) -> "IssueStructure":
        return IssueStructure(super().__xor__(__value))

    def restriction(self, atoms: set[PredicateAtom]) -> "IssueStructure":
        return IssueStructure(
            {(term, open_atom) for term, open_atom in self if open_atom(term) in atoms}
        )

    def validate_against_states(self, states: SetOfStates):
        for t, a in self:
            atom = a(t)
            if atom not in states.atoms and ~atom not in states.atoms:
                raise ValueError(
                    f"Issue atom {(t, a)} is not a subset of atoms in stage/supposition: {states.atoms}"
                )

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "IssueStructure":
        return IssueStructure(
            {(t.replace(replacements), a.replace(replacements)) for t, a in self}
        )

    def negation(self) -> "IssueStructure":
        return self | IssueStructure((t, ~a) for t, a in self)

    @property
    def detailed(self):
        return "{" + ",".join([a.detailed for t, a in self]) + "}"
