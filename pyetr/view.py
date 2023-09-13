__all__ = ["View"]

from collections import defaultdict
from functools import reduce
from itertools import permutations
from typing import Optional, cast

from pyetr.issues import IssueStructure
from pyetr.tools import ArbitraryObjectGenerator, powerset
from pyetr.weight import Weight

from .atom import Atom
from .dependency import Dependency, DependencyRelation
from .stateset import SetOfStates, State
from .term import ArbitraryObject, FunctionalTerm, Term
from pyetr import term


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
    """
    Definition 5.15, p208
    """
    stage_external, supposition_external = stage_supposition_external
    stage_internal, supposition_internal = stage_supposition_internal
    subset = get_subset(stage_external, supposition_internal)
    result_stage = (subset * stage_internal) | stage_external.difference(subset)
    return result_stage, supposition_external


def arg_max_states(potentials: list[tuple[int, State]]) -> list[State]:
    if len(potentials) == 0:
        return []
    max_potential = max([potential for potential, _ in potentials])
    return [state for potential, state in potentials if potential == max_potential]


def substitution(
    arb_gen: ArbitraryObjectGenerator,
    dep_relation: DependencyRelation,
    arb_obj: ArbitraryObject,
    term: FunctionalTerm | ArbitraryObject,
    stage: Stage,
    supposition: Supposition,
    issue_structure: IssueStructure,
) -> "View":
    """
    Based on definition 4.32
    """

    def Z() -> set[ArbitraryObject]:
        unis = set(
            [
                uni
                for uni in dep_relation.universals
                if dep_relation.triangle(uni, arb_obj)
            ]
        )
        exis = set(
            [
                exi
                for exi in dep_relation.existentials
                if dep_relation.less_sim(exi, arb_obj)
            ]
        )
        return (unis | exis) - {arb_obj}

    assert len(stage.arb_objects & supposition.arb_objects) == 0

    old_T = dep_relation

    new_dep_relation = dep_relation
    new_stage = stage
    subs = arb_gen.redraw(Z())
    new_dep_relation = new_dep_relation.replace(subs)
    new_stage = new_stage.replace(
        cast(dict[ArbitraryObject, Term], subs)
    )

    new_stage = new_stage.replace({arb_obj: term})

    new_dep_relation = new_dep_relation.restriction(set(subs.values()))
    T_prime = old_T.chain(new_dep_relation)

    new_issue_structure = issue_structure.replace(
        cast(dict[ArbitraryObject, Term], subs)
    )
    new_issue_structure = new_issue_structure.replace({arb_obj: term})

    # The following restriction is in the book but should not have been
    # T_prime = T_prime.restriction(new_stage.arb_objects | supposition.arb_objects)

    return View(
        stage=new_stage,
        supposition=supposition,
        dependency_relation=T_prime,
        issue_structure=new_issue_structure,
        is_pre_view=True,
    )


def division_cond(delta: State, supposition: Supposition, stage: Stage):
    for psi in supposition:
        for gamma in stage:
            if delta.issubset(gamma) and psi.issubset(gamma):
                return True
    return False


def division_presupposition(self_stage, other_stage, other_supposition):
    return all(
        division_cond(delta, supposition=other_supposition, stage=self_stage)
        for delta in other_stage
    )


def state_division(
    state: State,
    self_stage: Stage,
    other_stage: Stage,
    other_supposition: Supposition,
) -> State:
    """
    Based on definition 4.38
    """
    if division_presupposition(
        self_stage=self_stage,
        other_stage=other_stage,
        other_supposition=other_supposition,
    ):
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
    else:
        return state


def phi(
    gamma: State,
    delta: State,
    m_prime: set[tuple[FunctionalTerm | ArbitraryObject, ArbitraryObject]],
    other_supposition: Supposition,
) -> bool:
    for ms in powerset(m_prime):
        m_prime_set = set(ms)
        for psi in other_supposition:
            exis = [e for _, e in m_prime_set]
            x = psi | delta.replace({e: t for t, e in m_prime_set})
            if x.issubset(gamma) and (len(exis) == len(set(exis))):
                return True
    return False


def _some_gamma_doesnt_phi(
    self: "View",
    other: "View",
    m_prime: set[tuple[FunctionalTerm | ArbitraryObject, ArbitraryObject]],
):
    for gamma in self.stage:
        if all(
            [not phi(gamma, delta, m_prime, other.supposition) for delta in other.stage]
        ):
            return True
    return False


class View:
    stage: Stage
    supposition: Supposition
    dependency_relation: DependencyRelation
    issue_structure: IssueStructure
    weights: dict[State, Weight]

    def __init__(
        self,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
        weights: dict[State, Weight] = {},
        *,
        is_pre_view=False,
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        self.dependency_relation = dependency_relation
        self.issue_structure = issue_structure
        self.weights = weights
        self.validate(pre_view=is_pre_view)

    def validate(self, *, pre_view: bool = False):

        self.dependency_relation.validate_against_states(
            self.stage | self.supposition, pre_view=pre_view
        )
        for s, w in self.weights.items():
            if s not in self.stage:
                raise ValueError(f"{s} not in {self.stage}")

            w.validate_against_dep_rel(self.dependency_relation)
        
            # Assert weights dict is stage
            # Assert weights only use arbitrary objects in dependency relation
            # TODO: Does this use weight or state?

        if not pre_view:
            self.issue_structure.validate_against_states(self.stage | self.supposition)

    @classmethod
    def from_no_weights(
        cls,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
        *,
        is_pre_view=False,
    ):
        weights = {state: Weight.get_null_weight() for state in stage}
        return View(
            stage=stage,
            supposition=supposition,
            dependency_relation=dependency_relation,
            issue_structure=issue_structure,
            weights=weights,
            is_pre_view=is_pre_view
        )

    @classmethod
    def get_verum(cls):
        verum = SetOfStates({State({})})
        return View(
            stage=verum,
            supposition=verum,
            dependency_relation=DependencyRelation(set(), set(), frozenset()),
            issue_structure=IssueStructure(),
        )

    @classmethod
    def get_falsum(cls):
        verum = SetOfStates({State({})})
        falsum = SetOfStates()
        return View(
            stage=falsum,
            supposition=verum,
            dependency_relation=DependencyRelation(set(), set(), frozenset()),
            issue_structure=IssueStructure(),
        )

    @classmethod
    def with_restriction(
        cls,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
    ):
        return cls(
            stage,
            supposition,
            dependency_relation.restriction((stage | supposition).arb_objects),
            issue_structure.restriction((stage | supposition).atoms),
        )


    @property
    def detailed(self) -> str:
        return f"<View \n  stage={self.stage.detailed} \n  supposition={self.supposition.detailed} \n  dep_rel={self.dependency_relation.detailed} issue_structure={self.issue_structure.detailed} \n>"

    def __repr__(self) -> str:
        if self.is_falsum:
            return "F"
        elif self.is_verum:
            return "T"
        if len(self.dependency_relation.dependencies) == 0:
            dep_string = ""
        else:
            dep_string = f" deps={self.dependency_relation}"
        if len(self.issue_structure) == 0:
            issue_string = ""
        else:
            issue_string = f" issues={self.issue_structure}"
        return f"{self.stage}^{self.supposition}{issue_string}{dep_string}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, View):
            return False
        return (
            self.stage == other.stage
            and self.supposition == other.supposition
            and self.dependency_relation == other.dependency_relation
            and self.issue_structure == other.issue_structure
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.stage,
                self.supposition,
                self.dependency_relation,
                self.issue_structure,
            )
        )

    @property
    def is_verum(self) -> bool:
        return self.stage.is_verum and self.supposition.is_verum

    @property
    def is_falsum(self) -> bool:
        return self.stage.is_falsum and self.supposition.is_verum

    @property
    def stage_supp_arb_objects(self) -> set[ArbitraryObject]:
        return self.stage.arb_objects | self.supposition.arb_objects

    def replace(
        self, replacements: dict[ArbitraryObject, Term]
    ) -> "View":
        new_stage = self.stage.replace(replacements)
        new_supposition = self.supposition.replace(replacements)
        new_issue_structure = self.issue_structure.replace(replacements)
        filtered_replacements = {
            e: n for e, n in replacements.items() if isinstance(n, ArbitraryObject)
        }
        new_dep_relation = self.dependency_relation.replace(filtered_replacements)

        return View(
            stage=new_stage,
            supposition=new_supposition,
            dependency_relation=new_dep_relation.restriction(
                new_stage.arb_objects | new_supposition.arb_objects
            ),
            issue_structure=new_issue_structure,
        )

    def is_equivalent_under_arb_sub(self, other: "View") -> bool:
        """
        Complexity is O((n!)^2*n) where n is average num of exi and unis

        For exis and unis above 9 or 10 (of each) this becomes an issue, below is fine
        """
        self_uni = self.dependency_relation.universals
        self_exi = self.dependency_relation.existentials
        other_uni = other.dependency_relation.universals
        other_exi = other.dependency_relation.existentials

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
                replacements = {
                    **dict(zip(exi_perm, self_exi)),
                    **dict(zip(uni_perm, self_uni)),
                }

                new_view = other.replace(
                    cast(
                        dict[ArbitraryObject, Term],
                        replacements,
                    )
                )
                if new_view == self:
                    return True
        return False

    def issue_matches(
        self, other: "View"
    ) -> set[tuple[FunctionalTerm | ArbitraryObject, FunctionalTerm | ArbitraryObject]]:
        pairs: list[
            tuple[FunctionalTerm | ArbitraryObject, FunctionalTerm | ArbitraryObject]
        ] = []
        for atom_self in self.issue_structure:
            for atom_other in other.issue_structure:
                if atom_self.is_same_emphasis_context(atom_other):
                    pairs.append((atom_self.emphasis_term, atom_other.emphasis_term))

        return set(pairs)

    def _product(
        self, view: "View", inherited_dependencies: DependencyRelation
    ) -> "View":
        """
        Based on definition 4.27
        """
        # Corresponds to line 4
        stage, supposition = stage_supposition_product(
            (self.stage, self.supposition), (view.stage, view.supposition)
        )
        dep_relation = inherited_dependencies.fusion(self.dependency_relation).fusion(
            inherited_dependencies.fusion(view.dependency_relation)
        )
        return View.with_restriction(
            stage=stage,
            supposition=supposition,
            dependency_relation=dep_relation,
            issue_structure=(self.issue_structure | view.issue_structure),
        )

    def product(
        self, view: "View", inherited_dependencies: Optional[DependencyRelation] = None
    ) -> "View":
        """
        Based on definition 4.27
        """
        if inherited_dependencies is None:
            # Corresponds to line 5
            return self._product(view, DependencyRelation(set(), set(), frozenset()))
        else:
            # Corresponds to line 4
            return self._product(view, inherited_dependencies)

    def _sum(self, view: "View", inherited_dependencies: DependencyRelation):
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
        dep_relation = inherited_dependencies.fusion(self.dependency_relation).fusion(
            inherited_dependencies.fusion(view.dependency_relation)
        )
        return View.with_restriction(
            stage=stage,
            supposition=supposition,
            dependency_relation=dep_relation,
            issue_structure=(self.issue_structure | view.issue_structure),
        )

    def sum(
        self, view: "View", inherited_dependencies: Optional[DependencyRelation] = None
    ) -> "View":
        """
        Based on definition 4.28
        """
        if inherited_dependencies is None:
            # Corresponds to line 2
            return self._sum(view, DependencyRelation(set(), set(), frozenset()))
        else:
            # Corresponds to line 1
            return self._sum(view, inherited_dependencies)

    def answer(self, other: "View", verbose: bool = False) -> "View":
        """
        Based on definition 4.30
        """
        if verbose:
            print(f"AnswerInput: External: {self} Internal {other}")
        if not other.supposition.is_verum:
            if verbose:
                print(f"AnswerOutput: {self}")
            return self
        else:
            supposition = self.supposition
            potentials: list[tuple[int, State]] = []
            for s in self.stage:
                potential = SetOfStates({s}).answer_potential(other.stage)
                potentials.append((potential, s))
            stage = SetOfStates(arg_max_states(potentials))

            out = View.with_restriction(
                stage=stage,
                supposition=supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
            )
            if verbose:
                print(f"AnswerOutput: {out}")
            return out

    def negation(self, verbose: bool = False) -> "View":
        """
        Based on definition 4.31
        """
        if verbose:
            print(f"NegationInput: {self}")
        verum = SetOfStates({State({})})
        stage, _ = stage_supposition_product(
            (self.supposition, verum), (self.stage.negation(), verum)
        )
        out = View.with_restriction(
            stage=stage,
            supposition=verum,
            dependency_relation=self.dependency_relation.negation(),
            issue_structure=self.issue_structure.negation(),
        )
        if verbose:
            print(f"NegationOutput: {out}")
        return out

    def merge(self, view: "View", verbose: bool = False) -> "View":
        """
        Based on Definition 4.33
        """

        def _m_prime(
            gamma: State,
        ) -> set[tuple[FunctionalTerm | ArbitraryObject, Universal]]:
            out: set[tuple[FunctionalTerm | ArbitraryObject, Universal]] = set()
            for t, u in self.issue_matches(view):
                if isinstance(
                    u, ArbitraryObject
                ) and not view.dependency_relation.is_existential(u):
                    psi_exists = False
                    for psi in view.supposition:
                        new_psi = psi.replace({u: t})
                        if new_psi.issubset(gamma) and len(psi.difference(gamma)) != 0:
                            psi_exists = True
                            break
                    if psi_exists:
                        out.add((t, u))
            return out

        if verbose:
            print(f"MergeInput: External: {self} Internal {view}")
        if self.stage.is_falsum:
            return self

        if len(self.stage_supp_arb_objects & view.stage_supp_arb_objects) == 0 or (
            view.dependency_relation
            == self.dependency_relation.restriction(view.stage_supp_arb_objects)
        ):
            r_fuse_s = self.dependency_relation.fusion(view.dependency_relation)
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | view.stage_supp_arb_objects
            )
            views_for_sum: list[View] = []
            for gamma in self.stage:
                m_prime = _m_prime(gamma)
                if len(m_prime) == 0:
                    views_for_sum.append(
                        View(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                            self.issue_structure,
                            is_pre_view=True,
                        ).product(view, inherited_dependencies=r_fuse_s)
                    )
                else:
                    product_factors: list[View] = [
                        View(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                            self.issue_structure,
                        )
                    ] + [
                        substitution(
                            arb_gen=arb_gen,
                            dep_relation=r_fuse_s,
                            arb_obj=u,
                            term=t,
                            stage=view.stage,
                            supposition=SetOfStates({State({})}),
                            issue_structure=view.issue_structure,
                        )
                        for t, u in m_prime
                    ]

                    views_for_sum.append(
                        reduce(lambda v1, v2: v1.product(v2, r_fuse_s), product_factors)
                    )
            out = reduce(lambda v1, v2: v1.sum(v2, r_fuse_s), views_for_sum)
            if verbose:
                print(f"MergeOutput: {out}")
            return out
        else:
            if verbose:
                print(f"MergeOutput: {self}")
            return self

    def update(self, view: "View", verbose: bool = False) -> "View":
        """
        Based on Definition 4.34
        """
        if verbose:
            print()
            print(f"UpdateInput: External: {self} Internal {view}")
        arb_gen = ArbitraryObjectGenerator(
            self.stage_supp_arb_objects | view.stage_supp_arb_objects
        )
        shared_objs = self.stage_supp_arb_objects & view.stage_supp_arb_objects
        view = arb_gen.novelise(shared_objs, view)
        out = (
            self.universal_product(view, verbose=verbose)
            .existential_sum(view, verbose=verbose)
            .answer(view, verbose=verbose)
            .merge(view, verbose=verbose)
        )
        if verbose:
            print(f"UpdateOutput: {out}")
            print()
        return out

    def _uni_exi_condition(self, view: "View") -> bool:
        """
        Translated from:
        A(Γ) ∩ A(Θ) = ∅ and (A(R) ∩ A(S) = ∅ or [R]Δ = S)
        """
        expr1 = len(self.stage.arb_objects & self.supposition.arb_objects) == 0
        expr2 = len(self.stage_supp_arb_objects & view.stage_supp_arb_objects) == 0
        expr3 = (
            self.dependency_relation.restriction(view.stage.arb_objects)
            == view.dependency_relation
        )
        return expr1 and (expr2 or expr3)

    def universal_product(self, view: "View", verbose: bool = False) -> "View":
        """
        Based on Definition 4.35
        """

        def _m_prime() -> set[tuple[Universal, FunctionalTerm | ArbitraryObject]]:
            output_set = set()
            for u, t in self.issue_matches(view):
                if isinstance(u, ArbitraryObject) and u in (
                    self.dependency_relation.universals - self.supposition.arb_objects
                ):
                    output_set.add((u, t))
            return output_set

        if verbose:
            print(f"UniProdInput: External: {self} Internal {view}")
        arb_gen = ArbitraryObjectGenerator(
            self.stage_supp_arb_objects | view.stage_supp_arb_objects
        )

        m_prime = _m_prime()
        if len(m_prime) == 0:
            if verbose:
                print(f"UniProdOutput: {self}")
            return self
        if self._uni_exi_condition(view):
            if not view.supposition.is_verum:
                if verbose:
                    print(f"UniProdOutput: {self}")
                return self
            r_fuse_s = self.dependency_relation.fusion(view.dependency_relation)
            product_factors: list[View] = [
                View(
                    stage=SetOfStates({State({})}),
                    supposition=self.supposition,
                    dependency_relation=self.dependency_relation,
                    issue_structure=self.issue_structure,
                    is_pre_view=True,
                )
            ] + [
                substitution(
                    arb_gen=arb_gen,
                    dep_relation=r_fuse_s,
                    arb_obj=u,
                    term=t,
                    stage=self.stage,
                    supposition=SetOfStates({State({})}),
                    issue_structure=self.issue_structure,
                )
                for u, t in m_prime
            ]
            out = reduce(lambda v1, v2: v1.product(v2, r_fuse_s), product_factors)
            if verbose:
                print(f"UniProdOutput: {out}")
            return out
        else:
            if verbose:
                print(f"UniProdOutput: {self}")
            return self

    def existential_sum(self, view: "View", verbose: bool = False) -> "View":
        """
        Based on Definition 4.37
        """

        def _big_union(e: Existential) -> SetOfStates:
            def _big_product(gamma: State) -> SetOfStates:
                def B(gamma: State, e: Existential) -> State:
                    atoms = set()
                    for open_atom in self.issue_structure:
                        for atom in gamma:
                            if open_atom.refers_to_atom(atom):
                                 atoms.add(atom)
                    return State(atoms)

                return reduce(
                    lambda s1, s2: s1 * s2,
                    [SetOfStates({State({x}), State({~x})}) for x in B(gamma, e)],
                )

            assert e in self.stage_supp_arb_objects
            final_sets: list[SetOfStates] = []
            for gamma in self.stage:
                if e in gamma.arb_objects:
                    x_set = State([x for x in gamma if e not in x.arb_objects])
                    for delta in _big_product(gamma):
                        if not delta.issubset(gamma):
                            x_set.union(delta)

                    final_sets.append(SetOfStates({gamma}) | SetOfStates({x_set}))

            return reduce(lambda s1, s2: s1 | s2, final_sets)

        def _m_prime() -> set[tuple[Existential, FunctionalTerm | ArbitraryObject]]:
            output_set = set()
            for e, t in self.issue_matches(view):
                if isinstance(e, ArbitraryObject) and e in (
                    self.dependency_relation.existentials
                    - (self.supposition | view.stage).arb_objects
                ):
                    if not any(
                        d.existential == e
                        for d in self.dependency_relation.dependencies
                    ):
                        output_set.add((e, t))
            return output_set

        if verbose:
            print(f"ExiSumInput: External: {self} Internal {view}")
        if not view.supposition.is_verum:
            if verbose:
                print(f"ExiSumOutput: {self}")
            return self

        if self._uni_exi_condition(view):
            m_prime = _m_prime()
            if len(m_prime) == 0:
                if verbose:
                    print(f"ExiSumOutput: {self}")
                return self
            else:
                arb_gen = ArbitraryObjectGenerator(
                    self.stage_supp_arb_objects | view.stage_supp_arb_objects
                )
                r_fuse_s = self.dependency_relation.fusion(view.dependency_relation)
                sum_result: View = reduce(
                    lambda v1, v2: v1.sum(v2, r_fuse_s),
                    [
                        substitution(
                            arb_gen=arb_gen,
                            dep_relation=r_fuse_s,
                            arb_obj=e,
                            term=t,
                            stage=_big_union(e),
                            supposition=self.supposition,
                            issue_structure=self.issue_structure,
                        )
                        for e, t in m_prime
                    ],
                )
                out = self.sum(sum_result, r_fuse_s)
                if verbose:
                    print(f"ExiSumOutput: {out}")
                return out
        else:
            if verbose:
                print(f"ExiSumOutput: {self}")
            return self

    def division(self, other: "View") -> "View":
        """
        Based on definition 4.38
        """
        if division_presupposition(
            self_stage=self.stage,
            other_stage=other.stage,
            other_supposition=other.supposition,
        ):
            new_stage = SetOfStates(
                [
                    state_division(
                        state=gamma,
                        self_stage=self.stage,
                        other_stage=other.stage,
                        other_supposition=other.supposition,
                    )
                    for gamma in self.stage
                ]
            )
            return View.with_restriction(
                stage=new_stage,
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
            )
        else:
            return self

    def factor(self, other: "View", verbose: bool = False) -> "View":
        """
        Based on definition 4.39
        """
        if verbose:
            print(f"FactorInput: External: {self} Internal {other}")

        def big_intersection(state: State) -> Optional[State]:
            out: list[State] = []
            for t, a in self.issue_matches(other):
                if isinstance(
                    a, ArbitraryObject
                ) and not other.dependency_relation.is_existential(a):
                    replaced_stage = other.stage.replace({a: t})
                    replaced_supposition = other.supposition.replace({a: t})
                    out.append(
                        state_division(
                            state=state,
                            self_stage=self.stage,
                            other_stage=replaced_stage,
                            other_supposition=replaced_supposition,
                        )
                    )
            if len(out) == 0:
                return None
            else:
                return reduce(lambda s1, s2: s1 & s2, out)

        def state_factor(state: State) -> State:
            """
            Based on definition 4.39
            """
            gamma_prime = state_division(
                state=state,
                self_stage=self.stage,
                other_stage=other.stage,
                other_supposition=other.supposition,
            )
            expr = big_intersection(state)
            if expr is None:
                return gamma_prime
            else:
                return gamma_prime & expr

        if not other.is_falsum:
            new_stage = SetOfStates([state_factor(state=gamma) for gamma in self.stage])

        else:
            new_stage = SetOfStates(
                gamma for gamma in self.stage if not gamma.is_primitive_absurd
            )

        out = View.with_restriction(
            stage=new_stage,
            supposition=self.supposition,
            dependency_relation=self.dependency_relation,
            issue_structure=self.issue_structure,
        )
        if verbose:
            print(f"FactorOutput: {out}")
        return out

    def depose(self, verbose: bool = False) -> "View":
        """
        Based on definition 4.45
        """
        if verbose:
            print(f"DeposeInput: {self}")
        verum = SetOfStates({State({})})
        new_stage = self.stage | self.supposition.negation()
        out = View.with_restriction(
            stage=new_stage,
            supposition=verum,
            dependency_relation=self.dependency_relation,
            issue_structure=self.issue_structure.negation(),
        )
        if verbose:
            print(f"DeposeOutput: {out}")
        return out

    def inquire(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 4.43
        """
        if verbose:
            print(f"InquireInput: External: {self} Internal {other}")

        cond1 = len(self.stage_supp_arb_objects & other.stage_supp_arb_objects) == 0
        cond2 = len(other.stage.arb_objects & other.supposition.arb_objects) == 0
        if cond1 and cond2:
            # O case
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | other.stage_supp_arb_objects
            )
            v1 = View.with_restriction(
                stage=SetOfStates({State({})}),
                supposition=other.supposition,
                dependency_relation=other.dependency_relation,
                issue_structure=other.issue_structure,
            )
            v2 = View.with_restriction(
                stage=other.stage.negation(),
                supposition=SetOfStates({State({})}),
                dependency_relation=other.dependency_relation.negation(),
                issue_structure=other.issue_structure.negation(),
            )

            v3 = arb_gen.novelise_all(v2)
            out = self.product(other.sum(v1.product(v3))).factor(View.get_falsum())
        elif other.stage_supp_arb_objects.issubset(self.stage_supp_arb_objects):
            # I case
            view1 = View(
                stage=other.stage,
                supposition=other.supposition,
                dependency_relation=DependencyRelation(set(), set(), frozenset()),
                issue_structure=other.issue_structure,
                is_pre_view=True,
            )
            view2 = View(
                stage=other.stage.negation(),
                supposition=other.supposition,
                dependency_relation=DependencyRelation(set(), set(), frozenset()),
                issue_structure=other.issue_structure.negation(),
                is_pre_view=True,
            )

            out = self.product(view1.sum(view2)).factor(View.get_falsum())
        else:
            out = self

        if verbose:
            print(f"InquireOutput: {out}")
        return out

    def suppose(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 4.44
        """
        if verbose:
            print(f"SupposeInput: External: {self} Internal {other}")

        if len(self.stage_supp_arb_objects & other.stage_supp_arb_objects) == 0:
            # O case
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | other.stage_supp_arb_objects
            )
            v_prime = View(
                stage=self.supposition,
                supposition=SetOfStates({State({})}),
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
            ).product(
                arb_gen.novelise_all(
                    View(
                        stage=other.stage,
                        supposition=other.supposition,
                        dependency_relation=other.dependency_relation.negation(),
                        issue_structure=other.issue_structure,
                    ).depose(verbose=verbose)
                )
            )
            out = (
                View(
                    stage=self.stage,
                    supposition=v_prime.stage,
                    dependency_relation=self.dependency_relation.fusion(
                        v_prime.dependency_relation
                    ),
                    issue_structure=self.issue_structure | v_prime.issue_structure,
                )
                .universal_product(other, verbose=verbose)
                .existential_sum(other, verbose=verbose)
                .answer(other, verbose=verbose)
                .merge(other, verbose=verbose)
            )
        elif (
            (other.stage.arb_objects.issubset(self.stage_supp_arb_objects))
            and (
                self.dependency_relation.restriction(other.stage.arb_objects)
                == other.dependency_relation
            )
            and other.supposition.is_verum
        ):
            # I case
            out = (
                View(
                    stage=self.stage,
                    supposition=self.supposition * other.stage,
                    dependency_relation=self.dependency_relation,
                    issue_structure=self.issue_structure,
                )
                .universal_product(other, verbose=verbose)
                .existential_sum(other, verbose=verbose)
                .answer(other, verbose=verbose)
                .merge(other, verbose=verbose)
            )
        else:
            out = self

        if verbose:
            print(f"SupposeOutput: {out}")
        return out

    def _query_m_prime(
        self, other: "View"
    ) -> set[tuple[FunctionalTerm | ArbitraryObject, ArbitraryObject]]:
        output_set = set()
        for t, e in self.issue_matches(other):
            if isinstance(e, ArbitraryObject) and e in (
                other.dependency_relation.existentials
                - self.dependency_relation.existentials
            ):
                output_set.add((t, e))
        return output_set

    def query(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 4.41
        """

        if verbose:
            print(f"QueryInput: External: {self} Internal {other}")

        if other.dependency_relation.universals.issubset(
            self.dependency_relation.universals
        ):
            m_prime = self._query_m_prime(other)

            D1 = other.dependency_relation.restriction(
                other.stage_supp_arb_objects - self.dependency_relation.existentials
            ).dependencies

            exis_for_pairs = set()
            for t, e in m_prime:
                for t_prime, e_prime in m_prime:
                    if (e == e_prime) and (t != t_prime):
                        exis_for_pairs.add(e)
            D2: set[Dependency] = set()
            for u in self.dependency_relation.universals:
                for exi in exis_for_pairs:
                    D2.add(Dependency(existential=exi, universal=u))

            D3: set[Dependency] = set()
            for t, e in m_prime:
                for u in t.arb_objects:
                    if u in self.dependency_relation.universals:
                        D3.add(Dependency(existential=e, universal=u))

            D4: set[Dependency] = set()
            for t_m, e_m in m_prime:
                for e in t_m.arb_objects:
                    if e in self.dependency_relation.existentials:
                        for dep in self.dependency_relation.dependencies:
                            if e == dep.existential:
                                D4.add(
                                    Dependency(existential=e_m, universal=dep.universal)
                                )

            D5: set[Dependency] = set()
            D5_u_primes = {d.universal for d in D3 | D4}
            for _, e_m in m_prime:
                for u in self.dependency_relation.universals:
                    if all(
                        [
                            self.dependency_relation.triangle(u_prime, u)
                            for u_prime in D5_u_primes
                        ]
                    ):
                        D5.add(Dependency(existential=e_m, universal=u))

            dep_so_far = D1 | D2 | D3 | D4 | D5

            D6: set[Dependency] = set()
            D6_exi_set = (
                other.dependency_relation.existentials
                - self.dependency_relation.existentials
            )
            for e in D6_exi_set:
                for e_prime in D6_exi_set:
                    if other.dependency_relation.less_sim(e, e_prime) and (
                        len([e_m for _, e_m in m_prime if e_m == e_prime]) < 2
                    ):
                        for dep in dep_so_far:
                            if dep.existential == e_prime:
                                D6.add(
                                    Dependency(existential=e, universal=dep.universal)
                                )

            D_s_prime = dep_so_far | D6

            # Stage construction
            if _some_gamma_doesnt_phi(self, other, m_prime=m_prime):
                s1 = SetOfStates({State({})})
            else:
                s1 = SetOfStates()

            s2 = SetOfStates(
                {
                    delta
                    for delta in other.stage
                    if any(
                        phi(gamma, delta, m_prime, other.supposition)
                        for gamma in self.stage
                    )
                }
            )
            new_stage = s1 | s2

            new_dep_rel = self.dependency_relation.fusion(
                DependencyRelation(
                    self.dependency_relation.universals,
                    other.dependency_relation.existentials
                    - self.dependency_relation.existentials,
                    dependencies=D_s_prime,
                )
            )

            out = View.with_restriction(
                stage=new_stage,
                supposition=self.supposition,
                dependency_relation=new_dep_rel,
                issue_structure=self.issue_structure | other.issue_structure,
            )
        else:
            out = self
        if verbose:
            print(f"QueryOutput: {out}")
        return out

    def wh_query(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 4.42
        """

        if verbose:
            print(f"WHQueryInput: External: {self} Internal {other}")

        if other.dependency_relation.universals.issubset(
            self.dependency_relation.universals
        ):
            m_prime = self._query_m_prime(other)

            def psi(gamma: State) -> SetOfStates:
                out: set[State] = set()
                for x in powerset(m_prime):
                    m_prime_set = set(x)
                    if len({e_n for _, e_n in m_prime_set}) == len(m_prime_set):
                        for p in other.supposition:
                            for delta in other.stage:
                                xi = delta.replace(
                                    {e_n: t_n for t_n, e_n in m_prime_set}
                                )
                                if (xi | p).issubset(gamma):
                                    out.add(xi)
                return SetOfStates(out)

            if _some_gamma_doesnt_phi(self, other, m_prime):
                s1 = SetOfStates({State({})})
            else:
                s1 = SetOfStates()

            s2 = SetOfStates()
            for gamma in self.stage:
                s2 |= psi(gamma)

            out = View.with_restriction(
                stage=s1 | s2,
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
            )
        else:
            out = self

        if verbose:
            print(f"WHQueryOutput: {out}")
        return out
