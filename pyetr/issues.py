from typing import AbstractSet, Iterable, Optional

from pyetr.atom import Atom
from pyetr.stateset import SetOfStates
from pyetr.term import ArbitraryObject, FunctionalTerm


class IssueStructure(frozenset[Atom]):
    # IssueStructure contains (is) a set of atoms where each has exactly one emphasis
    # Atoms in the stage and supposition have 0 emphasis
    def __new__(
        cls, __iterable: Optional[Iterable[Atom]] = None, /
    ) -> "IssueStructure":
        if __iterable is None:
            return super().__new__(cls)
        else:
            cls.validate(__iterable)
            return super().__new__(cls, __iterable)

    @classmethod
    def validate(cls, atoms: Iterable[Atom]):
        for atom in atoms:
            if atom.emphasis_count != 1:
                raise TypeError(
                    f"Incorrect atom type: {atom} provided to issue structure"
                )

    def copy(self) -> "IssueStructure":
        return IssueStructure(super().copy())

    def difference(self, *s: Iterable[object]) -> "IssueStructure":
        return IssueStructure(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "IssueStructure":
        return IssueStructure(super().intersection(*s))

    def symmetric_difference(self, __s: Iterable[Atom]) -> "IssueStructure":
        return IssueStructure(super().symmetric_difference(__s))

    def union(self, *s: Iterable[Atom]) -> "IssueStructure":
        return IssueStructure(super().union(*s))

    def __and__(self, __value: AbstractSet[Atom]) -> "IssueStructure":
        return IssueStructure(super().__and__(__value))

    def __or__(self, __value: AbstractSet[Atom]) -> "IssueStructure":
        return IssueStructure(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[Atom]) -> "IssueStructure":
        return IssueStructure(super().__sub__(__value))

    def __xor__(self, __value: AbstractSet[Atom]) -> "IssueStructure":
        return IssueStructure(super().__xor__(__value))

    def restriction(self, atoms: set[Atom]) -> "IssueStructure":
        return IssueStructure(
            {atom for atom in self if atom.excluding_emphasis in atoms}
        )

    def validate_against_states(self, states: SetOfStates):
        atoms = {a.excluding_emphasis for a in self}
        if not atoms.issubset(states.atoms):
            raise ValueError(
                f"Issue atoms {atoms} is not a subset of atoms in stage/supposition: {states.atoms}"
            )

    def replace(
        self, replacements: dict[ArbitraryObject, FunctionalTerm | ArbitraryObject]
    ) -> "IssueStructure":
        return IssueStructure({a.replace(replacements) for a in self})

    def negation(self) -> "IssueStructure":
        return self | IssueStructure(~a for a in self)

    @property
    def detailed(self):
        return "{" + ",".join([a.detailed for a in self]) + "}"
