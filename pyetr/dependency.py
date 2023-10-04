__all__ = ["Dependency", "DependencyRelation"]

from typing import Iterable

from .atoms.terms import ArbitraryObject
from .stateset import SetOfStates

Universal = ArbitraryObject
Existential = ArbitraryObject


class Dependency:
    existential: Existential
    universal: Universal

    def __init__(self, *, existential: Existential, universal: Universal) -> None:
        """
        Dependency specifying a universal and the existentials that depend on it.

        Args:
            universal (Universal): The universal in question.
            existential (Existential): The existential depending on the universal.
        """
        self.existential = existential
        self.universal = universal

    def __repr__(self) -> str:
        return f"<Dependency existential={self.existential} universal={self.universal}>"

    @property
    def detailed(self) -> "str":
        return repr(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dependency):
            return False
        return (
            self.existential == other.existential and self.universal == other.universal
        )

    def __hash__(self) -> int:
        return hash((self.existential, self.universal))

    def replace(
        self, replacements: dict[ArbitraryObject, ArbitraryObject]
    ) -> "Dependency":
        if self.existential in replacements:
            new_exi = replacements[self.existential]
        else:
            new_exi = self.existential
        if self.universal in replacements:
            new_uni = replacements[self.universal]
        else:
            new_uni = self.universal
        return Dependency(universal=new_uni, existential=new_exi)


def transitive_closure(
    D_initial: list[tuple[ArbitraryObject, ArbitraryObject]],
    arb_objects: set[ArbitraryObject],
) -> list[tuple[ArbitraryObject, ArbitraryObject]]:
    def D_next(
        D: list[tuple[ArbitraryObject, ArbitraryObject]]
    ) -> list[tuple[ArbitraryObject, ArbitraryObject]]:
        D_i_plus_1: list[tuple[ArbitraryObject, ArbitraryObject]] = []
        for x, y in D:
            for z in arb_objects:
                if (y, z) in D_initial:
                    D_i_plus_1.append((x, z))
        return D_i_plus_1 + D

    d_current: list[tuple[ArbitraryObject, ArbitraryObject]] = D_initial
    while True:
        D_next_set = D_next(d_current)
        if set(D_next_set) == set(d_current):
            break
        d_current = D_next_set

    return d_current


def dependency_exists(
    universal: Universal, existential: Existential, dependencies: frozenset[Dependency]
) -> bool:
    for dep in dependencies:
        if dep.universal == universal and dep.existential == existential:
            return True
    return False


def dependencies_from_sets(
    sets: Iterable[tuple[Universal, Iterable[Existential]]]
) -> frozenset[Dependency]:
    new_deps = set()
    for uni, exi_set in sets:
        for exi in exi_set:
            new_deps.add(Dependency(existential=exi, universal=uni))
    return frozenset(new_deps)


def dependencies_to_sets(
    dependencies: frozenset[Dependency],
) -> list[tuple[Universal, set[Existential]]]:
    new_sets: dict[str, tuple[Universal, set[Existential]]] = {}
    for d in dependencies:
        if d.universal.name in new_sets:
            new_sets[d.universal.name][1].add(d.existential)
        else:
            new_sets[d.universal.name] = (d.universal, {d.existential})
    return list(new_sets.values())


class DependencyRelation:
    universals: set[Universal]
    existentials: set[Existential]
    dependencies: frozenset[Dependency]

    def __init__(
        self,
        universals: set[Universal],
        existentials: set[Existential],
        dependencies: frozenset[Dependency],
    ) -> None:
        self.universals = universals
        self.existentials = existentials
        self.dependencies = dependencies
        self.validate()
        self._test_matroyshka()

    def _test_matroyshka(self):
        existentials: list[frozenset[ArbitraryObject]] = [
            frozenset(e) for _, e in dependencies_to_sets(self.dependencies)
        ]
        stack = existentials.copy()
        while stack:
            set1 = stack.pop(0)
            for set2 in stack:
                if not (set1.issubset(set2) or set2.issubset(set1)):
                    raise ValueError(
                        f"Existential sets do not meet Matroyshka condition. \nSet1: {set1}\nSet2: {set2}"
                    )

    def is_existential(self, arb_object: ArbitraryObject) -> bool:
        if arb_object in self.existentials:
            return True
        elif arb_object in self.universals:
            return False
        else:
            raise ValueError(
                f"Arb object {arb_object} not found in dependency relation"
            )

    def validate_against_states(
        self, arb_objects: set[ArbitraryObject], pre_view: bool = False
    ):
        if pre_view:
            if not (self.universals | self.existentials).issuperset(arb_objects):
                raise ValueError(
                    f"Universals with existentials: {self.universals | self.existentials} not superset of states {arb_objects}"
                )
        else:
            if arb_objects != self.universals | self.existentials:
                raise ValueError(
                    f"Universals with existentials: {self.universals | self.existentials} not the same as states {arb_objects}"
                )

    @property
    def dependency_arb_objects(self) -> set[ArbitraryObject]:
        arb_objs = set()
        for dep in self.dependencies:
            if dep.universal not in arb_objs:
                arb_objs.add(dep.universal)
            if dep.existential not in arb_objs:
                arb_objs.add(dep.existential)
        return arb_objs

    def validate(self):
        if not (self.universals | self.existentials).issuperset(
            self.dependency_arb_objects
        ):
            raise ValueError(
                f"Existentials {self.universals | self.existentials} is not superset of dependency arb objects {self.dependency_arb_objects}"
            )

    def chain(self, other: "DependencyRelation") -> "DependencyRelation":
        universals = self.universals | other.universals
        existentials = self.existentials | other.existentials

        new_deps: set[Dependency] = set()
        for existential in other.existentials:
            for universal in self.universals:
                new_deps.add(Dependency(universal=universal, existential=existential))

        return DependencyRelation(
            universals, existentials, self.dependencies | other.dependencies | new_deps
        )

    def restriction(self, arb_objects: set[ArbitraryObject]) -> "DependencyRelation":
        """
        Based on definition 4.24
        """
        universals = self.universals & arb_objects
        existentials = self.existentials & arb_objects
        new_deps = [
            dep
            for dep in self.dependencies
            if dep.universal in arb_objects and dep.existential in arb_objects
        ]
        return DependencyRelation(
            universals, existentials, dependencies=frozenset(new_deps)
        )

    def get_all_dep_partners_for_arb_obj(
        self, arb_obj: ArbitraryObject
    ) -> set[ArbitraryObject]:
        out: set[ArbitraryObject] = set()
        if self.is_existential(arb_obj):
            for dep in self.dependencies:
                if dep.existential == arb_obj:
                    out.add(dep.universal)
        else:
            for dep in self.dependencies:
                if dep.universal == arb_obj:
                    out.add(dep.existential)
        return out

    def triangle(
        self, arb_object1: ArbitraryObject, arb_object2: ArbitraryObject
    ) -> bool:
        arb_obj1_found = False
        arb_obj2_found = False
        for arb_obj in self.universals | self.existentials:
            if arb_obj == arb_object1:
                arb_obj1_found = True
            if arb_obj == arb_object2:
                arb_obj2_found = True
        if not arb_obj1_found or not arb_obj2_found:
            return False

        if self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 1
            # There is X that E (arb_obj1) depends on and that e prime (arb_obj2) does not depend on
            unis_e_depends_on = self.get_all_dep_partners_for_arb_obj(arb_object1)
            unis_e_prime_depends_on = self.get_all_dep_partners_for_arb_obj(arb_object2)
            return len(unis_e_depends_on.difference(unis_e_prime_depends_on)) != 0
        elif self.is_existential(arb_object1) and not self.is_existential(arb_object2):
            # Case 2
            # There is a dependency of this structure
            return dependency_exists(
                universal=arb_object2,
                existential=arb_object1,
                dependencies=self.dependencies,
            )

        elif not self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 3
            # There is not a dependency of this structure
            return not dependency_exists(
                universal=arb_object1,
                existential=arb_object2,
                dependencies=self.dependencies,
            )

        elif not self.is_existential(arb_object1) and not self.is_existential(
            arb_object2
        ):
            # Case 4
            # There is X that does depend on u prime (arb_obj2) and does not depend on u (arb_obj 1)
            exis_depending_on_u = self.get_all_dep_partners_for_arb_obj(arb_object1)
            exis_depending_on_u_prime = self.get_all_dep_partners_for_arb_obj(
                arb_object2
            )
            return len(exis_depending_on_u_prime.difference(exis_depending_on_u)) != 0
        else:
            assert False

    def less_sim(
        self, arb_object1: ArbitraryObject, arb_object2: ArbitraryObject
    ) -> bool:
        arb_obj1_found = False
        arb_obj2_found = False
        for arb_obj in self.universals | self.existentials:
            if arb_obj == arb_object1:
                arb_obj1_found = True
            if arb_obj == arb_object2:
                arb_obj2_found = True
        if not arb_obj1_found or not arb_obj2_found:
            return False

        if self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 1
            # not(There is an X that E prime (arb_obj2) deps on and that e (arb_obj1)does not depend upon)
            unis_e_depends_on = self.get_all_dep_partners_for_arb_obj(arb_object1)
            unis_e_prime_depends_on = self.get_all_dep_partners_for_arb_obj(arb_object2)
            return len(unis_e_prime_depends_on.difference(unis_e_depends_on)) == 0

        elif self.is_existential(arb_object1) and not self.is_existential(arb_object2):
            # Case 2
            # There is a dependency of this structure
            return dependency_exists(
                universal=arb_object2,
                existential=arb_object1,
                dependencies=self.dependencies,
            )

        elif not self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 3
            # There is not a dependency of this structure
            return not dependency_exists(
                universal=arb_object1,
                existential=arb_object2,
                dependencies=self.dependencies,
            )

        elif not self.is_existential(arb_object1) and not self.is_existential(
            arb_object2
        ):
            # Case 4
            # not(There is an X that depends on u (arb_obj 1) but does not depend on u_prime (arb_obj2))
            exis_depending_on_u = self.get_all_dep_partners_for_arb_obj(arb_object1)
            exis_depending_on_u_prime = self.get_all_dep_partners_for_arb_obj(
                arb_object2
            )
            return len(exis_depending_on_u.difference(exis_depending_on_u_prime)) == 0
        else:
            assert False

    def E0(
        self,
        other: "DependencyRelation",
        new_pairs: list[tuple[ArbitraryObject, ArbitraryObject]],
    ) -> set[Existential]:
        new_out: list[ArbitraryObject] = []
        for e in self.existentials | other.existentials:
            pair_found = False
            for u in self.universals | other.universals:
                if (e, u) in new_pairs:
                    pair_found = True
                    break
            if not pair_found:
                new_out.append(e)
        return set(new_out)

    def U0(
        self,
        other: "DependencyRelation",
        new_pairs: list[tuple[ArbitraryObject, ArbitraryObject]],
        e_0: set[Existential],
    ) -> set[Universal]:
        new_out: list[ArbitraryObject] = []
        for u in self.universals | other.universals:
            pair_found = False
            for e in (self.existentials | other.existentials).difference(e_0):
                if (u, e) in new_pairs and (e, u) not in new_pairs:
                    pair_found = True
                    break
            if not pair_found:
                new_out.append(u)
        return set(new_out)

    @property
    def is_empty(self):
        if len(self.universals) == 0 and len(self.existentials) == 0:
            assert len(self.dependencies) == 0
            return True
        else:
            return False

    def fusion(self, other: "DependencyRelation") -> "DependencyRelation":
        if self.is_empty and other.is_empty:
            return self
        else:
            pairs: list[tuple[ArbitraryObject, ArbitraryObject]] = []
            arb_objects = (
                self.existentials
                | other.existentials
                | self.universals
                | other.universals
            )
            for x in arb_objects:
                for y in arb_objects:
                    if self.triangle(x, y) or other.triangle(x, y):
                        pairs.append((x, y))
            new_pairs = transitive_closure(pairs, arb_objects)

            e_0 = self.E0(other, new_pairs)
            u_0 = self.U0(other, new_pairs, e_0)

            initial_relation = DependencyRelation(u_0, e_0, frozenset())
            a_r = self.universals | self.existentials
            a_s = other.universals | other.existentials
            return initial_relation.chain(
                self.restriction(a_r.difference(e_0 | u_0)).fusion(
                    other.restriction(a_s.difference(e_0 | u_0))
                )
            )

    def __repr__(self) -> str:
        if len(self.dependencies) == 0:
            return "None"
        else:
            return "".join(
                f"{u}" + "{" + ",".join(repr(e) for e in exis) + "}"
                for u, exis in dependencies_to_sets(self.dependencies)
            )

    @property
    def detailed(self):
        return f"<DependencyRelation deps={[i.detailed for i in self.dependencies]} unis={self.universals} exis={self.existentials}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, DependencyRelation):
            return False
        return (
            self.dependencies == other.dependencies
            and self.universals == other.universals
            and self.existentials == other.existentials
        )

    def __hash__(self) -> int:
        return hash((self.universals, self.existentials, self.dependencies))

    def replace(
        self, replacements: dict[ArbitraryObject, ArbitraryObject]
    ) -> "DependencyRelation":
        def replace_arb_object(x: ArbitraryObject) -> ArbitraryObject:
            if x in replacements:
                return replacements[x]
            else:
                return x

        new_unis = {replace_arb_object(x) for x in self.universals}
        new_exis = {replace_arb_object(x) for x in self.existentials}
        new_deps = {d.replace(replacements) for d in self.dependencies}
        return DependencyRelation(new_unis, new_exis, frozenset(new_deps))

    def negation(self) -> "DependencyRelation":
        """
        Based on 4.31, Negation of a dependency relation
        """
        # Every new existential now depends on every new universal
        # Except those that the ancestor existential depended on the ancestor universal

        new_deps: list[Dependency] = []
        for exi in self.existentials:
            for uni in self.universals:
                ancestor_dep = Dependency(existential=exi, universal=uni)
                if ancestor_dep not in self.dependencies:
                    new_dep = Dependency(existential=uni, universal=exi)
                    new_deps.append(new_dep)

        return DependencyRelation(
            universals=self.existentials,
            existentials=self.universals,
            dependencies=frozenset(new_deps),
        )
