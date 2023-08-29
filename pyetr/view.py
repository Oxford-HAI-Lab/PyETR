__all__ = ["View"]

from functools import reduce
from itertools import permutations
from typing import Optional, cast

from pyetr.issues import IssueStructure
from pyetr.tools import ArbitraryObjectGenerator

from .atom import Atom
from .dependency import Dependency, DependencyRelation
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
    dep_relation: DependencyRelation,
    arb_obj: ArbitraryObject,
    term: Term | ArbitraryObject,
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
        cast(dict[ArbitraryObject, Term | ArbitraryObject], subs)
    )

    new_stage = new_stage.replace({arb_obj: term})

    new_dep_relation = new_dep_relation.restriction(set(subs.values()))
    T_prime = old_T.chain(new_dep_relation)

    new_issue_structure = issue_structure.replace(
        cast(dict[ArbitraryObject, Term | ArbitraryObject], subs)
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


class View:
    stage: Stage
    supposition: Supposition
    dependency_relation: DependencyRelation
    issue_structure: IssueStructure

    def __init__(
        self,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
        *,
        is_pre_view=False,
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        self.dependency_relation = dependency_relation
        self.issue_structure = issue_structure
        self.validate(pre_view=is_pre_view)

    def validate(self, *, pre_view: bool = False):
        self.dependency_relation.validate_against_states(
            self.stage | self.supposition, pre_view=pre_view
        )
        if not pre_view:
            self.issue_structure.validate_against_states(self.stage | self.supposition)

        if self.stage.emphasis_count > 0:
            raise ValueError(f"Stage {self.stage} contains emphasis")
        if self.supposition.emphasis_count > 0:
            raise ValueError(f"Supposition {self.supposition} contains emphasis")

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

    @classmethod
    def from_integrated_emp(
        cls,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
    ):
        atoms = stage.atoms | supposition.atoms
        emphasised_atoms: set[Atom] = set()
        for a in atoms:
            emphasised_atoms |= a.get_issue_atoms()

        return cls(
            stage=stage.excluding_emphasis,
            supposition=supposition.excluding_emphasis,
            dependency_relation=dependency_relation,
            issue_structure=IssueStructure(emphasised_atoms),
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
        self, replacements: dict[ArbitraryObject, Term | ArbitraryObject]
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
                    cast(dict[ArbitraryObject, Term | ArbitraryObject], replacements)
                )
                if new_view == self:
                    return True
        return False

    def issue_matches(
        self, other: "View"
    ) -> set[tuple[Term | ArbitraryObject, Term | ArbitraryObject]]:
        pairs: list[tuple[Term | ArbitraryObject, Term | ArbitraryObject]] = []
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
            dependency_relation=self.dependency_relation,
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
        ) -> set[tuple[Term | ArbitraryObject, Universal]]:
            out: set[tuple[Term | ArbitraryObject, Universal]] = set()
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

        def _m_prime() -> set[tuple[Universal, Term | ArbitraryObject]]:
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
                    for atom in self.issue_structure:
                        atom_excl = atom.excluding_emphasis
                        if atom_excl in gamma:
                            atoms.add(atom_excl)
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

        def _m_prime() -> set[tuple[Existential, Term | ArbitraryObject]]:
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

    def inquire(self, other: "View") -> "View":
        cond1 = len(self.stage_supp_arb_objects & other.stage_supp_arb_objects) == 0
        cond2 = len(other.stage.arb_objects & other.supposition.arb_objects) == 0
        if cond1 and cond2:
            # O case
            return self
        elif other.stage_supp_arb_objects.issubset(self.stage_supp_arb_objects):
            # I case
            # view1 = View(
            #     stage=other.stage,
            #     supposition=other.supposition,
            #     dependency_relation=DependencyRelation.from_arb_objects(
            #         other.stage_supp_arb_objects, dependencies=frozenset()
            #     ),
            #     issue_structure=other.issue_structure,
            # )
            # view2 = View(
            #     stage=other.stage,
            #     supposition=SetOfStates({State({})}),
            #     dependency_relation=DependencyRelation.from_arb_objects(other.stage.arb_objects, dependencies=frozenset()),

            # )
            # self.product().factor(SetOfStates())
            raise NotImplementedError
        else:
            return self
