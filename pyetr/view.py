__all__ = ["View"]

from functools import reduce
from itertools import permutations
from typing import Optional, cast

from pyetr.parsing.common import get_quantifiers

from .atoms import PredicateAtom, equals_predicate
from .atoms.terms import ArbitraryObject, FunctionalTerm, RealNumber, Term
from .dependency import Dependency, DependencyRelation
from .issues import IssueStructure
from .stateset import SetOfStates, Stage, State, Supposition
from .tools import ArbitraryObjectGenerator, powerset
from .weight import Weight, Weights


def get_subset(
    stage_external: SetOfStates, supposition_internal: SetOfStates
) -> SetOfStates:
    out_set = set()
    for state_stage_ext in stage_external:
        for supp_state in supposition_internal:
            if supp_state.issubset(state_stage_ext):
                out_set.add(state_stage_ext)
    return SetOfStates(out_set)


Existential = ArbitraryObject
Universal = ArbitraryObject


def stage_function_product(
    stage_supposition_external: tuple[Stage, Weights],
    stage_supposition_internal: tuple[Stage, Supposition, Weights],
) -> tuple[Stage, Weights]:
    """
    Definition 5.15, p208
    """
    stage_external, weights_external = stage_supposition_external
    stage_internal, supposition_internal, weights_internal = stage_supposition_internal

    subset = get_subset(stage_external, supposition_internal)
    not_subset = stage_external.difference(subset)
    f_prime = weights_external.in_set_of_states(not_subset)
    result_stage = not_subset | (subset * stage_internal)

    f = weights_external.in_set_of_states(subset)
    final_weights = f_prime + (f * weights_internal)

    return result_stage, final_weights


def substitution(
    arb_gen: ArbitraryObjectGenerator,
    dep_relation: DependencyRelation,
    arb_obj: ArbitraryObject,
    term: Term,
    stage: Stage,
    supposition: Supposition,
    issue_structure: IssueStructure,
    weights: Optional[Weights],
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
    subs = arb_gen.redraw(Z())
    new_dep_relation = new_dep_relation.replace(subs)

    if weights is None:
        weights = Weights.get_null_weights(stage)

    new_weights = Weights({})

    for state in stage:
        new_state = state.replace(cast(dict[ArbitraryObject, Term], subs))
        new_state = new_state.replace({arb_obj: term})
        new_weight = weights[state].replace(cast(dict[ArbitraryObject, Term], subs))
        new_weight = new_weight.replace({arb_obj: term})

        new_weights._adding(new_state, new_weight)

    new_stage = SetOfStates(new_weights.keys())

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
        weights=new_weights,
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
    gamma_weight: Weight,
    delta_weight: Weight,
) -> bool:
    for ms in powerset(m_prime):
        m_prime_set = set(ms)
        for psi in other_supposition:
            exis = [e for _, e in m_prime_set]
            replacements: dict[ArbitraryObject, Term] = {e: t for t, e in m_prime_set}
            delta_rep = delta.replace(replacements)
            x = psi | delta_rep
            weight_condition = (
                delta_weight.is_null
                or delta_weight.replace(replacements) == gamma_weight
            )
            if x.issubset(gamma) and (len(exis) == len(set(exis))) and weight_condition:
                return True
    return False


def _some_gamma_doesnt_phi(
    self: "View",
    other: "View",
    m_prime: set[tuple[FunctionalTerm | ArbitraryObject, ArbitraryObject]],
):
    for gamma in self.stage:
        if all(
            [
                not phi(
                    gamma,
                    delta,
                    m_prime,
                    other.supposition,
                    self.weights[gamma],
                    other.weights[delta],
                )
                for delta in other.stage
            ]
        ):
            return True
    return False


class View:
    _stage: Stage
    _supposition: Supposition
    _dependency_relation: DependencyRelation
    _issue_structure: IssueStructure
    _weights: Weights

    def __init__(
        self,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
        weights: Optional[Weights],
        *,
        is_pre_view=False,
    ) -> None:
        self._stage = stage
        self._supposition = supposition
        self._dependency_relation = dependency_relation
        self._issue_structure = issue_structure.restriction(
            stage.atoms | supposition.atoms
        )
        if weights is None:
            self._weights = Weights.get_null_weights(stage)
        else:
            self._weights = weights
        self.validate(pre_view=is_pre_view)

    @property
    def stage(self) -> Stage:
        return self._stage

    @property
    def supposition(self) -> Supposition:
        return self._supposition

    @property
    def dependency_relation(self) -> DependencyRelation:
        return self._dependency_relation

    @property
    def issue_structure(self) -> IssueStructure:
        return self._issue_structure

    @property
    def weights(self) -> Weights:
        return self._weights

    def validate(self, *, pre_view: bool = False):
        self.dependency_relation.validate_against_states(
            (self.stage | self.supposition).arb_objects | self.weights.arb_objects,
            pre_view=pre_view,
        )

        for s, w in self.weights.items():
            if s not in self.stage:
                raise ValueError(f"{s} not in {self.stage}")

            w.validate_against_dep_rel(self.dependency_relation)

        for state in self.stage:
            if state not in self.weights:
                raise ValueError(f"{state} not in {self.weights}")
        if not pre_view:
            self.issue_structure.validate_against_states(self.stage | self.supposition)

    @classmethod
    def get_verum(cls):
        verum = SetOfStates({State({})})
        return View(
            stage=verum,
            supposition=verum,
            dependency_relation=DependencyRelation(set(), set(), frozenset()),
            issue_structure=IssueStructure(),
            weights=None,
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
            weights=None,
        )

    @classmethod
    def with_restriction(
        cls,
        stage: Stage,
        supposition: Supposition,
        dependency_relation: DependencyRelation,
        issue_structure: IssueStructure,
        weights: Optional[Weights],
    ):
        new_dep_rel = dependency_relation.restriction((stage | supposition).arb_objects)
        if weights is None:
            new_weights = None
        else:
            new_weights = Weights(
                {
                    s: w.restriction(new_dep_rel.universals | new_dep_rel.existentials)
                    for s, w in weights.items()
                    if s in stage
                }
            )
        return cls(
            stage=stage,
            supposition=supposition,
            dependency_relation=new_dep_rel,
            issue_structure=issue_structure.restriction((stage | supposition).atoms),
            weights=new_weights,
        )

    @property
    def detailed(self) -> str:
        return f"<View \n  stage={self.stage.detailed} \n  supposition={self.supposition.detailed} \n  dep_rel={self.dependency_relation.detailed} issue_structure={self.issue_structure.detailed} weights={self.weights.detailed} \n>"

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

        quants = get_quantifiers(
            self.dependency_relation.universals | self.dependency_relation.existentials,
            self.dependency_relation,
        )
        quant_str = " ".join([i.to_string() for i in quants])
        end_str = " " if len(quant_str) > 0 else ""
        return f"{quant_str}{end_str}{self.weights}^{self.supposition}{issue_string}{dep_string}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, View):
            return False
        return (
            self.stage == other.stage
            and self.supposition == other.supposition
            and self.dependency_relation == other.dependency_relation
            and self.issue_structure == other.issue_structure
            and self.weights == other.weights
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.stage,
                self.supposition,
                self.dependency_relation,
                self.issue_structure,
                self.weights,
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

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "View":
        new_stage_set: set[State] = set()
        new_weights: Weights = Weights({})
        for state in self.stage:
            new_state = state.replace(replacements)
            new_stage_set.add(new_state)
            current_weight = self.weights[state]
            new_weight = current_weight.replace(replacements)
            new_weights._adding(new_state, new_weight)

        new_stage = SetOfStates(new_stage_set)

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
            weights=new_weights,
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

    def issue_matches(self, other: "View") -> set[tuple[Term, Term]]:
        pairs: list[tuple[Term, Term]] = []
        for t1, open_atom_self in self.issue_structure:
            for t2, open_atom_other in other.issue_structure:
                if (
                    open_atom_self == open_atom_other
                    or open_atom_self == ~open_atom_other
                ):
                    pairs.append((t1, t2))

        return set(pairs)

    def _product(
        self, view: "View", inherited_dependencies: DependencyRelation
    ) -> "View":
        """
        Based on definition 4.27
        """
        # Corresponds to line 4
        stage, weights = stage_function_product(
            (self.stage, self.weights), (view.stage, view.supposition, view.weights)
        )
        dep_relation = inherited_dependencies.fusion(self.dependency_relation).fusion(
            inherited_dependencies.fusion(view.dependency_relation)
        )
        return View.with_restriction(
            stage=stage,
            supposition=self.supposition,
            dependency_relation=dep_relation,
            issue_structure=(self.issue_structure | view.issue_structure),
            weights=weights,
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
        Based on definition 5.14, p208

        (Γ_f + Δ_g) = (Γ ∪ Δ)_h, where h(γ) = f(γ) + g(γ)
        Γ^θ_fRI ⊕ᵀ Δ^{0}_gSJ = (Γ_f + Δ_g)^θ_(T⋈R)⋈(T⋈S),I∪J

        This is where the subprocedure takes place.
        """
        if self.supposition != view.supposition:
            raise ValueError(
                f"Invalid sum on {self.supposition} and {view.supposition}"
            )

        supposition = self.supposition

        # Γ ∪ Δ
        stage = self.stage | view.stage

        # (T⋈R)⋈(T⋈S)
        dep_relation = inherited_dependencies.fusion(self.dependency_relation).fusion(
            inherited_dependencies.fusion(view.dependency_relation)
        )

        # h(γ) = f(γ) + g(γ)
        new_weights: Weights = self.weights + view.weights

        return View.with_restriction(
            stage=stage,
            supposition=supposition,
            dependency_relation=dep_relation,
            issue_structure=(self.issue_structure | view.issue_structure),
            weights=new_weights,
        )

    def sum(
        self, view: "View", inherited_dependencies: Optional[DependencyRelation] = None
    ) -> "View":
        """
        Based on definition 5.14, p208

        Γ^θ_fRI ⊕ᵀ Δ^{0}_gSJ

        Args:
            self (View): Γ^θ_fRI
            view (View): Δ^{0}_gSJ
            inherited_dependencies (Optional[DependencyRelation], optional): T. Defaults to an empty
                dependency relation.

        Returns:
            View: The result of the sum calculation
        """
        if inherited_dependencies is None:
            # Corresponds to line 2
            return self._sum(view, DependencyRelation(set(), set(), frozenset()))
        else:
            # Corresponds to line 1
            return self._sum(view, inherited_dependencies)

    def atomic_answer(self, other: "View", verbose: bool = False) -> "View":
        """
        Based on definition 5.12, p206

        Γ^θ_fRI[Δ^{0}_gSJ]^𝓐A = argmax_γ∈Γ(Δ[{{p} : p ∈ γ}]^𝓐P)_f |^θ_RI

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the atomic answer calculation
        """
        if verbose:
            print(f"AtomicAnswerInput: External: {self} Internal {other}")
        if not other.supposition.is_verum:
            if verbose:
                print(f"AtomicAnswerOutput: {self}")
            return self
        else:

            def _arg_max(potentials: list[tuple[int, State]]) -> list[State]:
                if len(potentials) == 0:
                    return []
                max_potential = max([potential for potential, _ in potentials])
                return [
                    state
                    for potential, state in potentials
                    if potential == max_potential
                ]

            supposition = self.supposition
            potentials: list[tuple[int, State]] = []

            # γ∈Γ
            for gamma in self.stage:
                # Δ[{{p} : p ∈ γ}]^𝓐P # TODO: Seems different? now fixed?
                potential = other.stage.atomic_answer_potential(
                    SetOfStates({State({p}) for p in gamma})
                )
                potentials.append((potential, gamma))
            stage = SetOfStates(_arg_max(potentials))

            out = View.with_restriction(
                stage=stage,
                supposition=supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
                weights=self.weights,
            )
            if verbose:
                print(f"AtomicAnswerOutput: {out}")
            return out

    def equilibrium_answer(self, other: "View", verbose: bool = False) -> "View":
        """
        Based on definition 5.10, p205

        Γ^θ_fRI[Δ^{0}_gSJ]^𝔼A

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the equilibrium answer calculation
        """
        if verbose:
            print(f"EquilibriumAnswerInput: External: {self} Internal {other}")
        if not other.supposition.is_verum:
            if verbose:
                print(f"EquilibriumAnswerOutput: {self}")
            return self
        else:

            def _arg_max(ps: list[tuple[FunctionalTerm, State]]) -> list[State]:
                if len(ps) == 0:
                    return []

                nums = []
                for p, _ in ps:
                    assert isinstance(p.f, RealNumber)
                    nums.append(p.f.num)
                max_potential = max(nums)

                new_states = []
                for p, state in ps:
                    assert isinstance(p.f, RealNumber)
                    if p.f.num == max_potential:
                        new_states.append(state)
                return new_states

            supposition = self.supposition
            potentials: list[tuple[FunctionalTerm, State]] = []
            for gamma in self.stage:
                potential = other.stage.equilibrium_answer_potential(
                    SetOfStates({State({p}) for p in gamma}), other.weights
                )
                potentials.append((potential, gamma))
            if verbose:
                print(f"Potentials: {potentials}")
            if not all([isinstance(ft.f, RealNumber) for ft, _ in potentials]):
                return self
            stage = SetOfStates(_arg_max(potentials))

            out = View.with_restriction(
                stage=stage,
                supposition=supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
                weights=self.weights,
            )
            if verbose:
                print(f"EquilibriumAnswerOutput: {out}")
            return out

    def answer(self, other: "View", verbose: bool = False) -> "View":
        """
        Based on definition 5.13, p206

        Γ^θ_fRI[Δ^{0}_gSJ]^A

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the answer calculation
        """
        if verbose:
            print(f"AnswerInput: External: {self} Internal {other}")
        out = self.equilibrium_answer(other, verbose=verbose).atomic_answer(
            other, verbose=verbose
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
        stage = self.supposition * self.stage.negation()
        out = View.with_restriction(
            stage=stage,
            supposition=verum,
            dependency_relation=self.dependency_relation.negation(),
            issue_structure=self.issue_structure.negation(),
            weights=None,
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
        ) -> set[tuple[Term, Universal]]:
            out: set[tuple[Term, Universal]] = set()
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
                        View.with_restriction(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                            self.issue_structure,
                            self.weights,
                        ).product(view, inherited_dependencies=r_fuse_s)
                    )
                else:
                    product_factors: list[View] = [
                        View.with_restriction(
                            SetOfStates({gamma}),
                            self.supposition,
                            self.dependency_relation,
                            self.issue_structure,
                            self.weights,
                        ),
                        view,
                    ] + [
                        substitution(
                            arb_gen=arb_gen,
                            dep_relation=r_fuse_s,
                            arb_obj=u,
                            term=t,
                            stage=view.stage,
                            supposition=SetOfStates({State({})}),
                            issue_structure=view.issue_structure,
                            weights=view.weights,
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
                View.with_restriction(
                    stage=SetOfStates({State({})}),
                    supposition=self.supposition,
                    dependency_relation=self.dependency_relation,
                    issue_structure=self.issue_structure,
                    weights=None,
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
                    weights=self.weights,
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

        def _big_union(e: Existential) -> Weights:
            def _big_product(gamma: State) -> SetOfStates:
                def B(gamma: State, e: Existential) -> State:
                    atoms = set()
                    for t, open_atom in self.issue_structure:
                        formed_atom = open_atom(t)
                        for atom in gamma:
                            if formed_atom == atom:
                                atoms.add(atom)
                    return State(atoms)

                return reduce(
                    lambda s1, s2: s1 * s2,
                    [SetOfStates({State({x}), State({~x})}) for x in B(gamma, e)],
                )

            assert e in self.stage_supp_arb_objects
            final_sets: list[SetOfStates] = []

            new_weights: dict[State, Weight] = {}
            for gamma in self.stage:
                if e in gamma.arb_objects:
                    new_weights[gamma] = self.weights[gamma]
                    proto_sets: set[State] = set()
                    x_set = State([x for x in gamma if e not in x.arb_objects])
                    for delta in _big_product(gamma):
                        if not delta.issubset(gamma):
                            proto_sets.add(x_set.union(delta))
                    final_sets.append(SetOfStates({gamma}) | SetOfStates(proto_sets))

            output_set = reduce(lambda s1, s2: s1 | s2, final_sets)

            final_weights = Weights(new_weights) + Weights.get_null_weights(output_set)
            return final_weights

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
                # TODO: Is this the null weights?
                to_sum: list["View"] = []
                for e, t in m_prime:
                    weights = _big_union(e)
                    stage = SetOfStates(weights.keys())
                    to_sum.append(
                        substitution(
                            arb_gen=arb_gen,
                            dep_relation=r_fuse_s,
                            arb_obj=e,
                            term=t,
                            stage=stage,
                            supposition=self.supposition,
                            issue_structure=self.issue_structure,
                            weights=weights,
                        )
                    )
                sum_result: View = reduce(
                    lambda v1, v2: v1.sum(v2, r_fuse_s),
                    to_sum,
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
            new_weights: Weights = Weights({})
            for gamma in self.stage:
                new_state = state_division(
                    state=gamma,
                    self_stage=self.stage,
                    other_stage=other.stage,
                    other_supposition=other.supposition,
                )
                new_weight = self.weights[gamma]
                new_weights._adding(new_state, new_weight)

            new_stage = SetOfStates(new_weights.keys())

            return View.with_restriction(
                stage=new_stage,
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
                weights=new_weights,
            )
        else:
            return self

    def factor(
        self,
        other: "View",
        verbose: bool = False,
        absurd_states: Optional[list[State]] = None,
    ) -> "View":
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

        def identity_factor_condition() -> bool:
            if len(other.stage) != 1:
                return False
            first_state = next(iter(other.stage))
            if len(first_state) != 1:
                return False
            first_atom = next(iter(first_state))
            if not isinstance(first_atom, PredicateAtom):
                return False
            if first_atom.predicate != equals_predicate:
                return False
            if len(other.issue_structure) != 1:
                return False
            if not other.supposition.is_verum:
                return False
            if (
                self.dependency_relation.restriction(
                    other.dependency_relation.universals
                    | other.dependency_relation.existentials
                )
                != other.dependency_relation
            ):
                return False
            return True

        if other.is_falsum:
            if verbose:
                print("Contradiction factor")
            new_weights = self.weights
            new_stage = SetOfStates(
                gamma
                for gamma in self.stage
                if not gamma.is_primitive_absurd(absurd_states)
            )
        elif identity_factor_condition():
            if verbose:
                print("Identity factor")
            first_state = next(iter(other.stage))
            first_atom = next(iter(first_state))
            assert isinstance(first_atom, PredicateAtom)
            assert len(first_atom.terms) == 2
            t1, t2 = first_atom.terms
            expr1_states = SetOfStates(
                {gamma for gamma in self.stage if first_atom not in gamma}
            )
            expr1_weights = self.weights.in_set_of_states(expr1_states)

            expr2_weights: Weights = Weights({})
            for gamma in self.stage:
                if first_atom in gamma:
                    gamma_prime = gamma.replace_term(t2, t1)
                    expr2_weights._adding(
                        gamma_prime, self.weights[gamma].replace_term(t2, t1)
                    )

            new_stage = expr1_states | SetOfStates(expr2_weights.keys())
            new_weights = expr1_weights + expr2_weights
        else:
            if verbose:
                print("Central case factor")
            new_weights = Weights({})
            for gamma in self.stage:
                new_weights._adding(state_factor(state=gamma), self.weights[gamma])
            new_stage = SetOfStates(new_weights.keys())

        out = View.with_restriction(
            stage=new_stage,
            supposition=self.supposition,
            dependency_relation=self.dependency_relation,
            issue_structure=self.issue_structure,
            weights=new_weights,
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
        sup_negation = self.supposition.negation()
        new_stage = self.stage | sup_negation
        new_weights = self.weights + Weights.get_null_weights(sup_negation)
        out = View.with_restriction(
            stage=new_stage,
            supposition=verum,
            dependency_relation=self.dependency_relation,
            issue_structure=self.issue_structure.negation(),
            weights=new_weights,
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
            if verbose:
                print("Inquire, O case")
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | other.stage_supp_arb_objects
            )
            v1 = View.with_restriction(
                stage=SetOfStates({State({})}),
                supposition=other.supposition,
                dependency_relation=other.dependency_relation,
                issue_structure=other.issue_structure,
                weights=None,
            )
            v2 = View.with_restriction(
                stage=other.stage.negation(),
                supposition=SetOfStates({State({})}),
                dependency_relation=other.dependency_relation.negation(),
                issue_structure=other.issue_structure.negation(),
                weights=None,
            )
            v3 = arb_gen.novelise_all(v2)
            out = self.product(other.sum(v1.product(v3))).factor(View.get_falsum())
        elif other.stage_supp_arb_objects.issubset(
            self.stage_supp_arb_objects
        ) and other.dependency_relation == self.dependency_relation.restriction(
            self.stage_supp_arb_objects
        ):
            if verbose:
                print("Inquire, I case")
            # I case
            view2 = View.with_restriction(
                stage=other.stage.negation(),
                supposition=other.supposition,
                dependency_relation=other.dependency_relation,
                issue_structure=other.issue_structure.negation(),
                weights=None,
            )
            out = self.product(other.sum(view2)).factor(View.get_falsum())
        else:
            if verbose:
                print("Inquire, pass-through case")
            out = self

        if verbose:
            print(f"InquireOutput: {out}")
        return out

    def suppose(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition A.76
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
                weights=None,
                is_pre_view=True,
            ).product(
                arb_gen.novelise_all(
                    View(
                        stage=other.stage,
                        supposition=other.supposition,
                        dependency_relation=other.dependency_relation.negation(),
                        issue_structure=other.issue_structure,
                        weights=other.weights,
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
                    weights=self.weights,
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
                    weights=self.weights,
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
            s2_weights: Weights = Weights({})
            for delta in other.stage:
                for gamma in self.stage:
                    if phi(
                        gamma,
                        delta,
                        m_prime,
                        other.supposition,
                        self.weights[gamma],
                        other.weights[delta],
                    ):
                        other_weight = other.weights[delta]
                        if other_weight.is_null:
                            s2_weights._adding(delta, self.weights[gamma])
                        else:
                            s2_weights._adding(delta, other_weight)

            s2 = SetOfStates(s2_weights.keys())
            new_stage = s1 | s2
            new_weights = Weights.get_null_weights(s1) + s2_weights
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
                weights=new_weights,
            )
        else:
            out = self
        if verbose:
            print(f"QueryOutput: {out}")
        return out

    def which(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 4.42
        """

        if verbose:
            print(f"WhichInput: External: {self} Internal {other}")

        if other.dependency_relation.universals.issubset(
            self.dependency_relation.universals
        ):
            m_prime = self._query_m_prime(other)

            def xi_fka_psi(gamma: State) -> Weights:
                weights: Weights = Weights({})
                for x in powerset(m_prime):
                    m_prime_set = set(x)
                    replacements: dict[ArbitraryObject, Term] = {
                        e_n: t_n for t_n, e_n in m_prime_set
                    }
                    if len({e_n for _, e_n in m_prime_set}) == len(m_prime_set):
                        for p in other.supposition:
                            for delta in other.stage:
                                xi = delta.replace(replacements)
                                if (xi | p).issubset(gamma):
                                    w = other.weights[delta].replace(replacements)
                                    # TODO: This is not exactly what's in the book, because here we count
                                    # each w.xi possibly multiple times, whereas the book (a little ambiguously,
                                    # but interpreted strictly) collapses the multiplicities to 1.
                                    weights._adding(xi, w)
                return weights

            if _some_gamma_doesnt_phi(self, other, m_prime):
                H = SetOfStates({State({})})
            else:
                H = SetOfStates()

            s2_weights: Weights = Weights({})
            for gamma in self.stage:
                s2_weights += xi_fka_psi(gamma)

            new_weights = Weights.get_null_weights(H) + s2_weights
            out = View.with_restriction(
                stage=SetOfStates(new_weights.keys()),
                supposition=self.supposition,
                dependency_relation=self.dependency_relation,
                issue_structure=self.issue_structure,
                weights=new_weights,
            )
        else:
            out = self

        if verbose:
            print(f"WhichOutput: {out}")
        return out
