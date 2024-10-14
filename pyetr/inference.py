__all__ = [
    "basic_step",
    "default_inference_procedure",
    "default_procedure_what_is_prob",
    "default_decision",
    "default_procedure_does_it_follow",
]
from typing import Iterable, Optional, Sequence

from pyetr.atoms.terms.function import RealNumber
from pyetr.atoms.terms.multiset import Multiset
from pyetr.atoms.terms.term import FunctionalTerm
from pyetr.issues import IssueStructure
from pyetr.stateset import SetOfStates, State
from pyetr.weight import Weight, Weights

from .view import View


def basic_step(v: Sequence[View], verbose: bool = False) -> View:
    """
    Based Definition 4.47 p179-180

    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G'
    """
    out = View.get_verum()
    for i, view in enumerate(v):
        if i == 0:
            out = out.update(view.depose(verbose=verbose), verbose=verbose)
        else:
            out = out.update(view, verbose=verbose)
    return out.factor(View.get_falsum(), verbose=verbose)


def default_inference_procedure(v: Sequence[View], verbose: bool = False) -> View:
    """
    Based Definition 4.47 p179-180

    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[P₁[]ᴰ]ꟳ...[Pₙ]ꟳ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G''
    """

    def _default_inference_step1(rel_v: Sequence[View]):
        g_prime = basic_step(v=rel_v, verbose=verbose)
        # Step (1)
        for i, view in enumerate(rel_v):
            if i == 0:
                # G'[P₁[]ᴰ]ꟳ
                g_prime = g_prime.factor(view.depose(verbose=verbose), verbose=verbose)
            else:
                # G'[Pₙ]ꟳ
                g_prime = g_prime.factor(view, verbose=verbose)
        return g_prime

    g_prime = _default_inference_step1(v)
    if g_prime.is_verum or g_prime.is_falsum:
        # Step (2)
        reversed_v = tuple(reversed(v))
        g_prime = _default_inference_step1(reversed_v)
        if g_prime.is_verum or g_prime.is_falsum:
            # Step (3)
            return View.get_verum()
    # Step (4)
    return g_prime


def default_procedure_does_it_follow(
    v: Sequence[View], target: View, verbose: bool = False
) -> bool:
    """
    Based Definition 4.47 p180

    (Sub-procedure for "does Δ^Ψ_RI follow?" tasks)
    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[Ψ^{0}_[R][I]]ˢ[Δ^Ψ_RI]ꟴ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        target View: Δ^Ψ_RI
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        bool: Report yes or no, note: Report G'' -> yes
    """

    def _default_does_it_follow_step1(rel_v: Sequence[View]):
        g_prime = basic_step(rel_v)
        return g_prime.suppose(
            View.with_restriction(
                stage=target.supposition,
                supposition=SetOfStates({State({})}),
                dependency_relation=target.dependency_relation,
                issue_structure=target.issue_structure,
                weights=None,
            ),
            verbose=verbose,
        ).query(target, verbose=verbose)

    # Step (1)
    g_prime_prime = _default_does_it_follow_step1(v)
    if g_prime_prime == target:
        return True
    else:
        # Step (2)
        reversed_v = tuple(reversed(v))
        g_prime_prime = _default_does_it_follow_step1(reversed_v)
        # Step (3)
        return g_prime_prime == target


def default_procedure_what_is_prob(
    v: Sequence[View], prob_of: View, verbose: bool = False
) -> View:
    """
    Based on definition 5.20, p212

    G' = T[P₁]^↻[]ᴰ[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[Δ^Ψ]ꟴ

    If G''[Δ]^𝔼P ∈ [0,100]:
        return G''
    Else
        x = (100 - (Σ_γ∈ΓΣ《α ∈ f(γ) : α ∈ ℝ》)) / #{γ∈Γ : f(γ) =《》}

        where γ₁...γₙ is {γ ∈ Γ : f(γ) =《》}
        G'' = G'[{《x》.0 }^{γ₁}]ᴵ...[{《x》.0 }^{γₙ}]ᴵ[Δ^Ψ]ꟴ

        If G''[Δ]^𝔼P ∈ [0,100]:
            return G''
        Else:
            return ⊥
    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        prob_of (View): Δ^Ψ
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G''
    """
    # G' = T[P₁]^↻[]ᴰ[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    g_prime = basic_step(v=v, verbose=verbose)
    if verbose:
        print(f"G prime: {g_prime}")

    # If G''[Δ]^𝔼P ∈ [0,100]: (condition changed from book)
    if not any(w.is_null for w in g_prime.weights.values()):
        if verbose:
            print(f"Case 1")
        # G'' = G'[Δ^Ψ]ꟴ
        return g_prime.query(prob_of, verbose=verbose)
    else:
        if verbose:
            print("Case 2")

        # (Σ_γ∈ΓΣ《α ∈ f(γ) : α ∈ ℝ》
        total: float = 0
        gammas_with_empty: list[State] = []
        for s, w in g_prime.weights.items():
            if w.is_null:
                gammas_with_empty.append(s)
            for t in w.multiplicative:
                if isinstance(t, FunctionalTerm) and isinstance(t.f, RealNumber):
                    total += t.f.num

        # x = (100 - (Σ_γ∈ΓΣ《α ∈ f(γ) : α ∈ ℝ》)) / #{γ∈Γ : f(γ) =《》}
        x = (100 - total) / len(gammas_with_empty)
        term_x = FunctionalTerm(RealNumber(x), t=[])

        res = g_prime
        # G'' = G'[{《x》.0 }^{γ₁}]ᴵ...[{《x》.0 }^{γₙ}]ᴵ[Δ^Ψ]ꟴ
        for gamma in gammas_with_empty:
            # ...[{《x》.0 }^{γₙ}]ᴵ
            res = res.inquire(
                View.with_restriction(
                    stage=SetOfStates([State([])]),
                    supposition=SetOfStates([gamma]),
                    dependency_relation=g_prime.dependency_relation,
                    issue_structure=IssueStructure([]),
                    weights=Weights(
                        {
                            State([]): Weight(
                                additive=Multiset([]), multiplicative=Multiset([term_x])
                            )
                        }
                    ),
                ),
                verbose=verbose,
            )
        # ...[Δ^Ψ]ꟴ
        g_prime_prime = res.query(prob_of, verbose=verbose)
        # G''[Δ]^𝔼P
        out = g_prime_prime.stage.equilibrium_answer_potential(
            prob_of.stage,
            g_prime_prime.weights,
        )
        if verbose:
            print(f"EquilibriumAnswerOut: {out}")
        # ... ∈ [0,100]
        if isinstance(out.f, RealNumber) and out.f.num >= 0 and out.f.num <= 100:
            return g_prime_prime
        else:
            return View.get_falsum()


def default_decision(
    dq: View,
    cv: Iterable[View],
    pr: Iterable[View],
    verbose: bool = False,
    absurd_states: Optional[list[State]] = None,
) -> View:
    """
    Based on Definition 6.7, p272

    dq[dq[CV]^↻[⊥]ꟳ[PR]^↻]

    Args:
        dq (View): dq, Decision Question
        cv (Iterable[View]): CV, Consequence Views
        pr (Iterable[View]): PR, Priority Views
        verbose (bool, optional): Enable verbose mode. Defaults to False.
        absurd_states (Optional[list[State]], optional): Any additional absurd states in the system. Defaults to None.

    Returns:
        View: The resultant view.
    """
    result = dq
    # dq[CV]^↻
    for v in cv:
        result = result.update(v, verbose=verbose)
    # ...[⊥]ꟳ
    result = result.factor(
        View.get_falsum(), verbose=verbose, absurd_states=absurd_states
    )
    # ...[PR]^↻
    for v in pr:
        result = result.update(v, verbose=verbose)
    return dq.answer(result, verbose=verbose)
