from typing import AbstractSet, Iterable, Optional

from .atoms import Atom, OpenAtom
from .atoms.terms import ArbitraryObject, Term
from .stateset import SetOfStates


class IssueStructure(frozenset[tuple[Term, OpenAtom]]):
    """
    An IssueStructure is a set of <Term, OpenAtom> where each open atom
    has exactly one question mark
    """

    def __new__(
        cls, __iterable: Optional[Iterable[tuple[Term, OpenAtom]]] = None, /
    ) -> "IssueStructure":
        if __iterable is None:
            return super().__new__(cls)
        else:
            cls._validate(__iterable)
            return super().__new__(cls, __iterable)

    def copy(self) -> "IssueStructure":  # pragma: not covered
        return IssueStructure(super().copy())

    def difference(
        self, *s: Iterable[object]
    ) -> "IssueStructure":  # pragma: not covered
        return IssueStructure(super().difference(*s))

    def intersection(
        self, *s: Iterable[object]
    ) -> "IssueStructure":  # pragma: not covered
        return IssueStructure(super().intersection(*s))

    def symmetric_difference(
        self, __s: Iterable[tuple[Term, OpenAtom]]
    ) -> "IssueStructure":  # pragma: not covered
        return IssueStructure(super().symmetric_difference(__s))

    def union(self, *s: Iterable[tuple[Term, OpenAtom]]) -> "IssueStructure":
        return IssueStructure(super().union(*s))  # pragma: not covered

    def __and__(self, __value: AbstractSet[tuple[Term, OpenAtom]]) -> "IssueStructure":
        return IssueStructure(super().__and__(__value))  # pragma: not covered

    def __or__(self, __value: AbstractSet[tuple[Term, OpenAtom]]) -> "IssueStructure":
        return IssueStructure(super().__or__(__value))  # pragma: not covered

    def __sub__(self, __value: AbstractSet[tuple[Term, OpenAtom]]) -> "IssueStructure":
        return IssueStructure(super().__sub__(__value))  # pragma: not covered

    def __xor__(self, __value: AbstractSet[tuple[Term, OpenAtom]]) -> "IssueStructure":
        return IssueStructure(super().__xor__(__value))  # pragma: not covered

    def restriction(self, atoms: set[Atom]) -> "IssueStructure":
        return IssueStructure(
            {(term, open_atom) for term, open_atom in self if open_atom(term) in atoms}
        )

    @classmethod
    def _validate(cls, __iterable: Iterable[tuple[Term, OpenAtom]]):
        for _, o in __iterable:
            if o.question_count() != 1:
                raise ValueError(
                    f"Open atom {o} must contain exactly one question mark"
                )

    def validate_against_states(self, states: SetOfStates):
        for t, a in self:
            atom = a(t)
            if atom not in states.atoms and ~atom not in states.atoms:
                raise ValueError(
                    f"Issue atom {(t, a)} is not a subset of atoms in stage/supposition: {states.atoms}"
                )

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "IssueStructure":
        """
        Replaces one arbitrary object found in the dependency with another term from a mapping.

        Args:
            replacements (dict[ArbitraryObject, Term]): Mapping of replacements.

        Returns:
            IssueStructure: The issue structure with replacements made.
        """
        return IssueStructure(
            {(t.replace(replacements), a.replace(replacements)) for t, a in self}
        )

    def negation(self) -> "IssueStructure":
        """
        Based on definition 4.31, p159

        [I]ᶰ = I ∪ {<t,x̄> : <t,x> ∈ I}

        Negates an Issue structure

        Returns:
            IssueStructure: The new issue structure
        """
        return self | IssueStructure((t, ~a) for t, a in self)

    @property
    def detailed(self):
        return "{" + ",".join([a.detailed for _, a in self]) + "}"
