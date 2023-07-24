__all__ = ["state"]

from typing import AbstractSet, Iterable, Optional

from .atom import Atom
from .term import ArbitraryObject


class state(frozenset[Atom]):
    def __new__(cls, __iterable: Optional[Iterable[Atom]] = None, /) -> "state":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "state":
        return state(super().copy())

    def difference(self, *s: Iterable[object]) -> "state":
        return state(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "state":
        return state(super().intersection(*s))

    def symmetric_difference(self, __s: Iterable[Atom]) -> "state":
        return state(super().symmetric_difference(__s))

    def union(self, *s: Iterable[Atom]) -> "state":
        return state(super().union(*s))

    def __and__(self, __value: AbstractSet[Atom]) -> "state":
        return state(super().__and__(__value))

    def __or__(self, __value: AbstractSet[Atom]) -> "state":
        return state(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[Atom]) -> "state":
        return state(super().__sub__(__value))

    def __xor__(self, __value: AbstractSet[Atom]) -> "state":
        return state(super().__xor__(__value))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objects: set[ArbitraryObject] = set()
        for atom in self:
            arb_objects |= atom.arb_objects
        return arb_objects

    @property
    def has_emphasis(self) -> bool:
        emphasis_count = 0
        for atom in self:
            emphasis_count += atom.has_emphasis
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in state at: {emphasis_count}")
        else:
            return emphasis_count == 1


class set_of_states(frozenset[state]):
    def __new__(
        cls, __iterable: Optional[Iterable[state]] = None, /
    ) -> "set_of_states":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "set_of_states":
        return set_of_states(super().copy())

    def difference(self, *s: Iterable[object]) -> "set_of_states":
        return set_of_states(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "set_of_states":
        return set_of_states(super().intersection(*s))

    def symmetric_difference(self, __s: Iterable[state]) -> "set_of_states":
        return set_of_states(super().symmetric_difference(__s))

    def union(self, *s: Iterable[state]) -> "set_of_states":
        return set_of_states(super().union(*s))

    def __and__(self, __value: AbstractSet[state]) -> "set_of_states":
        return set_of_states(super().__and__(__value))

    def __or__(self, __value: AbstractSet[state]) -> "set_of_states":
        return set_of_states(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[state]) -> "set_of_states":
        return set_of_states(super().__sub__(__value))

    def __xor__(self, __value: AbstractSet[state]) -> "set_of_states":
        return set_of_states(super().__xor__(__value))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objects: set[ArbitraryObject] = set()
        for state in self:
            arb_objects |= state.arb_objects
        return arb_objects

    @property
    def has_emphasis(self) -> bool:
        emphasis_count = 0
        for state in self:
            emphasis_count += state.has_emphasis
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in state at: {emphasis_count}")
        else:
            return emphasis_count == 1

    def __mul__(self, other: "set_of_states") -> "set_of_states":
        """
        Definition 4.14 Product of set of states
        """

        output: set[state] = set()
        for state1 in self:
            for state2 in other:
                output.add(state1 | state2)

        return set_of_states(output)

    def negation(self):
        """
        Definition 4.15 Negation of set of states
        """
        output = None
        for s in self:
            new_state_set_mut: set[state] = set()
            for atom in s:
                new_state = state({~atom})
                new_state_set_mut.add(new_state)
            new_state_set = set_of_states(new_state_set_mut)
            if output is None:
                output = new_state_set
            else:
                output = output * new_state_set
        assert output is not None
        return output

    @property
    def is_verum(self):
        if len(self) == 1:
            first_elem = next(iter(self))
            return len(first_elem) == 0
        else:
            return False

    @property
    def is_falsum(self):
        return len(self) == 0

    def answer_potential(self, other: "set_of_states") -> int:
        """
        Based on definition 4.29
        """
        return len(self.intersection(other))
