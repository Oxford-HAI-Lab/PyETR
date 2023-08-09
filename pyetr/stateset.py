__all__ = ["State", "SetOfStates"]

from typing import AbstractSet, Iterable, Optional

from .atom import Atom, equals_predicate
from .term import ArbitraryObject, Term


class State(frozenset[Atom]):
    def __new__(cls, __iterable: Optional[Iterable[Atom]] = None, /) -> "State":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "State":
        return State(super().copy())

    def difference(self, *s: Iterable[object]) -> "State":
        return State(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "State":
        return State(super().intersection(*s))

    def symmetric_difference(self, __s: Iterable[Atom]) -> "State":
        return State(super().symmetric_difference(__s))

    def union(self, *s: Iterable[Atom]) -> "State":
        return State(super().union(*s))

    def __and__(self, __value: AbstractSet[Atom]) -> "State":
        return State(super().__and__(__value))

    def __or__(self, __value: AbstractSet[Atom]) -> "State":
        return State(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[Atom]) -> "State":
        return State(super().__sub__(__value))

    def __xor__(self, __value: AbstractSet[Atom]) -> "State":
        return State(super().__xor__(__value))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objects: set[ArbitraryObject] = set()
        for atom in self:
            arb_objects |= atom.arb_objects
        return arb_objects

    @property
    def emphasis_count(self) -> int:
        emphasis_count = 0
        for atom in self:
            emphasis_count += atom.has_emphasis
        return emphasis_count

    def __repr__(self) -> str:
        if len(self) == 0:
            return "0"
        return "".join([repr(i) for i in self])

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self) + "}"

    def replace(
        self, replacements: dict[ArbitraryObject, Term | ArbitraryObject]
    ) -> "State":
        return State([s.replace(replacements) for s in self])

    @property
    def is_primitive_absurd(self) -> bool:
        state = State([a.excluding_emphasis for a in self])
        # LNC
        for atom in state:
            if ~atom in state:
                return True

        # Aristotle
        for atom in state:
            if (atom.predicate == equals_predicate) and (not atom.predicate.verifier):
                if atom.terms[0] == atom.terms[1]:
                    return True

        # Leibniz
        for atom in state:
            if (atom.predicate == equals_predicate) and atom.predicate.verifier:
                t = atom.terms[0]
                t_prime = atom.terms[1]
                for x in state:
                    if t in x.terms:
                        new_x = ~x.replace_low_level(old_term=t, new_term=t_prime)
                        if new_x in state:
                            return True
        return False

    @property
    def atoms(self) -> set[Atom]:
        a = set()
        for atom in self:
            a.add(atom)
        return a


class SetOfStates(frozenset[State]):
    def __new__(cls, __iterable: Optional[Iterable[State]] = None, /) -> "SetOfStates":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "SetOfStates":
        return SetOfStates(super().copy())

    def difference(self, *s: Iterable[object]) -> "SetOfStates":
        return SetOfStates(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "SetOfStates":
        return SetOfStates(super().intersection(*s))

    def symmetric_difference(self, __s: Iterable[State]) -> "SetOfStates":
        return SetOfStates(super().symmetric_difference(__s))

    def union(self, *s: Iterable[State]) -> "SetOfStates":
        return SetOfStates(super().union(*s))

    def __and__(self, __value: AbstractSet[State]) -> "SetOfStates":
        return SetOfStates(super().__and__(__value))

    def __or__(self, __value: AbstractSet[State]) -> "SetOfStates":
        return SetOfStates(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[State]) -> "SetOfStates":
        return SetOfStates(super().__sub__(__value))

    def __xor__(self, __value: AbstractSet[State]) -> "SetOfStates":
        return SetOfStates(super().__xor__(__value))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objects: set[ArbitraryObject] = set()
        for state in self:
            arb_objects |= state.arb_objects
        return arb_objects

    @property
    def emphasis_count(self) -> int:
        emphasis_count = 0
        for state in self:
            emphasis_count += state.emphasis_count
        return emphasis_count

    def __mul__(self, other: "SetOfStates") -> "SetOfStates":
        """
        Definition 4.14 Product of set of states
        """

        output: set[State] = set()
        for state1 in self:
            for state2 in other:
                output.add(state1 | state2)

        return SetOfStates(output)

    def negation(self):
        """
        Definition 4.15 Negation of set of states
        """
        output = None
        for s in self:
            new_state_set_mut: set[State] = set()
            for atom in s:
                new_state = State({~atom})
                new_state_set_mut.add(new_state)
            new_state_set = SetOfStates(new_state_set_mut)
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

    def answer_potential(self, other: "SetOfStates") -> int:
        """
        Based on definition 4.29
        """

        def _get_atoms(s: "SetOfStates"):
            atoms = set()
            for state in s:
                for a in state:
                    atoms.add(a.excluding_emphasis)
            return atoms

        self_atoms = _get_atoms(self)
        other_atoms = _get_atoms(other)
        return len(self_atoms.intersection(other_atoms))

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self])
        return "{" + terms + "}"

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self) + "}"

    def replace(
        self, replacements: dict[ArbitraryObject, Term | ArbitraryObject]
    ) -> "SetOfStates":
        return SetOfStates([s.replace(replacements) for s in self])

    @property
    def atoms(self) -> set[Atom]:
        a = set()
        for state in self:
            a |= state.atoms
        return a

    def flip(self):
        raise NotImplementedError
