__all__ = ["State", "SetOfStates"]

from functools import reduce
from typing import TYPE_CHECKING, AbstractSet, Iterable, Optional

from pyetr.atoms.terms.special_funcs import multiset_product

from .atoms import Atom, PredicateAtom, equals_predicate
from .atoms.terms import ArbitraryObject, FunctionalTerm, Multiset, Summation, Term

if TYPE_CHECKING:
    from pyetr.weight import Weights


class State(frozenset[Atom]):
    """
    A frozen set of atoms.
    """

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
        """
        The arbitrary objects in the state

        Returns:
            set[ArbitraryObject]: The set of arbitrary objects
        """
        arb_objects: set[ArbitraryObject] = set()
        for atom in self:
            arb_objects |= atom.arb_objects
        return arb_objects

    def __repr__(self) -> str:
        if len(self) == 0:
            return "0"
        return "".join([repr(i) for i in self])

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self) + "}"

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "State":
        """
        Replaces a series of arbitrary objects with terms and makes a new states.

        Args:
            replacements (dict[ArbitraryObject, Term]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            State: The new states.
        """
        return State([s.replace(replacements) for s in self])

    def replace_term(self, old_term: Term, new_term: Term) -> "State":
        return State(
            {i.replace_term(old_term=old_term, new_term=new_term) for i in self}
        )

    def is_primitive_absurd(self, absurd_states: Optional[list["State"]]) -> bool:
        """
        Based on definition 4.13, p147

        ∀t,t'_∈T ∀p_∈𝓐 ∀x_∈𝓐₁

        contain at least {p, p̄}, {≠tt}, {=tt',x[t/?],x̄[t'/?]}
        Args:
            absurd_states (Optional[list["State"]]): The custom absurd states.

        Returns:
            bool: True if the state is primitive absurd.
        """
        state = self
        if absurd_states is not None:
            for absurd_state in absurd_states:
                if absurd_state.issubset(state):
                    return True
        # LNC
        # {p, p̄}
        for atom in state:
            if ~atom in state:
                return True

        # Aristotle
        # {≠tt}
        for atom in state:
            if (
                isinstance(atom, PredicateAtom)
                and (atom.predicate == equals_predicate)
                and (not atom.predicate.verifier)
            ):
                if atom.terms[0] == atom.terms[1]:
                    return True

        # Leibniz
        # {=tt',x[t/?],x̄[t'/?]}
        for atom in state:
            if (
                isinstance(atom, PredicateAtom)
                and (atom.predicate == equals_predicate)
                and atom.predicate.verifier
            ):
                t = atom.terms[0]
                t_prime = atom.terms[1]
                for x in state:
                    if isinstance(x, PredicateAtom) and t in x.terms:
                        new_x = ~x.replace_low_level(old_term=t, new_term=t_prime)
                        if new_x in state:
                            return True
        return False

    @property
    def atoms(self) -> set[Atom]:
        a: set[Atom] = set()
        for atom in self:
            a.add(atom)
        return a


class SetOfStates(frozenset[State]):
    """
    A frozen set of states.
    """

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
        """
        The arbitrary objects in the set of states

        Returns:
            set[ArbitraryObject]: The set of arbitrary objects
        """
        arb_objects: set[ArbitraryObject] = set()
        for state in self:
            arb_objects |= state.arb_objects
        return arb_objects

    def __mul__(self, other: "SetOfStates") -> "SetOfStates":
        """
        Definition 4.14 Product of set of states, p151 # TODO: Note differs from book usage, this is for
            first order logic parser in book.

        Γ ⨂ Δ = {γ∪δ : γ ∈ Γ, δ ∈ Δ}
        """
        return SetOfStates({state1 | state2 for state1 in self for state2 in other})

    def negation(self):
        """
        Based on Definition 4.15, p151

        Negation of set of states # TODO: Note differs from book usage, this is for
            first order logic parser in book.

        [Γ]ᶰ = {{p̄} : p ∈ γ₁} ⨂ ... ⨂ {{p̄} : p ∈ γₙ}
        """
        output = None
        for s in self:
            new_state_set_mut: set[State] = set()
            for atom in s:
                # {p̄}
                new_state = State({~atom})
                new_state_set_mut.add(new_state)
            # {{p̄} : p ∈ γₙ}
            new_state_set = SetOfStates(new_state_set_mut)
            if output is None:
                output = new_state_set
            else:
                output = output * new_state_set

        if output is None and self.is_falsum:
            return SetOfStates({State()})
        assert output is not None

        return output

    @property
    def is_verum(self):
        """
        Returns true if the state is verum.
        """
        if len(self) == 1:
            first_elem = next(iter(self))
            return len(first_elem) == 0
        else:
            return False

    @property
    def is_falsum(self):
        """
        Returns true if the state is falsum.
        """
        return len(self) == 0

    def atomic_answer_potential(self, other: "SetOfStates") -> int:
        """
        Based on definition A.67
        """
        return len(self.atoms.intersection(other.atoms))

    def equilibrium_answer_potential(
        self, other: "SetOfStates", weights: "Weights"
    ) -> FunctionalTerm:
        """
        Based on definition 5.8, p204

        Δ_g[Γ]^𝔼P = σ(《σ(g(δ)) | δ ∈ Y》)
        Y = {δ ∈ Δ | ∃γ ∈ Γ.γ ⊆ δ}
        """
        # Y = {δ ∈ Δ | ∃γ ∈ Γ.γ ⊆ δ}
        Y = SetOfStates(
            {delta for delta in self if any([gamma.issubset(delta) for gamma in other])}
        )
        # 《σ(g(δ)) | δ ∈ Y》
        expr1: Multiset[Term] = reduce(
            lambda x, y: x + y,
            [
                multiset_product(weights[delta].multiplicative, weights[delta].additive)
                for delta in Y
            ],
            Multiset[Term]([]),
        )
        # σ(EXPR1)
        return FunctionalTerm(f=Summation, t=expr1)

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self])
        return "{" + terms + "}"

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self) + "}"

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "SetOfStates":
        """
        Replaces a series of arbitrary objects with terms and makes a new set of states.

        Args:
            replacements (dict[ArbitraryObject, Term]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            SetOfStates: The new set of states.
        """
        return SetOfStates([s.replace(replacements) for s in self])

    @property
    def atoms(self) -> set[Atom]:
        """
        Get the set of atoms in a state.

        Returns:
            set[Atom]: The atoms in a state.
        """
        a: set[Atom] = set()
        for state in self:
            a |= state.atoms
        return a


Stage = SetOfStates
Supposition = SetOfStates
