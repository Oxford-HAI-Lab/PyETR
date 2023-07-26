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
from .stateset import set_of_states, state
from .term import ArbitraryObject


def get_subset(
    stage_external: set_of_states, supposition_internal: set_of_states
) -> set_of_states:
    out_set = set()
    for state_stage_ext in stage_external:
        for supp_state in supposition_internal:
            if supp_state.issubset(state_stage_ext):
                out_set.add(state_stage_ext)
    return set_of_states(out_set)


Stage = set_of_states
Supposition = set_of_states
Existential = ArbitraryObject
Universal = ArbitraryObject


def stage_supposition_product(
    stage_supposition_external: tuple[Stage, Supposition],
    stage_supposition_internal: tuple[Stage, Supposition],
) -> tuple[set_of_states, set_of_states]:
    stage_external, supposition_external = stage_supposition_external
    stage_internal, supposition_internal = stage_supposition_internal
    subset = get_subset(stage_external, supposition_internal)
    result_stage = (subset * stage_internal) | stage_external.difference(subset)
    return result_stage, supposition_external


def arg_max_states(potentials: list[tuple[int, state]]) -> list[state]:
    max_potential = max([potential for potential, _ in potentials])
    return [state for potential, state in potentials if potential == max_potential]


class View:
    stage: set_of_states
    supposition: set_of_states
    dependency_relation: DependencyRelation

    def __init__(
        self,
        stage: set_of_states,
        supposition: set_of_states,
        dependency_relation: DependencyRelation,
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        dependency_relation.validate(stage.union(supposition))
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

    def _product(
        self, view: "View", inherited_dependencies: DependencyStructure
    ) -> "View":
        # Corresponds to line 4
        stage, supposition = stage_supposition_product(
            (self.stage, self.supposition), (view.stage, view.supposition)
        )
        self_uni, self_exi = self.universals_and_existentials
        view_uni, view_exi = view.universals_and_existentials
        expr1 = inherited_dependencies.fusion(
            DependencyStructure(self_uni, self_exi, self.dependency_relation)
        )
        expr2 = inherited_dependencies.fusion(
            DependencyStructure(view_uni, view_exi, view.dependency_relation)
        )
        dep_structure = expr1.fusion(expr2)
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

    def __add__(self, other: "View") -> "View":
        """
        Based on definition 4.28
        """
        raise NotImplementedError

    def answer(self, other: "View") -> "View":
        """
        Based on definition 4.30
        """
        if not other.supposition.is_verum:
            return self
        else:
            supposition = self.supposition
            potentials: list[tuple[int, state]] = []
            for s in self.stage:
                potential = set_of_states({s}).answer_potential(other.stage)
                potentials.append((potential, s))
            stage = set_of_states(arg_max_states(potentials))

            if not (stage.has_emphasis and supposition.has_emphasis):
                stage, supposition = add_new_emphasis(stage, supposition)

            dependency_relation = self.dependency_relation.restriction(
                stage | supposition
            )
            return View(stage, supposition, dependency_relation)

    def negation(self) -> "View":
        """
        Based on definition 4.31
        """

        def invert_stage_and_relation(
            stage: Stage, dep_rel: DependencyRelation
        ) -> DependencyRelation:
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
                for dep in dep_rel.dependencies:
                    # If Dependency is not pre-existing add to the final pairs
                    if not (dep.universal == uni and exi in dep.existentials):
                        final_pairs.append((exi, uni))

            # Invert all arb_objects. Due to being references this will update all
            for arb_object in stage.arb_objects:
                arb_object.is_existential = not arb_object.is_existential
            final_pairs: list[tuple[Universal, Existential]] = final_pairs

            # Form new deps
            new_deps: list[tuple[Universal, set[Existential]]] = []
            for uni, exi in final_pairs:
                existing_deps = [(u, e) for u, e in new_deps if uni == u]
                if len(existing_deps) == 0:
                    new_deps.append((uni, {exi}))
                elif len(existing_deps) == 1:
                    _, existing_exis = existing_deps[0]
                    existing_exis.add(exi)
                else:
                    assert False

            final_deps = [Dependency(u, frozenset(e)) for u, e in new_deps]

            return DependencyRelation(frozenset(final_deps))

        verum = set_of_states({state({})})
        stage, _ = stage_supposition_product(
            (self.supposition, verum), (self.stage.negation(), verum)
        )
        dep_rel = invert_stage_and_relation(stage, self.dependency_relation)
        return View(stage=stage, supposition=verum, dependency_relation=dep_rel)


class Commitment:
    view1: View
    view2: View

    def __init__(self, view1: View, view2: View) -> None:
        self.view1 = view1
        self.view2 = view2
