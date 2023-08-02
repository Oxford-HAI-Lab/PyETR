__all__ = ["View", "Commitment"]

from functools import reduce
from itertools import permutations
from typing import Optional, cast

from pyetr.tools import ArbitraryObjectGenerator

from .add_new_emphasis import add_new_emphasis
from .atom import Atom
from .dependency import (
    Dependency,
    DependencyRelation,
    DependencyStructure,
    _separate_arb_objects,
)
from .stateset import SetOfStates, State
from .term import ArbitraryObject, Term


def get_subset(
    stage_external: SetOfStates, supposition_internal: SetOfStates
) -> SetOfStates:
    out_set = set()
    for state_stage_ext in stage_external:
        for supp_state in supposition_internal:
            if supp_state.issubset(state_stage_ext):
                out_set.add(state_stage_ext)
    return SetOfStates(out_set)


Stage = SetOfStates
Supposition = SetOfStates
Existential = ArbitraryObject
Universal = ArbitraryObject


def stage_supposition_product(
    stage_supposition_external: tuple[Stage, Supposition],
    stage_supposition_internal: tuple[Stage, Supposition],
) -> tuple[Stage, Supposition]:
    stage_external, supposition_external = stage_supposition_external
    stage_internal, supposition_internal = stage_supposition_internal
    subset = get_subset(stage_external, supposition_internal)
    result_stage = (subset * stage_internal) | stage_external.difference(subset)
    return result_stage, supposition_external


def arg_max_states(potentials: list[tuple[int, State]]) -> list[State]:
    max_potential = max([potential for potential, _ in potentials])
    return [state for potential, state in potentials if potential == max_potential]


def substitution(
    arb_gen: ArbitraryObjectGenerator,
    dep_structure: DependencyStructure,
    arb_obj: ArbitraryObject,
    term: Term | ArbitraryObject,
    stage: Stage,
    supposition: Supposition,
) -> "View":
    """
    Based on definition 4.32
    """

    def Z() -> set[ArbitraryObject]:
        unis = set(
            [
                uni
                for uni in dep_structure.universals
                if dep_structure.triangle(uni, arb_obj)
            ]
        )
        exis = set(
            [
                exi
                for exi in dep_structure.existentials
                if dep_structure.less_sim(exi, arb_obj)
            ]
        )
        return (unis | exis) - {arb_obj}

    def _determine_substitutions(
        arb_objects: set[ArbitraryObject],
    ) -> dict[ArbitraryObject, ArbitraryObject]:
        return arb_gen.redraw(arb_objects)

    assert len(stage.arb_objects & supposition.arb_objects) == 0

    old_T = dep_structure

    new_dep_structure = dep_structure
    new_stage = stage

    subs = _determine_substitutions(Z())
    new_dep_structure = new_dep_structure.replace(subs)
    new_stage = new_stage.replace(
        cast(dict[ArbitraryObject, Term | ArbitraryObject], subs)
    )

    new_stage = new_stage.replace({arb_obj: term})

    new_dep_structure = new_dep_structure.restriction(set(subs.values()))
    T_prime = old_T.chain(new_dep_structure)
    T_prime = T_prime.restriction(new_stage.arb_objects | supposition.arb_objects)
    return View(
        stage=new_stage,
        supposition=supposition,
        dependency_relation=T_prime.dependency_relation,
    )


def state_division(
    state: State,
    other_stage: Stage,
    other_supposition: Supposition,
) -> State:
    """
    Based on definition 4.38
    """
    delta_that_meet_cond: list[State] = []
    for delta in other_stage:
        if delta.issubset(state) and any(
            psi.issubset(state) for psi in other_supposition
        ):
            delta_that_meet_cond.append(delta)

    if len(delta_that_meet_cond) == 1:
        return state - delta_that_meet_cond[0]
    else:
        return state


class View:
    stage: Stage
    supposition: Supposition
    dependency_relation: DependencyRelation

    def __init__(
        self,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        dependency_relation.validate(stage | supposition)
        self.dependency_relation = dependency_relation

    @property
    def detailed(self) -> str:
        return f"<View \n  stage={self.stage.detailed} \n  supposition={self.supposition.detailed} \n  dep_rel={self.dependency_relation.detailed}\n>"

    def __repr__(self) -> str:
        if self.is_falsum:
            return "F"
        elif self.is_verum:
            return "T"
        elif len(self.dependency_relation.dependencies) == 0:
            return f"{self.stage}^{self.supposition}"
        else:
            return f"{self.stage}^{self.supposition} deps={self.dependency_relation}"

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        return self.stage.arb_objects | self.supposition.arb_objects

    @property
    def universals_and_existentials(self) -> tuple[set[Universal], set[Existential]]:
        return _separate_arb_objects(self.arb_objects)

    def _fuse_views(
        self, view: "View", inherited_dependencies: DependencyStructure
    ) -> DependencyStructure:
        self_uni, self_exi = self.universals_and_existentials
        view_uni, view_exi = view.universals_and_existentials
        expr1 = inherited_dependencies.fusion(
            DependencyStructure(self_uni, self_exi, self.dependency_relation)
        )
        expr2 = inherited_dependencies.fusion(
            DependencyStructure(view_uni, view_exi, view.dependency_relation)
        )
        return expr1.fusion(expr2)

    def _product(
        self, view: "View", inherited_dependencies: DependencyStructure
    ) -> "View":
        """
        Based on definition 4.27
        """
        # Corresponds to line 4
        stage, supposition = stage_supposition_product(
            (self.stage, self.supposition), (view.stage, view.supposition)
        )
        dep_structure = self._fuse_views(view, inherited_dependencies)
        dep_rel = dep_structure.dependency_relation.restriction(
            (stage | supposition).arb_objects
        )
        return View(stage, supposition, dep_rel)

    def product(
        self, view: "View", inherited_dependencies: Optional[DependencyStructure] = None
    ) -> "View":
        """
        Based on definition 4.27
        """
        if inherited_dependencies is None:
            # Corresponds to line 5
            return self._product(
                view, DependencyStructure(set(), set(), DependencyRelation(frozenset()))
            )
        else:
            # Corresponds to line 4
            return self._product(view, inherited_dependencies)

    def _sum(self, view: "View", inherited_dependencies: DependencyStructure):
        """
        Based on definition 4.28
        """
        if self.supposition != view.supposition:
            raise ValueError(
                f"Invalid sum on {self.supposition} and {view.supposition}"
            )

        supposition = self.supposition
        # Corresponds to line 1
        stage = self.stage | view.stage
        dep_structure = self._fuse_views(view, inherited_dependencies)
        dep_rel = dep_structure.dependency_relation.restriction(
            (stage | supposition).arb_objects
        )
        return View(stage, supposition, dep_rel)

    def sum(
        self, view: "View", inherited_dependencies: Optional[DependencyStructure] = None
    ) -> "View":
        """
        Based on definition 4.28
        """
        if inherited_dependencies is None:
            # Corresponds to line 2
            return self._product(
                view, DependencyStructure(set(), set(), DependencyRelation(frozenset()))
            )
        else:
            # Corresponds to line 1
            return self._product(view, inherited_dependencies)

    def answer(self, other: "View") -> "View":
        """
        Based on definition 4.30
        """
        if not other.supposition.is_verum:
            return self
        else:
            supposition = self.supposition
            potentials: list[tuple[int, State]] = []
            for s in self.stage:
                potential = SetOfStates({s}).answer_potential(other.stage)
                potentials.append((potential, s))
            stage = SetOfStates(arg_max_states(potentials))

            if stage.emphasis_count + supposition.emphasis_count == 0:
                stage, supposition = add_new_emphasis(stage, supposition)

            dependency_relation = self.dependency_relation.restriction(
                (stage | supposition).arb_objects
            )
            return View(stage, supposition, dependency_relation)

    def negation(self) -> "View":
        """
        Based on definition 4.31
        """
        verum = SetOfStates({State({})})
        stage, _ = stage_supposition_product(
            (self.supposition, verum), (self.stage.negation(), verum)
        )
        # Every new existential now depends on every new universal
        # Except those that the ancestor existential depended on the ancestor universal
        new_pairs: list[tuple[Existential, Universal]] = []
        for arb_object in stage.arb_objects:
            if arb_object.is_existential:
                # This will become universal
                current_existential = arb_object

                for arb_object in stage.arb_objects:
                    if not arb_object.is_existential:
                        # This will become existential
                        current_universal = arb_object
                        new_pairs.append((current_existential, current_universal))
        # Now isolate only valid dependencies
        final_pairs: list[tuple[Existential, Universal]] = []
        for exi, uni in new_pairs:
            for dep in self.dependency_relation.dependencies:
                # If Dependency is not pre-existing add to the final pairs
                if not (dep.universal == uni and dep.existential == exi):
                    final_pairs.append((exi, uni))

        # Invert all arb_objects. Due to being references this will update all
        for arb_object in stage.arb_objects:
            arb_object._is_existential = not arb_object.is_existential
        final_pairs: list[tuple[Universal, Existential]] = final_pairs

        # Form new deps
        final_deps: list[Dependency] = [Dependency(u, e) for u, e in final_pairs]
        return View(
            stage=stage,
            supposition=verum,
            dependency_relation=DependencyRelation(frozenset(final_deps)),
        )

    def issue_matches(
        self, other: "View"
    ) -> set[tuple[Term | ArbitraryObject, Term | ArbitraryObject]]:
        self_atoms_with_emphasis: list[Atom] = []
        other_atoms_with_emphasis: list[Atom] = []
        for state in self.stage | self.supposition:
            for atom in state:
                if atom.has_emphasis:
                    self_atoms_with_emphasis.append(atom)

        for state in other.stage | other.supposition:
            for atom in state:
                if atom.has_emphasis:
                    other_atoms_with_emphasis.append(atom)

        pairs: list[tuple[Term | ArbitraryObject, Term | ArbitraryObject]] = []
        for atom_self in self_atoms_with_emphasis:
            for atom_other in other_atoms_with_emphasis:
                if atom_self.is_same_excl_emphasis(atom_other):
                    pairs.append((atom_self.emphasis_term, atom_other.emphasis_term))

        return set(pairs)

    @property
    def dep_structure(self) -> "DependencyStructure":
        return DependencyStructure.from_arb_objects(
            self.arb_objects, self.dependency_relation
        )

    def merge(self, view: "View") -> "View":
        """
        Based on Definition 4.33
        """

        def _m_prime(
            gamma: State,
        ) -> set[tuple[Term | ArbitraryObject, Universal]]:
            out: set[tuple[Term | ArbitraryObject, Universal]] = set()
            for t, u in self.issue_matches(view):
                if isinstance(u, ArbitraryObject) and not u.is_existential:
                    phi_exists = False
                    for phi in view.supposition:
                        # TODO: Do these replacements need to simultaneous?
                        new_phi = State([atom.replace({u: t}) for atom in phi])
                        if new_phi.issubset(gamma) and len(phi.difference(gamma)) != 0:
                            phi_exists = True
                            break
                    if phi_exists:
                        out.add((t, u))
            return out

        if len(self.arb_objects & view.arb_objects) == 0 or (
            view.dep_structure == self.dep_structure.restriction(view.arb_objects)
        ):
            r_fuse_s = self.dep_structure.fusion(view.dep_structure)
            arb_gen = ArbitraryObjectGenerator(self.arb_objects | view.arb_objects)
            views_for_sum: list[View] = []
            for gamma in self.stage:
                # TODO: What to do if m_prime(gamma) is empty?
                m_prime = _m_prime(gamma)
                if len(m_prime) == 0:
                    views_for_sum.append(
                        View(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                        ).product(view, inherited_dependencies=r_fuse_s)
                    )
                else:
                    product_result: View = reduce(
                        lambda v1, v2: v1.product(v2, r_fuse_s),
                        [
                            substitution(
                                arb_gen=arb_gen,
                                dep_structure=r_fuse_s,
                                arb_obj=u,
                                term=t,
                                stage=view.stage,
                                supposition=SetOfStates({State({})}),
                            )
                            for t, u in m_prime
                        ],
                    )
                    views_for_sum.append(
                        View(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                        )
                        .product(view, inherited_dependencies=r_fuse_s)
                        .product(product_result, inherited_dependencies=r_fuse_s)
                    )
            return reduce(lambda v1, v2: v1.sum(v2, r_fuse_s), views_for_sum)
        else:
            return self

    def _uni_exi_condition(self, view: "View") -> bool:
        """
        Translated from:
        A(Γ) ∩ A(Θ) = ∅ and (A(R) ∩ A(S) = ∅ or [R]Δ = S)
        """
        expr1 = len(self.stage.arb_objects & self.supposition.arb_objects) == 0
        expr2 = len(self.arb_objects | view.arb_objects) == 0
        expr3 = (
            self.dep_structure.restriction(view.stage.arb_objects) == view.dep_structure
        )
        return expr1 and (expr2 or expr3)

    def universal_product(self, view: "View") -> "View":
        """
        Based on Definition 4.35
        """

        def _m_prime() -> set[tuple[Universal, Term | ArbitraryObject]]:
            self_u, _ = _separate_arb_objects(
                self.stage.arb_objects | self.supposition.arb_objects
            )
            output_set = set()
            for u, t in self.issue_matches(view):
                if isinstance(u, ArbitraryObject) and u in (
                    self_u - self.supposition.arb_objects
                ):
                    output_set.add((u, t))
            return output_set

        arb_gen = ArbitraryObjectGenerator(self.arb_objects | view.arb_objects)

        m_prime = _m_prime()
        if len(m_prime) == 0:
            return self
        if self._uni_exi_condition(view):
            if not view.supposition.is_verum:
                return self
            initial_item = View(
                stage=view.supposition,
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
            )
            r_fuse_s = self.dep_structure.fusion(view.dep_structure)
            product_result: View = reduce(
                lambda v1, v2: v1.product(v2, r_fuse_s),
                [
                    substitution(
                        arb_gen=arb_gen,
                        dep_structure=r_fuse_s,
                        arb_obj=u,
                        term=t,
                        stage=self.stage,
                        supposition=SetOfStates({State({})}),
                    )
                    for u, t in m_prime
                ],
            )
            return initial_item.product(product_result, r_fuse_s)
        else:
            return self

    def existential_sum(self, view: "View") -> "View":
        """
        Based on Definition 4.37
        """

        def _big_union(e: Existential) -> SetOfStates:
            def _big_product(gamma: State) -> SetOfStates:
                def B(gamma: State, e: Existential) -> State:
                    return State([x for x in gamma if x.emphasis_term == e])

                return reduce(
                    lambda s1, s2: s1 * s2,
                    [SetOfStates({State({x}), State({~x})}) for x in B(gamma, e)],
                )

            assert e in self.arb_objects
            final_sets: list[SetOfStates] = []
            for gamma in self.stage:
                if e in gamma.arb_objects:
                    x_set = State([x for x in gamma if e not in x.arb_objects])
                    for delta in _big_product(gamma):
                        if not delta.issubset(gamma):
                            x_set.union(delta)

                    final_sets.append(SetOfStates({gamma}) | SetOfStates({x_set}))

            return reduce(lambda s1, s2: s1 | s2, final_sets)

        def _m_prime() -> set[tuple[Existential, Term | ArbitraryObject]]:
            _, self_e = self.universals_and_existentials
            output_set = set()
            for e, t in self.issue_matches(view):
                if isinstance(e, ArbitraryObject) and e in (
                    self_e - (self.supposition | view.stage).arb_objects
                ):
                    if not any(
                        d.existential == e
                        for d in self.dependency_relation.dependencies
                    ):
                        output_set.add((e, t))
            return output_set

        if not view.supposition.is_verum:
            return self

        if self._uni_exi_condition(view):
            m_prime = _m_prime()
            if len(m_prime) == 0:
                return self
            else:
                arb_gen = ArbitraryObjectGenerator(self.arb_objects | view.arb_objects)
                r_fuse_s = self.dep_structure.fusion(view.dep_structure)
                sum_result: View = reduce(
                    lambda v1, v2: v1.sum(v2, r_fuse_s),
                    [
                        substitution(
                            arb_gen=arb_gen,
                            dep_structure=r_fuse_s,
                            arb_obj=e,
                            term=t,
                            stage=_big_union(e),
                            supposition=self.supposition,
                        )
                        for e, t in m_prime
                    ],
                )
                return self.sum(sum_result, r_fuse_s)
        else:
            return self

    def update(self, view: "View") -> "View":
        """
        Based on Definition 4.34
        """
        arb_gen = ArbitraryObjectGenerator(self.arb_objects | view.arb_objects)
        shared_objs = self.arb_objects & view.arb_objects
        view = arb_gen.novelise(shared_objs, view)
        return (
            self.universal_product(view).existential_sum(view).answer(view).merge(view)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, View):
            return False
        return (
            self.stage == other.stage
            and self.supposition == other.supposition
            and self.dependency_relation == other.dependency_relation
        )

    def __hash__(self) -> int:
        return hash((self.stage, self.supposition, self.dependency_relation))

    def division(self, other: "View") -> "View":
        """
        Based on definition 4.38
        """

        def cond(delta: State):
            for psi in other.supposition:
                for gamma in self.stage:
                    if delta.issubset(gamma) and psi.issubset(gamma):
                        return True
            return False

        if all(cond(delta) for delta in other.stage):
            new_stage = SetOfStates(
                [
                    state_division(
                        state=gamma,
                        other_stage=other.stage,
                        other_supposition=other.supposition,
                    )
                    for gamma in self.stage
                ]
            )
            new_dep_rel = self.dependency_relation.restriction(
                new_stage.arb_objects | self.supposition.arb_objects
            )
            return View(
                stage=new_stage,
                supposition=self.supposition,
                dependency_relation=new_dep_rel,
            )
        else:
            return self

    @property
    def is_verum(self) -> bool:
        return self.stage.is_verum and self.supposition.is_verum

    @property
    def is_falsum(self) -> bool:
        return self.stage.is_falsum and self.supposition.is_verum

    def factor(self, other: "View") -> "View":
        """
        Based on definition 4.39
        """

        def big_intersection(state: State) -> State:
            out: list[State] = []
            for t, a in self.issue_matches(other):
                if isinstance(a, ArbitraryObject) and not a.is_existential:
                    replaced_stage = other.stage.replace({a: t})
                    replaced_supposition = other.supposition.replace({a: t})
                    out.append(
                        state_division(
                            state=state,
                            other_stage=replaced_stage,
                            other_supposition=replaced_supposition,
                        )
                    )
            # TODO: Is this correct?
            if len(out) == 0:
                return State({})
            return reduce(lambda s1, s2: s1 & s2, out)

        def state_factor(state: State) -> State:
            """
            Based on definition 4.39
            """
            gamma_prime = state_division(
                state=state,
                other_stage=other.stage,
                other_supposition=other.supposition,
            )
            expr = big_intersection(state)
            if len(expr) == 0:
                return gamma_prime
            else:
                return gamma_prime & expr

        if not other.is_falsum:
            new_stage = SetOfStates([state_factor(state=gamma) for gamma in self.stage])

        else:
            new_stage = SetOfStates(
                gamma for gamma in self.stage if not gamma.is_primitive_absurd
            )

        new_dep_rel = self.dependency_relation.restriction(
            new_stage.arb_objects | self.supposition.arb_objects
        )
        return View(
            stage=new_stage,
            supposition=self.supposition,
            dependency_relation=new_dep_rel,
        )

    def depose(self) -> "View":
        verum = SetOfStates({State({})})
        new_stage = self.stage | self.supposition.negation()
        return View(
            stage=new_stage,
            supposition=verum,
            dependency_relation=self.dependency_relation,
        )

    def replace(
        self, replacements: dict[ArbitraryObject, Term | ArbitraryObject]
    ) -> "View":
        new_stage = self.stage.replace(replacements)
        new_supposition = self.supposition.replace(replacements)
        filtered_replacements = {
            e: n for e, n in replacements.items() if isinstance(n, ArbitraryObject)
        }
        new_dep_rel = self.dependency_relation.replace(filtered_replacements)

        return View(
            stage=new_stage,
            supposition=new_supposition,
            dependency_relation=new_dep_rel.restriction(
                new_stage.arb_objects | new_supposition.arb_objects
            ),
        )

    def is_equivalent_under_arb_sub(self, other: "View") -> bool:
        """
        Complexity is O((n!)^2*n) where n is average num of exi and unis

        For exis and unis above 9 or 10 (of each) this becomes an issue, below is fine
        """
        self_uni, self_exi = _separate_arb_objects(self.arb_objects)
        other_uni, other_exi = _separate_arb_objects(other.arb_objects)
        if len(self_uni) != len(other_uni) or len(self_exi) != len(other_exi):
            return False
        if (
            len(self_uni) > 9
            or len(self_exi) > 9
            or len(other_uni) > 9
            or len(other_exi) > 9
        ):
            raise ValueError("Too many unis or exis to feasibly compute")

        for exi_perm in permutations(other_exi):
            for uni_perm in permutations(other_uni):
                new_view = self
                replacements = {
                    **dict(zip(exi_perm, self_exi)),
                    **dict(zip(uni_perm, self_uni)),
                }

                new_view = new_view.replace(
                    cast(dict[ArbitraryObject, Term | ArbitraryObject], replacements)
                )

                if new_view == other:
                    return True
        return False


class Commitment:
    views: set[View]
    current_view: View

    def __init__(self, views: set[View], current_view: View) -> None:
        self.views = views
        self.current_view = current_view
