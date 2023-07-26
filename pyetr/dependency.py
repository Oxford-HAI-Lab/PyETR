__all__ = ["Dependency", "DependencyRelation"]

from typing import Iterable

from .stateset import set_of_states
from .term import ArbitraryObject

Universal = ArbitraryObject
Existential = ArbitraryObject


class Dependency:
    universal: Universal
    existential: Existential

    def __init__(self, universal: Universal, existential: Existential) -> None:
        """
        Dependency specifying a universal and the existentials that depend on it.

        Args:
            universal (Universal): The universal in question.
            existentials (frozenset[Existential]): The existentials depending on the universal.
        """
        # TODO: Overhaul dependency to be in pairwise structure
        self.universal = universal
        self.existential = existential

    def __repr__(self) -> str:
        return (
            f"<Dependency universal={self.universal} existentials={self.existential}>"
        )


def _separate_arb_objects(
    arb_objects: set[ArbitraryObject],
) -> tuple[set[Universal], set[Existential]]:
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
        self.dependencies = dependencies
        self._test_matroyshka()

    def _test_matroyshka(self):
        existentials: list[frozenset[ArbitraryObject]] = [
            frozenset(e) for _, e in self.to_sets()
        ]
        stack = existentials.copy()
        while stack:
            set1 = stack.pop(0)
            for set2 in stack:
                if not set1.issubset(set2) or set2.issubset(set1):
                    raise ValueError(
                        f"Existential sets do not meet Matroyshka condition. \nSet1: {set1}\nSet2: {set2}"
                    )

    def validate(self, states: set_of_states):
        uni_arb_objects, exi_arb_objects = _separate_arb_objects(states.arb_objects)
        # universal to existentials that depend on them ( share a pair )
        s = self.to_sets()
        for universal, existentials in s:
            if not existentials.issubset(exi_arb_objects):
                raise ValueError(
                    f"{existentials} not found in existential states {exi_arb_objects}"
                )
            if universal not in uni_arb_objects:
                raise ValueError(
                    f"{universal } not found in universal states {uni_arb_objects}"
                )

    def __repr__(self) -> str:
        if len(self.dependencies) == 0:
            full_string = ""
        else:
            full_string = " dependencies=" + "\n".join(
                [dep.__repr__() for dep in self.dependencies]
            )
        return f"<DependencyRelation{full_string}>"

    @classmethod
    def from_sets(cls, sets: Iterable[tuple[Universal, Iterable[Existential]]]):
        new_deps = set()
        for uni, exi_set in sets:
            for exi in exi_set:
                new_deps.add(Dependency(uni, exi))
        return cls(dependencies=frozenset(new_deps))

    def to_sets(self) -> set[tuple[Universal, set[Existential]]]:
        new_sets: dict[str, tuple[Universal, set[Existential]]] = {}
        for d in self.dependencies:
            if d.universal.name in new_sets:
                new_sets[d.universal.name][1].add(d.existential)
        return set(new_sets.values())

    # @property
    # def arb_objects(self) -> set[ArbitraryObject]:
    #     arb_objs = set()
    #     for dep in self.dependencies:
    #         if dep.universal not in arb_objs:
    #             arb_objs.add(dep.universal)
    #         for existential in dep.existentials:
    #             if existential not in arb_objs:
    #                 arb_objs.add(existential)
    #     return arb_objs

    def restriction(self, set_of_states: set_of_states) -> "DependencyRelation":
        """
        Based on definition 4.24
        """
        arb_objects = set_of_states.arb_objects

        new_deps = []
        for dep in self.dependencies:
            # If the state arb objects contain the dep universal
            rel_deps = [a for a in arb_objects if dep.universal.identical(a)]
            if len(rel_deps) > 0:
                for arb_object in arb_objects:
                    if not dep.existential.identical(arb_object):
                        new_deps.append(Dependency(dep.universal, dep.existential))

        return DependencyRelation(frozenset(new_deps))


class DependencyStructure:
    universals: set[Universal]
    existentials: set[Existential]
    dependency_pairs: frozenset[tuple[Universal, Existential]]
    dependency_relation: DependencyRelation

    def __init__(
        self,
        universals: set[Universal],
        existentials: set[Existential],
        dependency_relation: DependencyRelation,
    ) -> None:
        self.universals = universals
        self.existentials = existentials
        self.dependency_relation = dependency_relation
        # TODO: validation that the two sets are supersets of the dependency relation

    def fusion(self, other: "DependencyStructure") -> "DependencyStructure":
        raise NotImplementedError
