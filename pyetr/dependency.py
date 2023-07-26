__all__ = ["Dependency", "DependencyRelation"]

from .stateset import set_of_states
from .term import ArbitraryObject

Universal = ArbitraryObject
Existential = ArbitraryObject


class Dependency:
    universal: Universal
    existentials: frozenset[Existential]

    def __init__(
        self, universal: Universal, existentials: frozenset[Existential]
    ) -> None:
        """
        Dependency specifying a universal and the existentials that depend on it.

        Args:
            universal (Universal): The universal in question.
            existentials (frozenset[Existential]): The existentials depending on the universal.
        """
        # TODO: Overhaul dependency to be in pairwise structure
        self.universal = universal
        self.existentials = existentials

    def __repr__(self) -> str:
        return (
            f"<Dependency universal={self.universal} existentials={self.existentials}>"
        )

    def pairs(self) -> set[tuple[Universal, Existential]]:
        new_set = set()
        for existential in self.existentials:
            new_set.add((self.universal, existential))
        return new_set


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

    def pairs(self) -> set[tuple[Universal, Existential]]:
        new_set: set[tuple[Universal, Existential]] = set()
        for dep in self.dependencies:
            new_set |= dep.pairs()
        return new_set

    @classmethod
    def from_pairs(cls, pairs: set[tuple[Universal, Existential]]):
        universal_deps: dict[str, tuple[Universal, set[Existential]]] = {}
        for uni, exi in pairs:
            if uni.name not in universal_deps:
                universal_deps[uni.name] = (uni, {exi})
            else:
                universal_deps[uni.name][1].add(exi)
        return cls(
            frozenset(
                [
                    Dependency(uni, frozenset(exi_set))
                    for uni, exi_set in universal_deps.values()
                ]
            )
        )

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
            if not [dep.universal.identical(a) for a in arb_objects]:
                new_exis = set()
                for exi in dep.existentials:
                    for arb_object in arb_objects:
                        if not exi.identical(arb_object):
                            new_exis.add(exi)
                if len(new_exis) == 0:
                    pass
                else:
                    new_deps.append(Dependency(dep.universal, frozenset(new_exis)))

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
        self.dependency_pairs = frozenset(dependency_relation.pairs())
        self.dependency_relation = dependency_relation
        # TODO: validation that the two sets are supersets of the dependency relation

    def fusion(self, other: "DependencyStructure") -> "DependencyStructure":
        raise NotImplementedError
