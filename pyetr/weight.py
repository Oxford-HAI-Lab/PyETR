from pyetr.dependency import DependencyRelation
from pyetr.special_funcs import XBar
from pyetr.stateset import SetOfStates, State
from pyetr.term import ArbitraryObject, FunctionalTerm, Multiset, Term


class Weight:
    multiplicative: Multiset
    additive: Multiset

    def __init__(self, multiplicative: Multiset, additive: Multiset) -> None:
        self.multiplicative = multiplicative
        self.additive = additive

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
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
        if len(self.multiplicative) == 0:
            v_cross_w = other.multiplicative
        elif len(other.multiplicative) == 0:
            v_cross_w = self.multiplicative
        else:
            v_cross_w = Multiset(
                [
                    FunctionalTerm(f=XBar, t=(s_i, t_j))
                    for s_i in self.multiplicative
                    for t_j in other.multiplicative
                ]
            )
        return Weight(multiplicative=v_cross_w, additive=self.additive + other.additive)

    def __repr__(self) -> str:
        return f"{self.multiplicative}×.{self.additive}+"

    @property
    def detailed(self):
        return f"<Weight multi={self.multiplicative.detailed} add={self.additive.detailed}>"

    @classmethod
    def get_null_weight(cls):
        return cls(multiplicative=Multiset([]), additive=Multiset([]))

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
    def is_null(self):
        return len(self.multiplicative) == 0 and len(self.additive) == 0

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "Weight":
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
            multiplicative=self.multiplicative.replace_term(
                old_term, new_term
            ),  # type:ignore
            additive=self.additive.replace_term(old_term, new_term),  # type:ignore
        )


class Weights:
    _weights: dict[State, Weight]

    def __init__(self, weights_dict: dict[State, Weight]) -> None:
        self._weights = weights_dict

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
        return self._weights[item]

    def items(self):
        return self._weights.items()

    def values(self):
        return self._weights.values()

    def keys(self):
        return self._weights.keys()

    def __contains__(self, item: object) -> bool:
        return item in self._weights

    def __mul__(self, other: "Weights") -> "Weights":
        new_weights: dict[State, Weight] = {}
        for state1, weight1 in self._weights.items():
            for state2, weight2 in other._weights.items():
                new_state = state1 | state2
                new_weight = weight1 * weight2
                if new_state in new_weights:
                    new_weights[new_state] += new_weight
                else:
                    new_weights[new_state] = new_weight
        return Weights(new_weights)

    @classmethod
    def get_null_weights(cls, states: SetOfStates) -> "Weights":
        return cls({state: Weight.get_null_weight() for state in states})

    def in_set_of_states(self, set_of_states: SetOfStates) -> "Weights":
        return Weights({k: v for k, v in self.items() if k in set_of_states})

    def __repr__(self) -> str:
        return "{" + ",".join([f"{w}.{s}" for s, w in self.items()]) + "}"
