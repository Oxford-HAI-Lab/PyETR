__all__ = ["View", "Commitment"]

from pprint import pformat
from typing import Optional

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
        total_emphasis = stage.has_emphasis + supposition.has_emphasis
        if total_emphasis == 2:
            raise ValueError("Both stage and supposition have an Emphasis")
        elif total_emphasis == 0 and not (
            (stage.is_falsum or stage.is_verum)
            and (supposition.is_falsum or supposition.is_verum)
        ):
            raise ValueError("Neither stage nor supposition has an Emphasis")
        # view has exactly one emphasis

    def __repr__(self) -> str:
        return f"<View \n  stage={pformat(self.stage)} \n  supposition={pformat(self.supposition)} \n  dep_rel={self.dependency_relation}\n>"

    @property
    def universals_and_existentials(self) -> tuple[set[Universal], set[Existential]]:
        return _separate_arb_objects(
            self.stage.arb_objects | self.supposition.arb_objects
        )

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
        return View(stage, supposition, dep_structure.dependency_relation)

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
        # TODO: Suppositions must be equal?
        supposition = self.supposition
        # Corresponds to line 1
        stage = self.stage | view.stage
        dep_structure = self._fuse_views(view, inherited_dependencies)
        return View(stage, supposition, dep_structure.dependency_relation)

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

            if not (stage.has_emphasis and supposition.has_emphasis):
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

    def merge(self, view: "View") -> "View":
        """
        Based on Definition 4.33
        """

        def _m_prime(
            s: State,
        ) -> set[
            tuple[Term | ArbitraryObject | Emphasis, Term | ArbitraryObject | Emphasis]
        ]:
            raise NotImplementedError

        self_arb = self.stage.arb_objects | self.supposition.arb_objects
        other_arb = view.stage.arb_objects | view.supposition.arb_objects
        if len(self_arb & other_arb) == 0 or False:  # TODO: What is this?
            return self
        raise NotImplementedError

    def universal_product(self, view: "View") -> "View":
        """
        Based on Definition 4.35
        """
        if not view.supposition.is_verum:
            raise ValueError("External supposition is not verum")
        raise NotImplementedError

    def existential_sum(self, view: "View") -> "View":
        """
        Based on Definition 4.37
        """
        if not view.supposition.is_verum:
            raise ValueError("External supposition is not verum")
        raise NotImplementedError


class Commitment:
    views: set[View]
    current_view: View

    def __init__(self, views: set[View], current_view: View) -> None:
        self.views = views
        self.current_view = current_view

    def update(self, view: View) -> "Commitment":
        """
        Based on Definition 4.34
        """
        # TODO: Why is C relevant here? Why not just operate on views?

        if view not in self.views:
            raise ValueError("View not in views")

        new_view = (
            self.current_view.universal_product(view)
            .existential_sum(view)
            .answer(view)
            .merge(view)
        )
        return Commitment(self.views, new_view)
