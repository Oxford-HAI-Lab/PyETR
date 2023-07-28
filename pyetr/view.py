__all__ = ["View", "Commitment"]

from functools import reduce
from operator import xor
from pprint import pformat
from typing import Optional

from pyetr.atom import Atom

from .add_new_emphasis import add_new_emphasis
from .dependency import (
    Dependency,
    DependencyRelation,
    DependencyStructure,
    _separate_arb_objects,
)
from .stateset import SetOfStates, State
from .term import ArbitraryObject, Emphasis, Term


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
    dep_structure: DependencyStructure,
    arb_obj: ArbitraryObject,
    term: Term | ArbitraryObject | Emphasis,
    stage: Stage,
    supposition: Supposition,
) -> "View":
    """
    Based on definition 4.32
    """
    raise NotImplementedError


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

    def __repr__(self) -> str:
        return f"<View \n  stage={pformat(self.stage)} \n  supposition={pformat(self.supposition)} \n  dep_rel={self.dependency_relation}\n>"

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
            arb_object.is_existential = not arb_object.is_existential
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
        ) -> set[tuple[Term | ArbitraryObject | Emphasis, Universal]]:
            out: set[tuple[Term | ArbitraryObject | Emphasis, Universal]] = set()
            for t, u in self.issue_matches(view):
                if isinstance(u, ArbitraryObject) and not u.is_existential:
                    phi_exists = False
                    for phi in view.supposition:
                        new_phi = State(
                            [atom.replace(old_term=t, new_term=u) for atom in phi]
                        )
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
            views_for_sum: list[View] = []
            for gamma in self.stage:
                product_result: View = reduce(
                    lambda v1, v2: v1.product(v2, r_fuse_s),
                    [
                        substitution(
                            dep_structure=r_fuse_s,
                            arb_obj=u,
                            term=t,
                            stage=view.stage,
                            supposition=SetOfStates({State({})}),
                        )
                        for t, u in _m_prime(gamma)
                    ],
                )
                views_for_sum.append(
                    View(
                        SetOfStates({gamma}), self.supposition, self.dependency_relation
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
        A(Γ) ∩ A(Θ) = ∅ and either A(R) ∩ A(S) = ∅ or [R]Δ = S
        """
        expr1 = len(self.stage.arb_objects & self.supposition.arb_objects) == 0
        expr2 = (
            len(
                self.dependency_relation.arb_objects
                | view.dependency_relation.arb_objects
            )
            == 0
        )
        expr3 = (
            self.dependency_relation.restriction(view.stage.arb_objects)
            == view.dependency_relation
        )

        return expr1 and xor(expr2, expr3)

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
            if output_set == set():
                raise ValueError("No values were found m_prime output set")
            return output_set

        if self._uni_exi_condition(view):
            if not view.supposition.is_verum:
                return self
                # raise ValueError("External supposition is not verum")
            initial_item = View(
                stage=view.supposition,
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
            )
            r_fuse_s = self.dep_structure.fusion(view.dep_structure)
            m_prime = _m_prime()
            product_result: View = reduce(
                lambda v1, v2: v1.product(v2, r_fuse_s),
                [
                    substitution(
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

    @staticmethod
    def _big_product() -> SetOfStates:
        raise NotImplementedError

    @staticmethod
    def _big_union() -> SetOfStates:
        def B(gamma, e):
            raise NotImplementedError

        # TODO: e is used twice as descriptor??
        raise NotImplementedError

    def existential_sum(self, view: "View") -> "View":
        """
        Based on Definition 4.37
        """

        def _m_prime() -> set[tuple[Universal, Term | ArbitraryObject]]:
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
            raise ValueError("External supposition is not verum")

        if self._uni_exi_condition(view):
            m_prime = _m_prime()
            if m_prime == set():
                return self
            else:
                r_fuse_s = self.dep_structure.fusion(view.dep_structure)
                sum_items: list[View] = []
                for e, t in m_prime:
                    sum_items.append(
                        substitution(
                            dep_structure=r_fuse_s,
                            arb_obj=e,
                            term=t,
                            stage=self._big_union(),
                            supposition=self.supposition,
                        )
                    )
                sum_result: View = reduce(
                    lambda v1, v2: v1.sum(v2, r_fuse_s),
                    sum_items,
                )
                return self.sum(sum_result, r_fuse_s)
        else:
            return self

    def update(self, view: "View") -> "View":
        """
        Based on Definition 4.34
        """
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


class Commitment:
    views: set[View]
    current_view: View

    def __init__(self, views: set[View], current_view: View) -> None:
        self.views = views
        self.current_view = current_view
