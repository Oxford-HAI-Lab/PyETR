__all__ = ["View", "Commitment"]

from pprint import pformat

from pyetr.term import ArbitraryObject, Function, Term

from .dependency import DependencyRelation
from .stateset import set_of_states, state


def get_subset(
    stage_external: set_of_states, supposition_internal: set_of_states
) -> set_of_states:
    out_set = set()
    for state_stage_ext in stage_external:
        for supp_state in supposition_internal:
            if supp_state.issubset(state_stage_ext):
                out_set.add(state_stage_ext)
    return set_of_states(out_set)


def stage_supposition_product(
    stage_supposition_external: tuple[set_of_states, set_of_states],
    stage_supposition_internal: tuple[set_of_states, set_of_states],
) -> tuple[set_of_states, set_of_states]:
    stage_external, supposition_external = stage_supposition_external
    stage_internal, supposition_internal = stage_supposition_internal
    subset = get_subset(stage_external, supposition_internal)
    result_stage = subset * stage_internal | stage_external.difference(subset)
    return result_stage, supposition_external


def arg_max_states(potentials: list[tuple[int, state]]) -> list[state]:
    raise NotImplementedError


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

    def __mul__(self, other: "View") -> "View":
        """
        Based on definition 4.27
        """
        raise NotImplementedError

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

    def __invert__(self) -> "View":
        """
        Based on definition 4.31
        """
        raise NotImplementedError


class Commitment:
    view1: View
    view2: View

    def __init__(self, view1: View, view2: View) -> None:
        self.view1 = view1
        self.view2 = view2


def extract_candidates(states: set_of_states):
    raise NotImplementedError


def get_arb_universals(candidates):
    raise NotImplementedError


class Candidate:
    term: ArbitraryObject | Function | Term


def compare_candidate(candidate1: Candidate, candidate2: Candidate) -> Candidate:
    raise NotImplementedError


def determine_emphasis(stage: set_of_states, supposition: set_of_states):
    if not (supposition.is_verum or supposition.is_falsum):
        candidates = extract_candidates(supposition)
    elif not (stage.is_verum or stage.is_falsum):
        candidates = extract_candidates(stage)
    else:
        return None

    # Direct arguments of a predicate
    # Term is opaque - no items within

    arbitrary_universals = get_arb_universals(candidates)
    if len(arbitrary_universals) != 0:
        pass
    ### TYPE ###
    # Rule2/3 Universals have priority over existentials

    # Rule3.1 Existentials have priority over functions with 0 arity

    # Rule3.2 Terms have lower priority than functions

    ### ORDER ###
    # Rule 4: left most wins in predicate

    ### QUANTITY ###
    # Lower priority than type (applies to objects of the same type)
    # Most wins

    ### RANDOMISED ###
    # use random.sample


def add_new_emphasis(
    stage: set_of_states, supposition: set_of_states
) -> tuple[set_of_states, set_of_states]:
    raise NotImplementedError
