__all__ = ["Dependency", "DependencyRelation"]

from .stateset import set_of_states
from .term import ArbitraryObject


class Dependency:
    universal: ArbitraryObject
    existentials: frozenset[ArbitraryObject]

    def __init__(
        self, universal: ArbitraryObject, existentials: frozenset[ArbitraryObject]
    ) -> None:
        """
        Dependency specifying a universal and the existentials that depend on it.

        Args:
            universal (ArbitraryObject): The universal in question.
            existentials (frozenset[ArbitraryObject]): The existentials depending on the universal.
        """
        self.universal = universal
        self.existentials = existentials

    def __repr__(self) -> str:
        return (
            f"<Dependency universal={self.universal} existentials={self.existentials}>"
        )


def _test_matroyshka(deps: frozenset[Dependency]):
    existentials: list[frozenset[ArbitraryObject]] = [d.existentials for d in deps]
    stack = existentials.copy()
    while stack:
        set1 = stack.pop(0)
        for set2 in stack:
            if not set1.issubset(set2) or set2.issubset(set1):
                raise ValueError(
                    f"Existential sets do not meet Matroyshka condition. \nSet1: {set1}\nSet2: {set2}"
                )


UniArbObjects = set[ArbitraryObject]
ExiArbObjects = set[ArbitraryObject]


def _separate_arb_objects(
    arb_objects: set[ArbitraryObject],
) -> tuple[UniArbObjects, ExiArbObjects]:
    uni_objs = set()
    exi_objs = set()
    for obj in arb_objects:
        if obj.is_existential:
            exi_objs.add(obj)
        else:
            uni_objs.add(obj)
    return uni_objs, exi_objs


class DependencyRelation:
    dependencies: frozenset[Dependency]

    def __init__(self, dependencies: frozenset[Dependency]) -> None:
        _test_matroyshka(dependencies)
        self.dependencies = dependencies

    def validate(self, states: set_of_states):
        uni_arb_objects, exi_arb_objects = _separate_arb_objects(states.arb_objects)
        # universal to existentials that depend on them ( share a pair )
        for d in self.dependencies:
            if not d.existentials.issubset(exi_arb_objects):
                raise ValueError(
                    f"{d.existentials} not found in existential states {exi_arb_objects}"
                )
            if d.universal not in uni_arb_objects:
                raise ValueError(
                    f"{d.universal } not found in universal states {uni_arb_objects}"
                )

    def __repr__(self) -> str:
        if len(self.dependencies) == 0:
            full_string = ""
        else:
            full_string = " dependencies=" + "\n".join(
                [dep.__repr__() for dep in self.dependencies]
            )
        return f"<DependencyRelation{full_string}>"
