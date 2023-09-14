from pyetr.dependency import DependencyRelation
from pyetr.function import XBar
from pyetr.multiset import Multiset
from pyetr.term import FunctionalTerm, Term


class Weight:
    multiplicative: Multiset[Term]
    additive: Multiset[Term]

    def __init__(
        self, multiplicative: Multiset[Term], additive: Multiset[Term]
    ) -> None:
        self.multiplicative = multiplicative
        self.additive = additive

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
            v_cross_w = Multiset[Term](
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
        return None
        raise NotImplementedError
