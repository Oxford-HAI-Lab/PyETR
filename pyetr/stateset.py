__all__ = ["State", "SetOfStates"]

from copy import copy
from functools import reduce
from typing import TYPE_CHECKING, AbstractSet, Iterable, Optional

from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_predicate_atom import OpenPredicateAtom
from pyetr.atoms.predicate import Predicate
from pyetr.atoms.terms.function import Function
from pyetr.atoms.terms.open_term import (
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    get_open_equivalent,
)
from pyetr.atoms.terms.special_funcs import multiset_product

from .atoms import Atom, PredicateAtom, equals_predicate
from .atoms.terms import ArbitraryObject, FunctionalTerm, Multiset, Summation, Term

if TYPE_CHECKING:  # pragma: not covered
    from pyetr.weight import Weights

    from .types import MatchCallback, MatchItem


def _get_open_terms(term: Term, search_term: Term) -> list[OpenTerm]:
    if term == search_term:
        return [QuestionMark()]
    else:
        if isinstance(term, FunctionalTerm):
            template_new_subterms = [get_open_equivalent(i) for i in term.t]
            new_open_terms: list[OpenTerm] = []
            for j, subterm in enumerate(term.t):
                open_t = _get_open_terms(subterm, search_term)
                for new_subterm in open_t:
                    new_subterms = copy(template_new_subterms)
                    new_subterms[j] = new_subterm
                    new_open_terms.append(OpenFunctionalTerm(f=term.f, t=new_subterms))
            return new_open_terms
        elif isinstance(term, ArbitraryObject):
            return []
        else:
            assert False


def get_opens(atom: PredicateAtom, search_term: Term) -> list[OpenPredicateAtom]:
    template_new_terms = [get_open_equivalent(i) for i in atom.terms]
    new_open_atoms: list[OpenPredicateAtom] = []
    for i, t in enumerate(atom.terms):
        open_t = _get_open_terms(t, search_term)
        for new_t in open_t:
            new_terms = copy(template_new_terms)
            new_terms[i] = new_t
            new_open_atoms.append(
                OpenPredicateAtom(predicate=atom.predicate, terms=tuple(new_terms))
            )
    return new_open_atoms


class State(frozenset[Atom]):
    """
    A frozen set of atoms.
    """

    def __new__(cls, __iterable: Optional[Iterable[Atom]] = None, /) -> "State":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "State":  # pragma: not covered
        return State(super().copy())

    def difference(self, *s: Iterable[object]) -> "State":  # pragma: not covered
        return State(super().difference(*s))

    def intersection(self, *s: Iterable[object]) -> "State":  # pragma: not covered
        return State(super().intersection(*s))

    def symmetric_difference(
        self, __s: Iterable[Atom]
    ) -> "State":  # pragma: not covered
        return State(super().symmetric_difference(__s))

    def union(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, *s: Iterable[Atom]
    ) -> "State":  # pragma: not covered
        return State(super().union(*s))

    def __and__(self, __value: AbstractSet[Atom]) -> "State":  # pragma: not covered
        return State(super().__and__(__value))

    def __or__(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, __value: AbstractSet[Atom]
    ) -> "State":
        return State(super().__or__(__value))

    def __sub__(self, __value: AbstractSet[Atom]) -> "State":
        return State(super().__sub__(__value))

    def __xor__(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, __value: AbstractSet[Atom]
    ) -> "State":  # pragma: not covered
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
        return "".join([repr(i) for i in self.sorted_iter()])

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self.sorted_iter()) + "}"

    def _replace_arbs(self, replacements: dict[ArbitraryObject, Term]) -> "State":
        """
        Replaces a series of arbitrary objects with terms and makes a new states.

        Args:
            replacements (dict[ArbitraryObject, Term]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            State: The new states.
        """
        return State([s._replace_arbs(replacements) for s in self])

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
            if isinstance(atom, PredicateAtom) and (
                atom.predicate == ~equals_predicate
            ):
                if atom.terms[0] == atom.terms[1]:
                    return True

        # Leibniz
        # {=tt',x[t/?],x̄[t'/?]}
        for atom in state:
            if isinstance(atom, PredicateAtom) and (atom.predicate == equals_predicate):
                t = atom.terms[0]
                t_prime = atom.terms[1]
                for x in state:
                    if isinstance(x, PredicateAtom) and t in x.terms:
                        new_atoms = set([~o(t_prime) for o in get_opens(x, t)])
                        if any((atom in state) for atom in new_atoms):
                            return True
        return False

    @property
    def atoms(self) -> set[Atom]:
        a: set[Atom] = set()
        for atom in self:
            a.add(atom)
        return a

    def sorted_iter(self):
        return sorted(self, key=str)

    def match(self, old_item: "MatchItem", callback: "MatchCallback") -> "State":
        return State(
            {atom.match(old_item=old_item, callback=callback) for atom in self}
        )


class SetOfStates(frozenset[State]):
    """
    A frozen set of states.
    """

    def __new__(cls, __iterable: Optional[Iterable[State]] = None, /) -> "SetOfStates":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().copy())

    def difference(self, *s: Iterable[object]) -> "SetOfStates":
        return SetOfStates(super().difference(*s))

    def intersection(
        self, *s: Iterable[object]
    ) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().intersection(*s))

    def symmetric_difference(
        self, __s: Iterable[State]
    ) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().symmetric_difference(__s))

    def union(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, *s: Iterable[State]
    ) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().union(*s))

    def __and__(
        self, __value: AbstractSet[State]
    ) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().__and__(__value))

    def __or__(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, __value: AbstractSet[State]
    ) -> "SetOfStates":
        return SetOfStates(super().__or__(__value))

    def __sub__(
        self, __value: AbstractSet[State]
    ) -> "SetOfStates":  # pragma: not covered
        return SetOfStates(super().__sub__(__value))

    def __xor__(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, __value: AbstractSet[State]
    ) -> "SetOfStates":  # pragma: not covered
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
        Definition 4.14 Product of set of states, p151

        NOTE: This is also produced from definition 4.27, p157, if you combine lines
            1 and 2.

        Γ ⨂ Δ = {γ∪δ : γ ∈ Γ, δ ∈ Δ}
        """
        return SetOfStates({state1 | state2 for state1 in self for state2 in other})

    def negation(self):
        """
        Based on Definition 4.31, p159

        Negation of set of states

        [Γ]ᶰ = ⭙_γ∈Γ {{p̄} : p ∈ γ}
        """
        output = None
        for s in self:
            new_state_set_mut: set[State] = set()
            for atom in s:
                # {p̄}
                new_state = State({~atom})
                new_state_set_mut.add(new_state)
            # {{p̄} : p ∈ γ}
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
        terms = ",".join([repr(i) for i in self.sorted_iter()])
        return "{" + terms + "}"

    @property
    def detailed(self) -> str:
        return "{" + ",".join(i.detailed for i in self.sorted_iter()) + "}"

    def _replace_arbs(self, replacements: dict[ArbitraryObject, Term]) -> "SetOfStates":
        """
        Replaces a series of arbitrary objects with terms and makes a new set of states.

        Args:
            replacements (dict[ArbitraryObject, Term]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            SetOfStates: The new set of states.
        """
        return SetOfStates([s._replace_arbs(replacements) for s in self])

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

    @property
    def predicate_atoms(self) -> set[PredicateAtom]:
        all_atoms = self.atoms
        p_atoms: set[PredicateAtom] = set()
        for a in all_atoms:
            if isinstance(a, DoAtom):
                p_atoms |= a.atoms
            else:
                assert isinstance(a, PredicateAtom)
                p_atoms.add(a)
        return p_atoms

    def sorted_iter(self):
        return sorted(self, key=str)

    def match(self, old_item: "MatchItem", callback: "MatchCallback") -> "SetOfStates":
        return SetOfStates(
            {state.match(old_item=old_item, callback=callback) for state in self}
        )


Stage = SetOfStates
Supposition = SetOfStates
