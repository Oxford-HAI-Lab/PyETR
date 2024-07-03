__all__ = ["Dependency", "DependencyRelation"]

from typing import Iterable

from .atoms.terms import ArbitraryObject

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
        """
        Replaces one arbitrary object found in the dependency with another from a mapping.

        Args:
            replacements (dict[ArbitraryObject, ArbitraryObject]): Mapping of replacements.

        Returns:
            Dependency: The dependency with replacements made.
        """
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
    D_initial: set[tuple[ArbitraryObject, ArbitraryObject]],
    arb_objects: frozenset[ArbitraryObject],
) -> set[tuple[ArbitraryObject, ArbitraryObject]]:
    d_current = D_initial

    while True:
        D_next_set = {
            (x, z) for x, y in d_current for z in arb_objects if (y, z) in d_current
        }
        D_next_set |= d_current
        if D_next_set == d_current:
            return d_current
        d_current = D_next_set


def dependencies_from_sets(
    sets: Iterable[tuple[Universal, Iterable[Existential]]]
) -> frozenset[Dependency]:
    """
    Converts existential set form dependencies to standard form.

    Args:
        sets (Iterable[tuple[Universal, Iterable[Existential]]]): Existential set form dependencies

    Returns:
        frozenset[Dependency]: Standard form dependencies
    """
    new_deps: set[Dependency] = set()
    for uni, exi_set in sets:
        for exi in exi_set:
            new_deps.add(Dependency(existential=exi, universal=uni))
    return frozenset(new_deps)


def dependencies_to_sets(
    dependencies: frozenset[Dependency],
) -> list[tuple[Universal, set[Existential]]]:
    """
    Converts dependencies to collected by existential set form.

    Args:
        dependencies (frozenset[Dependency]): The input dependencies

    Returns:
        list[tuple[Universal, set[Existential]]]: Dependencies in existential set form.
    """
    new_sets: dict[str, tuple[Universal, set[Existential]]] = {}
    for d in dependencies:
        if d.universal.name in new_sets:
            new_sets[d.universal.name][1].add(d.existential)
        else:
            new_sets[d.universal.name] = (d.universal, {d.existential})
    return list(new_sets.values())


def cross(
    *, existentials: frozenset[Existential], universals: frozenset[Universal]
) -> frozenset[Dependency]:
    """
    E × U
    Args:
        universals (frozenset[Universal]): U
        existentials (frozenset[Existential]): E

    Returns:
        frozenset[Dependency]: The dependency resulting from the cross.
    """
    return frozenset(
        {
            Dependency(existential=existential, universal=universal)
            for existential in existentials
            for universal in universals
        }
    )


class DependencyRelation:
    universals: frozenset[Universal]
    existentials: frozenset[Existential]
    dependencies: frozenset[Dependency]

    def __init__(
        self,
        universals: Iterable[Universal],
        existentials: Iterable[Existential],
        dependencies: Iterable[Dependency],
    ) -> None:
        """
        A dependency relation, containing information about the dependencies
        and the nature of the arbitrary objects.

        Args:
            universals (Iterable[Universal]): The set of universals.
            existentials (Iterable[Existential]): The set of existentials.
            dependencies (Iterable[Dependency]): The set of dependencies.
        """
        self.universals = frozenset(universals)
        self.existentials = frozenset(existentials)
        self.dependencies = frozenset(dependencies)
        self._validate()
        self._test_matryoshka()

    def _test_matryoshka(self):
        """
        Based on the Matryoshka condition, p141

        Raises:
            ValueError: Raised if the dependencies fail the Matryoshka condition.
        """
        existentials: list[frozenset[ArbitraryObject]] = [
            frozenset(e) for _, e in dependencies_to_sets(self.dependencies)
        ]
        stack = existentials.copy()
        while stack:
            set1 = stack.pop(0)
            for set2 in stack:
                if not (set1.issubset(set2) or set2.issubset(set1)):
                    raise ValueError(
                        f"Existential sets do not meet Matryoshka condition. \nSet1: {set1}\nSet2: {set2}"
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

    def __eq__(self, other: object) -> bool:
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
        """
        Replaces a series of arbitrary objects and makes a new dependency relation.

        Args:
            replacements (dict[ArbitraryObject, ArbitraryObject]): A dict of the replacements,
                where the keys are the existing values and the values are the new values.

        Returns:
            DependencyRelation: The new dependency relation.
        """

        def replace_arb_object(x: ArbitraryObject) -> ArbitraryObject:
            if x in replacements:
                return replacements[x]
            else:
                return x

        new_unis = {replace_arb_object(x) for x in self.universals}
        new_exis = {replace_arb_object(x) for x in self.existentials}
        new_deps = {d.replace(replacements) for d in self.dependencies}
        return DependencyRelation(new_unis, new_exis, frozenset(new_deps))

    def is_existential(self, arb_object: ArbitraryObject) -> bool:
        """
        Returns true if an arbitrary object given is existential, based on the
            dependency relation.

        Args:
            arb_object (ArbitraryObject): The arbitrary object to be determined.

        Raises:
            ValueError: The arbitrary object is not found in the dependency relation.

        Returns:
            bool: True if the arbitrary object is an existential.
        """
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
        """
        Validates the dependency against the provided arb_objects

        Args:
            arb_objects (set[ArbitraryObject]): The set of arbitrary provided
            pre_view (bool, optional): If the view under validation is a pre-view (Incomplete view, with
                lower restrictions on validation). Defaults to False.

        Raises:
            ValueError: The arbitrary objects contained in the dependency relation do not match the arb objects provided.
        """
        if pre_view:
            if not (self.universals | self.existentials).issuperset(arb_objects):
                raise ValueError(
                    f"Universals with existentials: {self.universals | self.existentials} not superset of those in stage/supposition {arb_objects}"
                )
        else:
            if frozenset(arb_objects) != self.universals | self.existentials:
                raise ValueError(
                    f"Universals with existentials: {self.universals | self.existentials} not the same as those in stage/supposition {arb_objects}"
                )

    def _validate(self):
        """
        Validates the dependency relation against itself, to ensure it's self consistent.

        Raises:
            ValueError: Invalid dependency relation.
        """
        dep_arb_objs: set[ArbitraryObject] = set()
        for dep in self.dependencies:
            if dep.universal not in dep_arb_objs:
                dep_arb_objs.add(dep.universal)
            if dep.existential not in dep_arb_objs:
                dep_arb_objs.add(dep.existential)

        if not (self.universals | self.existentials).issuperset(dep_arb_objs):
            raise ValueError(
                f"Existentials {self.universals | self.existentials} is not superset of dependency arb objects {dep_arb_objs}"
            )

    def restriction(self, arb_objects: set[ArbitraryObject]) -> "DependencyRelation":
        """
        Based on definition 4.24, p155

        [R]_X = <U_R ∩ X, E_R ∩ X, D_R ∩ ((E_R ∩ X) × (U_R ∩ X))
        Args:
            arb_objects (set[ArbitraryObject]): X

        Returns:
            DependencyRelation: The new dependency relation
        """
        # U_R ∩ X
        universals = self.universals & arb_objects
        # E_R ∩ X
        existentials = self.existentials & arb_objects
        # D_R ∩ ((E_R ∩ X) × (U_R ∩ X))
        new_deps = self.dependencies & cross(
            universals=universals, existentials=existentials
        )

        return DependencyRelation(universals, existentials, dependencies=new_deps)

    def related_universals(self, existential: Existential) -> set[Universal]:
        """
        Returns all universals related to an existential, by a dependency.

        Args:
            existential (Existential): The existential

        Returns:
            set[Universal]: The related universals.
        """
        assert self.is_existential(arb_object=existential)
        return {
            dep.universal for dep in self.dependencies if dep.existential == existential
        }

    def related_existentials(self, universal: Universal) -> set[Existential]:
        """
        Returns all existentials related to a universal, by a dependency.

        Args:
            universal (Universal): The universal

        Returns:
            set[Existential]: The related existentials.
        """
        assert not self.is_existential(arb_object=universal)
        return {
            dep.existential for dep in self.dependencies if dep.universal == universal
        }

    def triangle(
        self, arb_object1: ArbitraryObject, arb_object2: ArbitraryObject
    ) -> bool:
        """
        Based on Definition B.1.2, p315

        a ◁_R b

        Based on Lemma B.7
        (i) e ◁_R u iff <e,u> ∈ D_R
        (i) u ◁_R e iff ¬(e ◁_R u) iff ¬(<e,u> ∈ D_R)
        (ii), (b): u ◁_R u' iff ∃e ∈ E_R.<e,u> ∉ D_R ∧ <e,u'> ∈ D_R
        (iii), (b): e ◁_R e' iff ∃u ∈ U_R.<e',u> ∉ D_R ∧ <e,u> ∈ D_R
        Args:
            arb_object1 (ArbitraryObject): a
            arb_object2 (ArbitraryObject): b

        Returns:
            bool: The result of a ◁_R b
        """
        if (arb_object1 not in (self.universals | self.existentials)) or (
            arb_object2 not in (self.universals | self.existentials)
        ):
            return False

        if self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 1
            # B.7, (iii), (b): e ◁_R e' iff ∃u ∈ U_R.<e',u> ∉ D_R ∧ <e,u> ∈ D_R

            # There is X that E (arb_obj1) depends on and that e prime (arb_obj2) does not depend on
            unis_e_depends_on = self.related_universals(arb_object1)
            unis_e_prime_depends_on = self.related_universals(arb_object2)
            return len(unis_e_depends_on.difference(unis_e_prime_depends_on)) != 0
        elif self.is_existential(arb_object1) and not self.is_existential(arb_object2):
            # Case 2

            # (i) e ◁_R u iff <e,u> ∈ D_R
            # There is a dependency of this structure
            return (
                Dependency(existential=arb_object1, universal=arb_object2)
                in self.dependencies
            )

        elif not self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 3
            # (i) u ◁_R e iff ¬(e ◁_R u) iff ¬(<e,u> ∈ D_R)
            # There is not a dependency of this structure
            return (
                Dependency(existential=arb_object2, universal=arb_object1)
                not in self.dependencies
            )

        elif not self.is_existential(arb_object1) and not self.is_existential(
            arb_object2
        ):
            # Case 4
            # B.7, (ii), (b): u ◁_R u' iff ∃e ∈ E_R.<e,u> ∉ D_R ∧ <e,u'> ∈ D_R

            # There is X that does depend on u prime (arb_obj2) and does not depend on u (arb_obj 1)
            exis_depending_on_u = self.related_existentials(arb_object1)
            exis_depending_on_u_prime = self.related_existentials(arb_object2)
            return len(exis_depending_on_u_prime.difference(exis_depending_on_u)) != 0
        else:
            assert False

    def less_sim(
        self, arb_object1: ArbitraryObject, arb_object2: ArbitraryObject
    ) -> bool:
        """
        Based on Definition B.1.2, p315

        a ≲_R b

        Based on Lemma B.7
        (i) e ≲_R u iff <e,u> ∈ D_R
        (i) u ≲_R e iff ¬(e ≲_R u) iff ¬(<e,u> ∈ D_R)
        (ii), (a): u ≲_R u' iff ∀e ∈ E_R.<e,u> ∈ D_R => <e,u'> ∈ D_R
        (iii), (a): e ≲_R e' iff ∃u ∈ U_R.<e',u> ∈ D_R => <e,u> ∈ D_R
        Args:
            arb_object1 (ArbitraryObject): a
            arb_object2 (ArbitraryObject): b

        Returns:
            bool: The result of a ◁_R b
        """

        if (arb_object1 not in (self.universals | self.existentials)) or (
            arb_object2 not in (self.universals | self.existentials)
        ):  # pragma: not covered
            return False

        if self.is_existential(arb_object1) and self.is_existential(arb_object2):
            # Case 1
            # (iii), (a): e ≲_R e' iff ∃u ∈ U_R.<e',u> ∈ D_R => <e,u> ∈ D_R
            # not(There is an X that E prime (arb_obj2) deps on and that e (arb_obj1)does not depend upon)
            unis_e_depends_on = self.related_universals(arb_object1)
            unis_e_prime_depends_on = self.related_universals(arb_object2)
            return len(unis_e_prime_depends_on.difference(unis_e_depends_on)) == 0

        elif self.is_existential(arb_object1) and not self.is_existential(arb_object2):
            # Case 2

            # (i) e ≲_R u iff <e,u> ∈ D_R
            # There is a dependency of this structure
            return (
                Dependency(existential=arb_object1, universal=arb_object2)
                in self.dependencies
            )

        elif not self.is_existential(arb_object1) and self.is_existential(
            arb_object2
        ):  # pragma: not covered
            # Case 3

            # Not actually used but here for completeness
            # (i) u ≲_R e iff ¬(e ≲_R u) iff ¬(<e,u> ∈ D_R)
            # There is not a dependency of this structure
            return (
                Dependency(existential=arb_object2, universal=arb_object1)
                not in self.dependencies
            )

        elif not self.is_existential(arb_object1) and not self.is_existential(
            arb_object2
        ):  # pragma: not covered
            # Case 4

            # Not actually used but here for completeness
            # (ii), (a): u ≲_R u' iff ∀e ∈ E_R.<e,u> ∈ D_R => <e,u'> ∈ D_R
            # not(There is an X that depends on u (arb_obj 1) but does not depend on u_prime (arb_obj2))
            exis_depending_on_u = self.related_existentials(arb_object1)
            exis_depending_on_u_prime = self.related_existentials(arb_object2)
            return len(exis_depending_on_u.difference(exis_depending_on_u_prime)) == 0
        else:
            assert False

    @property
    def is_empty(self) -> bool:
        """
        If the relation contains no arb objects, return true, else false

        Returns:
            bool: True if relation contains nothing.
        """
        if len(self.universals) == 0 and len(self.existentials) == 0:
            assert len(self.dependencies) == 0
            return True
        else:
            return False

    def chain(self, other: "DependencyRelation") -> "DependencyRelation":
        """
        Based on Definition 4.26, p156

        R ⋊ S = <U_R ∪ U_S, E_R ∪ E_S, D_R ∪ D_S ∪ E_S × U_R>
        Args:
            other (DependencyRelation): The DependencyRelation to be chained to.

        Returns:
            DependencyRelation: The resulting Dependency Relation.
        """
        # E_S × U_R
        new_deps = cross(universals=self.universals, existentials=other.existentials)
        return DependencyRelation(
            self.universals | other.universals,  # U_R ∪ U_S
            self.existentials | other.existentials,  # E_R ∪ E_S
            self.dependencies | other.dependencies | new_deps,  # D_R ∪ D_S ∪ E_S × U_R
        )

    def E0(
        self,
        other: "DependencyRelation",
        new_pairs: set[tuple[ArbitraryObject, ArbitraryObject]],
    ) -> frozenset[Existential]:
        """
        Based on the Definition B.5, p317

        E₀ = {e ∈ E_R ∪ E_S : ∀u ∈ U_R ∪ U_S.¬(e ◁ u)}

        Args:
            self (DependencyRelation): R
            other (DependencyRelation): S
            new_pairs (set[tuple[ArbitraryObject, ArbitraryObject]]): e ◁ u

        Returns:
            frozenset[Existential]: The set of existentials in E₀
        """
        new_out: list[ArbitraryObject] = []
        # e ∈ E_R ∪ E_S
        for e in self.existentials | other.existentials:
            pair_found = False
            # ∀u ∈ U_R ∪ U_S.¬(e ◁ u)
            for u in self.universals | other.universals:
                if (e, u) in new_pairs:
                    pair_found = True
                    break
            if not pair_found:
                new_out.append(e)
        return frozenset(new_out)

    def U0(
        self,
        other: "DependencyRelation",
        new_pairs: set[tuple[ArbitraryObject, ArbitraryObject]],
        e_0: frozenset[Existential],
    ) -> frozenset[Universal]:
        """
        Based on the Definition B.5, p317

        U₀ = {u ∈ U_R ∪ U_S : ∀e ∈ E_R ∪ E_S＼E₀.(u ◁ e) -> (e ◁ u)}

        Args:
            self (DependencyRelation): R
            other (DependencyRelation): S
            new_pairs (set[tuple[ArbitraryObject, ArbitraryObject]]): e ◁ u
            e_0 (frozenset[Existential]): E₀

        Returns:
            frozenset[Universal]: The set of existentials in U₀
        """
        new_out: list[ArbitraryObject] = []
        # u ∈ U_R ∪ U_S
        for u in self.universals | other.universals:
            pair_found = False
            # ∀e ∈ (E_R ∪ E_S)＼E₀
            for e in (self.existentials | other.existentials).difference(e_0):
                # .(u ◁ e) -> (e ◁ u)
                if (u, e) in new_pairs and (e, u) not in new_pairs:
                    pair_found = True
                    break
            if not pair_found:
                new_out.append(u)
        return frozenset(new_out)

    def fusion(self, other: "DependencyRelation") -> "DependencyRelation":
        """
        Based on the Definition B.5, p317

        R ⋈ S = <U₀, E₀, Ø> ⋊ ([R]_A(R)＼(E₀ ∪ U₀) ⋈ [S]_A(S)＼(E₀ ∪ U₀))

        Args:
            other (DependencyRelation): The DependencyRelation to be fused.

        Returns:
            DependencyRelation: the resulting DependencyRelation.
        """
        if self.is_empty and other.is_empty:
            return self
        else:
            arb_objects = (
                self.existentials
                | other.existentials
                | self.universals
                | other.universals
            )
            pairs: set[tuple[ArbitraryObject, ArbitraryObject]] = set()
            for x in arb_objects:
                for y in arb_objects:
                    if self.triangle(x, y) or other.triangle(x, y):
                        pairs.add((x, y))
            # e ◁ u
            e_triangle_u = transitive_closure(pairs, arb_objects)

            e_0 = self.E0(other, e_triangle_u)
            u_0 = self.U0(other, e_triangle_u, e_0)

            # <U₀, E₀, Ø>
            initial_relation = DependencyRelation(u_0, e_0, frozenset())
            a_r = self.universals | self.existentials
            a_s = other.universals | other.existentials

            # A(R)＼(E₀ ∪ U₀)
            expr1 = set(a_r.difference(e_0 | u_0))
            # A(S)＼(E₀ ∪ U₀)
            expr2 = set(a_s.difference(e_0 | u_0))

            # <U₀, E₀, Ø> ⋊ ([R]_A(R)＼(E₀ ∪ U₀) ⋈ [S]_A(S)＼(E₀ ∪ U₀))
            return initial_relation.chain(
                self.restriction(expr1).fusion(other.restriction(expr2))
            )

    def negation(self) -> "DependencyRelation":
        """
        Based on 4.31, p159, Negation of a dependency relation

        [R]ᶰ = <E_R, U_R, {<a,b> ∈ U_R × E_R : <b,a> ∉ D_R}

        Returns:
            DependencyRelation: The negated dependency relation.
        """
        # Every new existential now depends on every new universal
        # Except those that the ancestor existential depended on the ancestor universal

        ancestor_deps = cross(
            universals=self.existentials, existentials=self.universals
        )

        # {<a,b> ∈ U_R × E_R : <b,a> ∉ D_R}
        new_deps = frozenset(
            {
                ancestor_dep
                for ancestor_dep in ancestor_deps
                if Dependency(
                    existential=ancestor_dep.universal,
                    universal=ancestor_dep.existential,
                )
                not in self.dependencies
            }
        )
        return DependencyRelation(
            universals=self.existentials,
            existentials=self.universals,
            dependencies=new_deps,
        )
