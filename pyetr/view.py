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


def get_subset(big_gamma: SetOfStates, big_psi: SetOfStates) -> SetOfStates:
    """
    Produces the subset of states in big gamma and big psi that satisfy ψ⊆γ

    {γ ∃γ ∈ Γ ∃ψ ∈ Ψ Ψ.ψ⊆γ}

    Args:
        big_gamma (SetOfStates): The states in the stage of the external (Γ)
        big_psi (SetOfStates): The states in the supposition of the internal (Ψ)

    Returns:
        SetOfStates: The subset of states that satisfy this.
    """
    out_set = set()
    for gamma in big_gamma:
        for psi in big_psi:
            # .ψ⊆γ
            if psi.issubset(gamma):
                out_set.add(gamma)
    return SetOfStates(out_set)


Existential = ArbitraryObject
Universal = ArbitraryObject


def stage_function_product(
    stage_supposition_external: tuple[Stage, Weights],
    stage_supposition_internal: tuple[Stage, Supposition, Weights],
) -> tuple[Stage, Weights]:
    """
    Definition 5.15, p208

    Γ_f ⨂ Δ^{Ψ}_g = P + Σ_γ∈(Γ＼P) Σ_δ∈Δ {f(γ) x g(δ)).(γ∪δ)}
    where P = {f(γ).γ∈Γ |¬∃ψ ∈ Ψ.ψ⊆γ}
    """
    big_gamma, f_gamma = stage_supposition_external
    stage_internal, big_psi, g_delta = stage_supposition_internal

    gamma_new = get_subset(big_gamma, big_psi)
    P = big_gamma.difference(gamma_new)
    P_weights = f_gamma.in_set_of_states(P)

    # f(γ).(γ∪δ)
    f_gamma_new = f_gamma.in_set_of_states(gamma_new)

    result_stage = P | (gamma_new * stage_internal)
    final_weights = P_weights + (f_gamma_new * g_delta)

    return result_stage, final_weights


def Z(T: DependencyRelation, a: ArbitraryObject) -> set[ArbitraryObject]:
    """
    Based on definition A.43, p306 (TODO: Where in book?)

    Z(T,a) = {u ∈ U_T : u ◁_T a} ∪ {e ∈ E_T : e ≲_T a} – {a}

    Args:
        T (DependencyRelation): T
        a (ArbitraryObject): a

    Returns:
        set[ArbitraryObject]: The set of arbitrary objects resulting from Z
    """
    # {u ∈ U_T : u ◁_T a}
    unis = set([uni for uni in T.universals if T.triangle(uni, a)])
    # {e ∈ E_T : e ≲_T a}
    exis = set([exi for exi in T.existentials if T.less_sim(exi, a)])
    return (unis | exis) - {a}


def substitution(
    arb_gen: ArbitraryObjectGenerator,
    dep_relation: DependencyRelation,
    arb_obj: ArbitraryObject,
    term: Term,
    stage: Stage,
    supposition: Supposition,
    issue_structure: IssueStructure,
    weights: Weights,
) -> "View":
    """
    Based on definition A.43, p306 (TODO: Where in book?)
    Weight section based on definition 5.25, p221

    # Note, in book it returns a tuple
    Sub^T_<t,a> (Γ^Θ_I) = View(
        stage = Γ[ν₁]_Z(T,a) [t/a],
        supposition = Θ,
        dep_rel = T ⋊ ([T]_Z(T,a)[t/a]),
        issues = I[ν₁]_Z(T,a) [t/a],
        weights = ? TODO: No expr found
    )

    Args:
        arb_gen (ArbitraryObjectGenerator): The generator of arbitrary objects used for novelisation.
        dep_relation (DependencyRelation): T, the dependency relation
        arb_obj (ArbitraryObject): a
        term (Term): t
        stage (Stage): Γ
        supposition (Supposition): Θ
        issue_structure (IssueStructure): I
        weights (Weights): f? TODO: What's this?

    Returns:
        View: The view with values substituted.
    """
    assert len(stage.arb_objects & supposition.arb_objects) == 0

    subs = arb_gen.redraw(Z(T=dep_relation, a=arb_obj))

    # T' = T ⋊ ([T]_Z(T,a)[t/a])
    T_prime = dep_relation.chain(
        dep_relation.replace(subs).restriction(set(subs.values()))
    )

    new_weights = Weights()
    for state in stage:
        # Γ[ν₁]_Z(T,a) [t/a]
        new_state = state.replace(cast(dict[ArbitraryObject, Term], subs)).replace(
            {arb_obj: term}
        )
        new_weight = (
            weights[state]
            .replace(cast(dict[ArbitraryObject, Term], subs))
            .replace({arb_obj: term})
        )
        new_weights._adding(new_state, new_weight)

    new_stage = SetOfStates(new_weights.keys())

    # I[ν₁]_Z(T,a) [t/a]
    new_issue_structure = issue_structure.replace(
        cast(dict[ArbitraryObject, Term], subs)
    ).replace({arb_obj: term})

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


def division_presupposition(
    self_stage: Stage, other_stage: Stage, other_supposition: Supposition
) -> bool:
    """
    Based on definition 4.38, p168

    ∀δ_∈Δ ∃ψ_∈Ψ ∃γ∈Γ (δ ⊆ γ ∧ ψ ⊆ γ)

    Args:
        self_stage (Stage): Γ
        other_stage (Stage): Δ
        other_supposition (Supposition): Ψ

    Returns:
        bool: True if the presupposition is satisified
    """

    def division_cond(delta):
        """
        ∃ψ_∈Ψ ∃γ∈Γ (δ ⊆ γ ∧ ψ ⊆ γ)
        """
        return any(
            delta.issubset(gamma) and psi.issubset(gamma)
            for psi in other_supposition
            for gamma in self_stage
        )

    return all(division_cond(delta) for delta in other_stage)


def state_division(
    state: State,
    self_stage: Stage,
    other_stage: Stage,
    other_supposition: Supposition,
) -> State:
    """
    Based on definition 4.38, p168

    If DIVISION_PRESUPPOSITION:

        γ⌀_Γ Δ^Ψ = γ – ıδ(δ ∈ Δ ∧ δ ⊆ γ ∧ ∃ψ_∈Ψ (ψ ⊆ γ))
    Else:
        γ⌀_Γ Δ^Ψ = γ

    Args:
        state (State): γ
        self_stage (Stage): Γ
        other_stage (Stage): Δ
        other_supposition (Supposition): Ψ

    Returns:
        State: The divided state.
    """
    if division_presupposition(
        self_stage=self_stage,
        other_stage=other_stage,
        other_supposition=other_supposition,
    ):
        # γ – ıδ(δ ∈ Δ ∧ δ ⊆ γ ∧ ∃ψ_∈Ψ (ψ ⊆ γ))

        # ıδ(δ ∈ Δ ∧ δ ⊆ γ ∧ ∃ψ_∈Ψ (ψ ⊆ γ))
        delta_that_meet_cond: list[State] = []
        # δ ∈ Δ
        for delta in other_stage:
            # δ ⊆ γ ∧ ∃ψ_∈Ψ (ψ ⊆ γ)
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
    m_prime: set[tuple[Term, ArbitraryObject]],
    other_supposition: Supposition,
    gamma_weight: Weight,
    delta_weight: Weight,
) -> bool:
    """
    Based on definition 5.19, p211 and 5.33, p232

    Φ(γ, δ) = ∃ψ_∈Ψ ∃n≥0 ∃<t₁,e₁>,...,<tₙ,eₙ>∈M'ij (∀i,j.e_i = e_j -> i=j) ∧ (ψ∪δ[t₁/e₁,...,tₙ/eₙ] ⊆ γ) ∧ (f(γ) = g(δ)[t₁/e₁,...] ∨ g(δ) =《》)

    Args:
        gamma (State): γ
        delta (State): δ
        m_prime (set[tuple[Term, ArbitraryObject]]): M'ij
        other_supposition (Supposition): Ψ
        gamma_weight (Weight): f(γ)
        delta_weight (Weight): g(δ)

    Returns:
        bool: Φ(γ, δ)
    """
    # ∃n≥0
    for m_prime_set in powerset(m_prime):
        # ∃ψ_∈Ψ
        for psi in other_supposition:
            # ∃<t₁,e₁>,...,<tₙ,eₙ>∈M'ij
            exis = [e for _, e in m_prime_set]
            # (∀i,j.e_i = e_j -> i=j)
            first_cond = len(exis) == len(set(exis))

            # [t₁/e₁,...,tₙ/eₙ]
            replacements: dict[ArbitraryObject, Term] = {e: t for t, e in m_prime_set}
            # δ[t₁/e₁,...,tₙ/eₙ]
            delta_new = delta.replace(replacements)
            # ψ∪δ[t₁/e₁,...,tₙ/eₙ]
            x = psi | delta_new
            # (ψ∪δ[t₁/e₁,...,tₙ/eₙ] ⊆ γ)
            second_cond = x.issubset(gamma)

            # (f(γ) = g(δ)[t₁/e₁,...] ∨ g(δ) =《》)
            third_cond = (
                delta_weight.is_null
                or delta_weight.replace(replacements) == gamma_weight
            )

            if first_cond and second_cond and third_cond:
                return True
    return False


def _H(
    self: "View", other: "View", m_prime: set[tuple[Term, ArbitraryObject]]
) -> SetOfStates:
    """
    If ∃γ ∈ Γ.∀δ ∈ Δ.¬Φ(γ, δ):
        H = {0}
    Else:
        H = {}

    Args:
        self (View): Γ
        other (View): Δ
        m_prime (set[tuple[Term, ArbitraryObject]]): M'ij

    Returns:
        SetOfStates: H
    """
    # ∃γ ∈ Γ.∀δ ∈ Δ.¬Φ(γ, δ)
    some_gamma_doesnt_phi = any(
        all(
            [
                # ¬Φ(γ, δ)
                not phi(
                    gamma,
                    delta,
                    m_prime,
                    other.supposition,
                    self.weights[gamma],
                    other.weights[delta],
                )
                for delta in other.stage  # ∀δ ∈ Δ
            ]
        )
        for gamma in self.stage  # ∃γ ∈ Γ
    )
    if some_gamma_doesnt_phi:
        return SetOfStates({State({})})
    else:
        return SetOfStates()


def issue_matches(i: IssueStructure, j: IssueStructure) -> set[tuple[Term, Term]]:
    """
    Based on definition 4.8, p144

    M_IJ = {<t_1,t_2> : ∃x(<t_1,x> ∈ I ∧ (<t_2,x> ∈ J ∨ <t_2,x̄> ∈ J)}

    where for x = <P^k, <t_1,...,t_k>>, x̄ = <P̄^k, <t_1,...,t_k>>

    Args:
        i (IssueStructure): The issue structure I
        j (IssueStructure): The issue structure J

    Returns:
        set[tuple[Term, Term]]: The set of term matches.
    """
    pairs: list[tuple[Term, Term]] = []
    for t1, open_atom_self in i:
        # <t_1,x> ∈ I
        for t2, open_atom_other in j:
            if (
                open_atom_self == open_atom_other  # <t_2,x> ∈ J
                or open_atom_self == ~open_atom_other  # <t_2,x̄> ∈ J
            ):
                pairs.append((t1, t2))

    return set(pairs)


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
                    s: w.restriction(
                        set(new_dep_rel.universals | new_dep_rel.existentials)
                    )
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
        """
        Replaces arbitrary objects found in the view with another term from a mapping.

        Args:
            replacements (dict[ArbitraryObject, Term]): Mapping of replacements.

        Returns:
            View: The view with replacements made.
        """
        new_stage_set: set[State] = set()
        new_weights: Weights = Weights()
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
        Checks to see if two views are equivalent when the arbitrary objects
        are changed designation.

        Complexity is O((n!)^2*n) where n is average num of exi and unis

        For exis and unis above 9 or 10 (of each) this becomes an issue, below is fine

        Args:
            other (View): The view for comparison

        Raises:
            ValueError: Too many arbitrary objects for permutation computation.

        Returns:
            bool: True for is equivalent, False for is not.
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

    def product(
        self, view: "View", inherited_dependencies: Optional[DependencyRelation] = None
    ) -> "View":
        """
        Based on definition 5.15, p208

        Γ^θ_fRI ⨂ᵀ Δ^{Ψ}_gSJ = (Γ_f ⨂ Δ^{Ψ}_g)^θ_(T⋈R)⋈(T⋈S),I∪J

        where Γ_f ⨂ Δ^{Ψ}_g = P + Σ_γ∈(Γ＼P) Σ_δ∈Δ {f(γ) x g(δ)).(γ∪δ)}
        and P = {f(γ).γ∈Γ |¬∃ψ ∈ Ψ.ψ⊆γ}

        Args:
            self (View): Γ^θ_fRI
            view (View): Δ^{Ψ}_gSJ
            inherited_dependencies (Optional[DependencyRelation], optional): T. Defaults to an empty
                dependency relation.

        Returns:
            View: The result of the product calculation.
        """
        if inherited_dependencies is None:
            inherited_dependencies = DependencyRelation(set(), set(), frozenset())

        # Γ_f ⨂ Δ^{Ψ}_g
        stage, weights = stage_function_product(
            (self.stage, self.weights), (view.stage, view.supposition, view.weights)
        )

        # (T⋈R)⋈(T⋈S)
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

    def sum(
        self, view: "View", inherited_dependencies: Optional[DependencyRelation] = None
    ):
        """
        Based on definition 5.14, p208

        Γ^θ_fRI ⊕ᵀ Δ^{0}_gSJ = (Γ_f + Δ_g)^θ_(T⋈R)⋈(T⋈S),I∪J

        where (Γ_f + Δ_g) = (Γ ∪ Δ)_h, where h(γ) = f(γ) + g(γ)

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
            inherited_dependencies = DependencyRelation(set(), set(), frozenset())
        if self.supposition != view.supposition:
            # TODO: Added this
            return self
            # raise ValueError(
            #     f"Invalid sum on {self.supposition} and {view.supposition}"
            # )

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
                supposition=self.supposition,
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

        Γ^θ_fRI[Δ^{0}_gSJ]^A = Γ^θ_fRI[Δ^{0}_gSJ]^𝔼A[Δ^{0}_gSJ]^𝓐A

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
        Based on definition 5.16, p210

        [Γ^Θ_fRI]ᶰ = (Θ ⨂ [Γ]ᶰ)^{0}_[R]ᶰ[I]ᶰ

        Args:
            self (View): Γ^Θ_fRI
            verbose (bool, optional): enable verbose mode. Defaults to False.

        Returns:
            View: The negated view.
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
        Based on Definition 5.26, p221

        Γ^Θ_fRI[Δ^Ψ_gSJ]ᴹ = ⊕^R⋈S_γ∈Γ {f(γ).γ}|^Θ_RI ⨂^R⋈S Δ^Ψ_gSJ ⨂^R⋈S (⭙^R⋈S_<t,u>∈M'ij(γ) Sub^R⋈S_<t,u>(Δ^{0}_gSJ))

        Args:
            self (View): Γ^Θ_fRI
            view (View): Δ^Ψ_gSJ
            verbose (bool, optional): enable verbose mode. Defaults to False.

        Returns:
            View: Returns the merged view.
        """

        def _m_prime(
            gamma: State,
        ) -> set[tuple[Term, Universal]]:
            """
            M'ij(γ) = {<t,u> ∈ Mij : u ∈ U_s ∧ ∃ψ ∈ Ψ (ψ[t/u] ⊆ γ ∧ ψ⊈γ)}

            Args:
                gamma (State): γ

            Returns:
                set[tuple[Term, Universal]]: M'ij(γ)
            """
            out: set[tuple[Term, Universal]] = set()
            # <t,u> ∈ Mij
            for t, u in issue_matches(self.issue_structure, view.issue_structure):
                # u ∈ U_s
                if isinstance(
                    u, ArbitraryObject
                ) and not view.dependency_relation.is_existential(u):
                    # ∃ψ ∈ Ψ
                    psi_exists = False
                    for psi in view.supposition:
                        # (ψ[t/u] ⊆ γ ∧ ψ⊈γ)
                        if psi.replace({u: t}).issubset(gamma) and not psi.issubset(
                            gamma
                        ):  # TODO: Changed to be the same as book? Is this correct?
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
                product_factors: list[View] = [
                    View.with_restriction(
                        SetOfStates({gamma}),
                        self.supposition,
                        self.dependency_relation,
                        self.issue_structure,
                        self.weights,
                    ),  # γ∈Γ {f(γ).γ}|^Θ_RI
                    view,  # Δ^Ψ_gSJ
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
                    )  # <t,u>∈M'ij Sub^R⋈S_<t,u>(Δ^{0}_gSJ)
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
        Based on Definition 4.34, p163

        Γ^Θ_fRI[D]^↻ = Γ^Θ_fRI[D]ᵁ[D]ᴱ[D]ᴬ[D]ᴹ

        Args:
            self (View): Γ^Θ_fRI
            view (View): D
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The updated view.
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
        Based on Definition 5.28, p223

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
        Based on Definition 5.28, p223

        Γ^Θ_fRI[D]ᵁ = {0}^Θ_RI ⨂^R⋈S (⨂^R⋈S_<t,u>∈M'ij Sub^R⋈S_<t,u> (Γ^{0}_fRI))

        # TODO: Note swapping of t and u in M'ij, is this significant or typo?
        """

        def _m_prime() -> set[tuple[Universal, FunctionalTerm | ArbitraryObject]]:
            """
            Based on Definition 5.28, p223

            M'ij = {<u,t> : <u,t> ∈ Mij ∧ U_R - A(Θ)}

            Returns:
                set[tuple[Universal, FunctionalTerm | ArbitraryObject]]: Returns the M'ij set.
            """
            output_set = set()
            for u, t in issue_matches(self.issue_structure, view.issue_structure):
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
        # M'ij ≠ Ø}
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
                # {0}^Θ_RI
                View.with_restriction(
                    stage=SetOfStates({State({})}),
                    supposition=self.supposition,
                    dependency_relation=self.dependency_relation,
                    issue_structure=self.issue_structure,
                    weights=None,
                )
            ] + [
                # <t,u>∈M'ij Sub^R⋈S_<t,u> (Γ^{0}_fRI)
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
        Based on Definition 5.34, p233

        Γ^Θ_fRI[Δ^{0}_gSJ]ᴱ = Γ^Θ_fRI ⊕^R⋈S (
            ⊕^R⋈S_<e,t>∈M'ij Sub^R⋈S_<t,e> (BIG_UNION(e)^Θ_SJ)
        )
        """

        def _big_union(e: Existential) -> tuple[Stage, Weights]:
            """
            Based on Definition 5.34, p233

            BIG_UNION(e) = ∪_γ∈Γ,e∈A(γ) {γ}∪{{x∈γ : e∉A(x)} ∪ δ : δ ∈ BIG_PRODUCT(γ) ∧ δ⊈γ}
            Args:
                e (Existential): The existential input

            Returns:
                tuple[Stage, Weights]: The stage and associated weights
            """

            def _big_product(gamma: State) -> SetOfStates:
                """
                Based on Definition 5.34, p233

                BIG_PRODUCT(γ) = ⭙_x∈N(γ,I,e) {{x}, {x̄}}

                Args:
                    gamma (State): The input state

                Returns:
                    SetOfStates: The resulting set of states
                """

                def N(gamma: State, e: Existential) -> State:
                    """
                    N(γ,I,e) = {x[e/?] ∈ γ : <e,x> ∈ I}

                    Args:
                        gamma (State): γ
                        e (Existential): e

                    Returns:
                        State: N(γ,I,e)
                    """
                    # TODO: Think this need updating??? e is overloaded??
                    atoms = set()
                    for t, open_atom in self.issue_structure:
                        formed_atom = open_atom(t)
                        for atom in gamma:
                            if formed_atom == atom:
                                atoms.add(atom)
                    return State(atoms)

                return reduce(
                    lambda s1, s2: s1 * s2,
                    [SetOfStates({State({x}), State({~x})}) for x in N(gamma, e)],
                )

            # BIG_UNION(e) = ∪_γ∈Γ,e∈A(γ) {γ}∪{{x∈γ : e∉A(x)} ∪ δ : δ ∈ BIG_PRODUCT(γ) ∧ δ⊈γ}
            assert e in self.stage_supp_arb_objects
            final_sets: list[SetOfStates] = []

            new_weights: dict[State, Weight] = {}
            # γ∈Γ
            for gamma in self.stage:
                # e∈A(γ)
                if e in gamma.arb_objects:
                    new_weights[gamma] = self.weights[gamma]
                    # {x∈γ : e∉A(x)}
                    x_set = State([x for x in gamma if e not in x.arb_objects])
                    # {γ}∪{{x∈γ : e∉A(x)} ∪ δ : δ ∈ BIG_PRODUCT(γ) ∧ δ⊈γ}
                    proto_sets: SetOfStates = SetOfStates(
                        {
                            x_set | delta
                            for delta in _big_product(gamma)
                            if not delta.issubset(gamma)
                        }
                    )
                    final_sets.append(SetOfStates({gamma}) | proto_sets)

            output_set = reduce(lambda s1, s2: s1 | s2, final_sets)
            output_weights = Weights(new_weights) + Weights.get_null_weights(output_set)
            return SetOfStates(output_weights.keys()), output_weights

        def _m_prime() -> set[tuple[Existential, Term]]:
            """
            Based on Definition 5.34, p233

            M'ij = {<e,t> ∈ Mij : e ∈ E_R - A(Θ ∪ Δ) ∧ ¬∃(<e,x> ∈ D_R)}

            Returns:
                set[tuple[Existential, Term]]: The pairs of terms matching for M'ij
            """
            output_set: set[tuple[Existential, Term]] = set()
            # <e,t> ∈ Mij
            for e, t in issue_matches(self.issue_structure, view.issue_structure):
                # e ∈ E_R - A(Θ ∪ Δ) ∧ ¬∃(<e,x> ∈ D_R)
                if (
                    isinstance(e, ArbitraryObject)
                    and e
                    in (
                        self.dependency_relation.existentials
                        - (self.supposition | view.stage).arb_objects
                    )
                    and not any(
                        d.existential == e
                        for d in self.dependency_relation.dependencies
                    )
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
            # M'ij ≠ ∅
            if len(m_prime) == 0:
                if verbose:
                    print(f"ExiSumOutput: {self}")
                return self
            else:
                arb_gen = ArbitraryObjectGenerator(
                    self.stage_supp_arb_objects | view.stage_supp_arb_objects
                )
                r_fuse_s = self.dependency_relation.fusion(view.dependency_relation)
                to_sum: list["View"] = []
                # <e,t>∈M'ij
                for e, t in m_prime:
                    stage, weights = _big_union(e)
                    to_sum.append(
                        # Sub^R⋈S_<t,e> (BIG_UNION(e)^Θ_SJ)
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
                # ⊕^R⋈S_<e,t>∈M'ij (...)
                sum_result: View = reduce(
                    lambda v1, v2: v1.sum(v2, r_fuse_s),
                    to_sum,
                )
                # Γ^Θ_fRI ⊕^R⋈S (...)
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
        # TODO: Is it needed? Skipping doc string for now
        """
        if division_presupposition(
            self_stage=self.stage,
            other_stage=other.stage,
            other_supposition=other.supposition,
        ):
            new_weights: Weights = Weights()
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
        Based on definition 5.17 p210 (contradiction)
        Based on definition 5.35 p233 (identity)
        Based on definition 5.32 p232 (central case)

        Contradiction: Γ^Θ_fRI[⊥]ꟳ = {γ∈Γ : ¬∃κ ∈ 𝕂.κ ⊆ γ}^Θ_fRI
        Identity: Γ^Θ_fRI[{w.It₁t₂}^{0}_gSJ]ꟳ = {γ ∈ Γ : It₁t₂ ∉ γ}_f + Σ_γ∈Γ s.t.It₁t₂∈γ {(f(γ)[t₁/t₂]).(γ[t₁/t₂])}^Θ_RI # TODO: What is this supposed to say? Is issue I or J? Where is g?
        Central: Γ^Θ_fRI[Δ^Ψ_gSJ]ꟳ = Σ_γ∈Γ {f(γ).γ[Δ^Ψ]ꟳ}

        # TODO: When its ready fill out identity

        Args:
            self (View): Γ^Θ_fRI
            other (View): ⊥ | {w.It₁t₂}^{0}_gSJ | Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.
            absurd_states (Optional[list[State]], optional): Manual input of primitive absurd states. Defaults to None.

        Returns:
            View: The factored view.
        """
        if verbose:
            print(f"FactorInput: External: {self} Internal {other}")

        def big_intersection(state: State) -> Optional[State]:
            """
            ∩{γ⌀_Γ(Δ^Ψ[t/a]) : <t,a> ∈ Mij ∧ a ∈ U_S}

            Args:
                state (State): γ

            Returns:
                Optional[State]: If nothing inside intersection, returns None,
                    else returns the resultant state of the intersection.
            """
            out: list[State] = []
            # <t,a> ∈ Mij
            for t, a in issue_matches(self.issue_structure, other.issue_structure):
                # a ∈ U_S
                if isinstance(
                    a, ArbitraryObject
                ) and not other.dependency_relation.is_existential(a):
                    # γ⌀_Γ(Δ^Ψ[t/a])
                    out.append(
                        state_division(
                            state=state,
                            self_stage=self.stage,
                            other_stage=other.stage.replace({a: t}),  # Δ[t/a]
                            other_supposition=other.supposition.replace(
                                {a: t}
                            ),  # Ψ[t/a]
                        )
                    )
            if len(out) == 0:
                return None
            else:
                return reduce(lambda s1, s2: s1 & s2, out)

        def state_factor(gamma: State) -> State:
            """
            Based on definition 4.39, p168

            γ[Δ^Ψ] = (γ⌀_Γ Δ^Ψ) ∩ (BIG_INTERSECTION)

            Args:
                gamma (State): γ

            Returns:
                State: The factored state.
            """
            # γ⌀_Γ Δ^Ψ
            gamma_prime = state_division(
                state=gamma,
                self_stage=self.stage,
                other_stage=other.stage,
                other_supposition=other.supposition,
            )
            expr = big_intersection(gamma)
            if expr is None:
                return gamma_prime
            else:
                return gamma_prime & expr

        def identity_factor_condition() -> bool:
            """
            It₁t₂ ∉ γ

            TODO: What goes here?
            Returns:
                bool: True if identity factor should be used.
            """
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
                    set(
                        other.dependency_relation.universals
                        | other.dependency_relation.existentials
                    )
                )
                != other.dependency_relation
            ):
                return False
            return True

        if other.is_falsum:
            if verbose:
                print("Contradiction factor")
            # {γ∈Γ : ¬∃κ ∈ 𝕂.κ ⊆ γ}^Θ_fRI
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

            expr2_weights: Weights = Weights()
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
            # Σ_γ∈Γ {f(γ).γ[Δ^Ψ]ꟳ}

            new_weights = Weights()
            for gamma in self.stage:
                new_weights._adding(state_factor(gamma=gamma), self.weights[gamma])
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
        Based on definition 5.23

        Γ^Θ_fRI[]ᴰ = (Γ_f + [Θ]ᶰ)^{0}_R[I]ᶰ

        Args:
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The deposed view.
        """
        if verbose:
            print(f"DeposeInput: {self}")
        verum = SetOfStates({State({})})
        # [Θ]ᶰ
        sup_negation = self.supposition.negation()
        # Γ_f + [Θ]ᶰ
        new_stage = self.stage | sup_negation
        new_weights = self.weights + Weights.get_null_weights(sup_negation)
        out = View.with_restriction(
            stage=new_stage,
            supposition=verum,
            dependency_relation=self.dependency_relation,
            issue_structure=self.issue_structure.negation(),  # [I]ᶰ
            weights=new_weights,
        )
        if verbose:
            print(f"DeposeOutput: {out}")
        return out

    def inquire(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 5.18, p210

        # TODO: Note typo in book in if statement - corrected here γ -> Γ
        If A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅ and A(Δ) ∩ A(Ψ) = ∅
            O Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = (Γ^Θ_fRI ⨂ (Δ^Ψ_gSJ ⊕ˢ({0}^Ψ_SJ ⨂ ([Δ^{0}_gSJ]ᶰ)^nov(A(Δ)))))[⊥]ꟳ

        Else if A(Δ∪Ψ) ⊆ A(Γ∪Θ) and S = [R]_Γ∪Θ
            I Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = (Γ^Θ_fRI ⨂ᴿ (Δ^Ψ_gSJ ⊕ᴿ ([Δ_g]ᶰ|^Ψ_SJ)))[⊥]ꟳ

        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = Γ^Θ_fRI
        Args:
            self (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant inquired view.
        """
        if verbose:
            print(f"InquireInput: External: {self} Internal {other}")
        # A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅
        cond1 = len(self.stage_supp_arb_objects & other.stage_supp_arb_objects) == 0
        # A(Δ) ∩ A(Ψ) = ∅
        cond2 = len(other.stage.arb_objects & other.supposition.arb_objects) == 0
        if cond1 and cond2:
            # O case
            # (Γ^Θ_fRI ⨂ (Δ^Ψ_gSJ ⊕ˢ({0}^Ψ_SJ ⨂ ([Δ^{0}_gSJ]ᶰ)^nov(A(Δ)))))[⊥]ꟳ

            if verbose:
                print("Inquire, O case")
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | other.stage_supp_arb_objects
            )
            # {0}^Ψ_SJ
            v1 = View.with_restriction(
                stage=SetOfStates({State({})}),
                supposition=other.supposition,
                dependency_relation=other.dependency_relation,
                issue_structure=other.issue_structure,
                weights=None,
            )
            # [Δ^{0}_gSJ]ᶰ TODO: Book suggests view negation, also where are the weights?
            v2 = View.with_restriction(
                stage=other.stage.negation(),
                supposition=SetOfStates({State({})}),
                dependency_relation=other.dependency_relation.negation(),
                issue_structure=other.issue_structure.negation(),
                weights=None,
            )
            # (V2)^nov(A(Δ))
            v3 = arb_gen.novelise_all(v2)

            # (Γ^Θ_fRI ⨂ (Δ^Ψ_gSJ ⊕ˢ(V1 ⨂ V3)))[⊥]ꟳ
            out = self.product(
                other.sum(v1.product(v3), other.dependency_relation)
            ).factor(View.get_falsum())
        elif other.stage_supp_arb_objects.issubset(  # A(Δ∪Ψ) ⊆ A(Γ∪Θ)
            self.stage_supp_arb_objects
        ) and other.dependency_relation == self.dependency_relation.restriction(
            self.stage_supp_arb_objects  # S = [R]_Γ∪Θ
        ):
            # I case
            # (Γ^Θ_fRI ⨂ᴿ (Δ^Ψ_gSJ ⊕ᴿ ([Δ_g]ᶰ|^Ψ_SJ)))[⊥]ꟳ

            if verbose:
                print("Inquire, I case")

            # [Δ_g]ᶰ|^Ψ_SJ
            # TODO: Does not match?
            view2 = View.with_restriction(
                stage=other.stage.negation(),
                supposition=other.supposition,
                dependency_relation=other.dependency_relation,
                issue_structure=other.issue_structure.negation(),
                weights=None,
            )
            # (Γ^Θ_fRI ⨂ᴿ (Δ^Ψ_gSJ ⊕ᴿ VIEW2))[⊥]ꟳ
            out = self.product(
                other.sum(view2, self.dependency_relation), self.dependency_relation
            ).factor(View.get_falsum())
        else:
            if verbose:
                print("Inquire, pass-through case")
            out = self

        if verbose:
            print(f"InquireOutput: {out}")
        return out

    def suppose(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 5.22, p219

        If A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅ ∧ Δ^Ψ_gSJ = Δ^Ψ_SJ
            O Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ˢ = Γ^Θ'_[R⋈R'][I∪I'] [Δ^Ψ_gSJ]ᵁ[Δ^Ψ_gSJ]ᴱ[Δ^Ψ_gSJ]ᴬ[Δ^Ψ_gSJ]ᴹ

            where: Θ'^{0}_f'R'I' = Θ^{0}_fRI ⨂ Nov(Δ^Ψ_g[S]ᶰJ []ᴰ)

        Else if A(Δ) ⊆ A(Γ∪Θ), [R]_Δ = S, and Δ^Ψ_gSJ = Δ^Ψ_SJ and Ψ = {0}
            I Case: Γ^Θ_fRI[Δ^{0}_gSJ]ˢ = Γ^(Θ⨂Δ)_fRI[Δ^{0}_gSJ]ᵁ[Δ^{0}_gSJ]ᴱ[Δ^{0}_gSJ]ᴬ[Δ^{0}_gSJ]ᴹ

        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = Γ^Θ_fRI

        Args:
            self: (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant view.
        """
        if verbose:
            print(f"SupposeInput: External: {self} Internal {other}")
        # TODO: What about Δ^Ψ_gSJ = Δ^Ψ_SJ?
        # A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅ ∧ Δ^Ψ_gSJ = Δ^Ψ_SJ
        if len(self.stage_supp_arb_objects & other.stage_supp_arb_objects) == 0:
            # O case
            arb_gen = ArbitraryObjectGenerator(
                self.stage_supp_arb_objects | other.stage_supp_arb_objects
            )
            # Θ'^{0}_f'R'I' = Θ^{0}_fRI ⨂ Nov(Δ^Ψ_g[S]ᶰJ []ᴰ)
            # TODO: note difference in book, here uses f - are we supposed to generate some weights?
            v_prime = View(
                stage=self.supposition,
                supposition=SetOfStates({State()}),
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
            # Γ^Θ'_[R⋈R'][I∪I'] [Δ^Ψ_gSJ]ᵁ[Δ^Ψ_gSJ]ᴱ[Δ^Ψ_gSJ]ᴬ[Δ^Ψ_gSJ]ᴹ
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
        # A(Δ) ⊆ A(Γ∪Θ), [R]_Δ = S, and Δ^Ψ_gSJ = Δ^Ψ_SJ and Ψ = {0}
        # TODO: What about Δ^Ψ_gSJ = Δ^Ψ_SJ?
        elif (
            (other.stage.arb_objects.issubset(self.stage_supp_arb_objects))
            and (
                self.dependency_relation.restriction(other.stage.arb_objects)
                == other.dependency_relation
            )
            and other.supposition.is_verum
        ):
            # I case
            # Γ^(Θ⨂Δ)_fRI[Δ^{0}_gSJ]ᵁ[Δ^{0}_gSJ]ᴱ[Δ^{0}_gSJ]ᴬ[Δ^{0}_gSJ]ᴹ
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

    def _query_m_prime(self, other: "View") -> set[tuple[Term, ArbitraryObject]]:
        """
        Based on definition 5.19, p210

        M'ij = {<t,e> ∈ Mij : e ∈ E_S＼E_R}
        """
        return {
            (t, e)
            for t, e in issue_matches(self.issue_structure, other.issue_structure)
            if isinstance(e, ArbitraryObject)
            and e
            in (
                other.dependency_relation.existentials
                - self.dependency_relation.existentials
            )
        }

    def query(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 5.19, p210
        If U_S ⊆ U_R:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ꟴ = H + Σ_γ∈Γ Σ_δ∈Δ_s.t.Φ(γ, δ) {w_(γ,δ).δ}^Θ_R⋈<U_R,E_S＼E_R,D_S'>,I∪J
        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ꟴ = Γ^Θ_fRI
        """

        def _Ds_prime(
            m_prime: set[tuple[Term, ArbitraryObject]]
        ) -> frozenset[Dependency]:
            """
            Based on definition 4.41, p172

            D_S' = D₁ ∪ D₂ ∪ D₃ ∪ D₄ ∪ D₅ ∪ D₆

            D₁ = [D_S]_A/E_R
            D₂ = {<eₘ,u> : ∃m∃m' ∈ M'ij(eₘ = eₘ'  ∧ tₘ ≠ tₘ') ∧ u ∈ U_R}
            D₃ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ u ∈ U_R(tₘ)}
            D₄ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ e ∈ E_R(tₘ) ∧ <e,u> ∈ R}
            D₅ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ u ∈ U_R ∧ ∀u'_∈U_R(D₃∪D₄) (u' ◁_R u)}
            D₆ = {<e,u> : e,e' ∈ E_S – E_R ∧ e ≲_S e' ∧ (∀m,m' ∈ M'ij(eₘ = e' ∧ eₘ' = e') -> tₘ = tₘ') ∧ <e',u> ∈ D₁ ∪ D₂ ∪ D₃ ∪ D₄ ∪ D₅}

            Args:
                m_prime (set[tuple[Term, ArbitraryObject]]): M'ij

            Returns:
                frozenset[Dependency]: D_S'
            """
            # D₁ = [D_S]_A/E_R
            D1 = other.dependency_relation.restriction(
                other.stage_supp_arb_objects - self.dependency_relation.existentials
            ).dependencies

            # D₂ = {<eₘ,u> : ∃m∃m' ∈ M'ij(eₘ = eₘ'  ∧ tₘ ≠ tₘ') ∧ u ∈ U_R}
            #
            #    ∃m∃m' ∈ M'ij(eₘ = eₘ'  ∧ tₘ ≠ tₘ')
            exis_for_pairs = {
                e
                for t, e in m_prime
                for t_prime, e_prime in m_prime
                if e == e_prime and t != t_prime
            }
            D2 = {
                Dependency(existential=exi, universal=u)
                for u in self.dependency_relation.universals
                for exi in exis_for_pairs
            }

            # D₃ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ u ∈ U_R(tₘ)}
            D3 = {
                Dependency(existential=e_m, universal=u)
                for t_m, e_m in m_prime
                for u in t_m.arb_objects
                if u in self.dependency_relation.universals
            }

            # D₄ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ e ∈ E_R(tₘ) ∧ <e,u> ∈ R}
            D4: set[Dependency] = set()
            # <tₘ,eₘ> ∈ M'ij
            for t_m, e_m in m_prime:
                # e ∈ E_R(tₘ)
                for e in t_m.arb_objects:
                    if self.dependency_relation.is_existential(e):
                        # <e,u> ∈ R
                        for dep in self.dependency_relation.dependencies:
                            if e == dep.existential:
                                D4.add(
                                    Dependency(existential=e_m, universal=dep.universal)
                                )

            # D₅ = {<eₘ,u> : <tₘ,eₘ> ∈ M'ij ∧ u ∈ U_R ∧ ∀u'_∈U_R(D₃∪D₄) (u' ◁_R u)}
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
            # DSF = D₁ ∪ D₂ ∪ D₃ ∪ D₄ ∪ D₅
            dep_so_far = D1 | D2 | D3 | D4 | D5
            # DES = E_S – E_R
            D6_exi_set = (
                other.dependency_relation.existentials
                - self.dependency_relation.existentials
            )
            # D₆ = {<e,u> : e,e' ∈ DES ∧ e ≲_S e' ∧ (∀m,m' ∈ M'ij(eₘ = e' ∧ eₘ' = e') -> tₘ = tₘ') ∧ <e',u> ∈ DSF}
            D6: set[Dependency] = set()
            # e,e' ∈ DES
            for e in D6_exi_set:
                for e_prime in D6_exi_set:
                    # e ≲_S e'
                    # TODO: Is the second condition?: (∀m,m' ∈ M'ij(eₘ = e' ∧ eₘ' = e') -> tₘ = tₘ')
                    if other.dependency_relation.less_sim(e, e_prime) and (
                        len([e_m for _, e_m in m_prime if e_m == e_prime]) < 2
                    ):
                        # <e',u> ∈ DSF
                        for dep in dep_so_far:
                            if dep.existential == e_prime:
                                D6.add(
                                    Dependency(existential=e, universal=dep.universal)
                                )

            return dep_so_far | D6

        if verbose:
            print(f"QueryInput: External: {self} Internal {other}")
        # U_S ⊆ U_R
        if other.dependency_relation.universals.issubset(
            self.dependency_relation.universals
        ):
            # H + Σ_γ∈Γ Σ_δ∈Δ_s.t.Φ(γ, δ) {w_(γ,δ).δ}^Θ_R⋈<U_R,E_S＼E_R,D_S'>,I∪J
            m_prime = self._query_m_prime(other)
            D_s_prime = _Ds_prime(m_prime)

            H = _H(self, other, m_prime)

            s2_weights: Weights = Weights()
            # δ∈Δ
            for delta in other.stage:
                # γ∈Γ
                for gamma in self.stage:
                    # Φ(γ, δ)
                    if phi(
                        gamma,
                        delta,
                        m_prime,
                        other.supposition,
                        self.weights[gamma],
                        other.weights[delta],
                    ):
                        # {w_(γ,δ).δ}
                        other_weight = other.weights[delta]
                        # g(δ) = <<>>
                        if other_weight.is_null:
                            # f(γ)
                            s2_weights._adding(delta, self.weights[gamma])
                        # g(δ) ≠ <<>>
                        else:
                            # g(δ)
                            s2_weights._adding(delta, other_weight)

            s2 = SetOfStates(s2_weights.keys())
            new_stage = H | s2
            new_weights = Weights.get_null_weights(H) + s2_weights
            # R⋈<U_R,E_S＼E_R,D_S'>
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
                issue_structure=self.issue_structure | other.issue_structure,  # I∪J
                weights=new_weights,
            )
        else:
            out = self
        if verbose:
            print(f"QueryOutput: {out}")
        return out

    def which(self, other: "View", *, verbose: bool = False) -> "View":
        """
        Based on definition 5.53, p232

        Γ^Θ_fRI[Δ^Ψ_gSJ]ᵂ = H + Σ_γ∈Γ《ω.ξ : Ξ(γ,ω.ξ)》|^Θ_RI

        Ξ(γ,ω.ξ) = ∃ψ_∈Ψ ∃δ_∈Δ ∃n≥0 ∃<t₁,e₁>,...,<tₙ,eₙ>∈M'ij (∀i,j.(e_i=e_j -> i=j)) ∧ (ξ∪ψ ⊆ γ ∧ ω.ξ = (g(δ).δ)[t₁/e₁,...,tₙ/eₙ])

        Args:
            self (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant view.
        """

        if verbose:
            print(f"WhichInput: External: {self} Internal {other}")

        if other.dependency_relation.universals.issubset(
            self.dependency_relation.universals
        ):
            m_prime = self._query_m_prime(other)

            def xi_fka_psi(gamma: State) -> Weights:
                weights: Weights = Weights()
                for m_prime_set in powerset(m_prime):
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

            # H
            H = _H(self, other, m_prime)

            s2_weights: Weights = Weights()
            # Σ_γ∈Γ
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
