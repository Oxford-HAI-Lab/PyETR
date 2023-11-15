from typing import Optional

from pyetr.atoms.terms.special_funcs import multiset_product

from .atoms.terms import ArbitraryObject, Multiset, Term
from .dependency import DependencyRelation
from .stateset import SetOfStates, State


class Weight:
    multiplicative: Multiset[Term]
    additive: Multiset[Term]

    def __init__(
        self,
        multiplicative: Optional[Multiset[Term]] = None,
        additive: Optional[Multiset[Term]] = None,
    ) -> None:
        if multiplicative is None:
            multiplicative = Multiset[Term]([])
        if additive is None:
            additive = Multiset[Term]([])

        self.multiplicative = multiplicative
        self.additive = additive

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Weight):
            return False
        return (self.multiplicative == other.multiplicative) and (
            self.additive == other.additive
        )

    def __hash__(self) -> int:
        return hash((self.multiplicative, self.additive))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        """
        The arbitrary objects in the set of states

        Returns:
            set[ArbitraryObject]: The set of arbitrary objects
        """
        arbs = set()
        for multiset in self.multiplicative + self.additive:
            arbs |= multiset.arb_objects
        return arbs

    def __add__(self, other: "Weight") -> "Weight":
        return Weight(
            multiplicative=self.multiplicative + other.multiplicative,
            additive=self.additive + other.additive,
        )

    def __mul__(self, other: "Weight") -> "Weight":
        v_cross_w = multiset_product(self.multiplicative, other.multiplicative)
        return Weight(multiplicative=v_cross_w, additive=self.additive + other.additive)

    def __repr__(self) -> str:
        if len(self.multiplicative) == 0:
            multi_str = ""
        else:
            multi_str = f"{self.multiplicative}×."
        if len(self.additive) == 0:
            add_str = ""
        else:
            add_str = f"{self.additive}+."
        return f"{multi_str}{add_str}"

    @property
    def detailed(self):
        return f"<Weight multi={self.multiplicative.detailed} add={self.additive.detailed}>"

    def validate_against_dep_rel(self, dependency_relation: DependencyRelation):
        if not self.arb_objects.issubset(
            dependency_relation.universals | dependency_relation.existentials
        ):
            raise ValueError(
                "Arb objects in weights not present in dependency relation"
            )

    def restriction(self, arb_objects: set[ArbitraryObject]) -> "Weight":
        return Weight(
            multiplicative=Multiset(
                [t for t in self.multiplicative if t.arb_objects.issubset(arb_objects)]
            ),
            additive=Multiset(
                [t for t in self.additive if t.arb_objects.issubset(arb_objects)]
            ),
        )

    @property
    def is_null(self) -> bool:
        """
        Return true if the weight is empty

        Returns:
            bool: True if the weight is empty.
        """
        return len(self.multiplicative) == 0 and len(self.additive) == 0

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "Weight":
        """
        Replaces a series of arbitrary objects with terms and makes a new weight.
        Args:
            replacements (dict[ArbitraryObject, Term]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            Weight: The new weight
        """
        return Weight(
            multiplicative=Multiset(
                [i.replace(replacements) for i in self.multiplicative]
            ),
            additive=Multiset([i.replace(replacements) for i in self.additive]),
        )

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> "Weight":
        return Weight(
            multiplicative=Multiset[Term](
                [i.replace_term(old_term, new_term) for i in self.multiplicative]
            ),
            additive=Multiset[Term](
                [i.replace_term(old_term, new_term) for i in self.additive]
            ),
        )


class Weights:
    _weights: dict[State, Weight]

    def __init__(self, weights_dict: Optional[dict[State, Weight]] = None) -> None:
        if weights_dict is None:
            weights_dict = {}
        self._weights = weights_dict

    def __iter__(self):
        return iter(self._weights)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Weights):
            return False
        return self._weights == other._weights

    def __hash__(self) -> int:
        return hash(tuple([(k, v) for k, v in self._weights.items()]))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        """
        The arbitrary objects in the set of states

        Returns:
            set[ArbitraryObject]: The set of arbitrary objects
        """
        arbs = set()
        for weight in self.values():
            arbs |= weight.arb_objects
        return arbs

    def __add__(self, other: "Weights") -> "Weights":
        new_weights: dict[State, Weight] = {}
        for k, x in self._weights.items():
            if k not in other._weights:
                new_weights[k] = x
            else:
                new_weights[k] = x + other._weights[k]

        for k, x in other._weights.items():
            if k not in new_weights:
                new_weights[k] = x
        return Weights(new_weights)

    @property
    def detailed(self):
        weight_details = {s.detailed: w.detailed for s, w in self._weights.items()}
        return f"<Weights {weight_details}>"

    def __getitem__(self, item: State):
        if item not in self._weights:
            raise ValueError(f"{self} and {item}")
        return self._weights[item]

    def _adding(self, state: State, weight: Weight):
        if state in self:
            self._weights[state] += weight
        else:
            self._weights[state] = weight

    def items(self):
        return self._weights.items()

    def values(self):
        return self._weights.values()

    def keys(self):
        return self._weights.keys()

    def __contains__(self, item: object) -> bool:
        return item in self._weights

    def __mul__(self, other: "Weights") -> "Weights":
        new_weights: Weights = Weights()
        for state1, weight1 in self._weights.items():
            for state2, weight2 in other._weights.items():
                new_weights._adding(state1 | state2, weight1 * weight2)
        return new_weights

    @classmethod
    def get_null_weights(cls, states: SetOfStates) -> "Weights":
        """
        Get the null weights for the states provided

        Args:
            states (SetOfStates): The set of states

        Returns:
            Weights: The null weights associated
        """
        return cls({state: Weight() for state in states})

    def in_set_of_states(self, set_of_states: SetOfStates) -> "Weights":
        """
        The subset of the weights that reflects the states in the set of
        states provided

        Args:
            set_of_states (SetOfStates): The set of states to get the weights
                for.

        Returns:
            Weights: The new subset weights.
        """
        assert set_of_states.issubset(SetOfStates(self.keys()))
        return Weights({k: v for k, v in self.items() if k in set_of_states})

    def __repr__(self) -> str:
        return "{" + ",".join([f"{w}{s}" for s, w in self.items()]) + "}"
