from typing import Iterable, Optional

from pyetr.atoms.terms.function import RealNumber
from pyetr.atoms.terms.multiset import Multiset
from pyetr.atoms.terms.term import FunctionalTerm
from pyetr.dependency import DependencyRelation
from pyetr.issues import IssueStructure
from pyetr.stateset import SetOfStates, State
from pyetr.weight import Weight, Weights

from .view import View

# def basic_step(*, v: tuple[View, ...], verbose: bool = False) -> View:
#     out = View.get_verum()

#     for view in v:
#         new_out = out.update(view, verbose=verbose)
#         if new_out == out:
#             new_out = out.update(view.depose(verbose=verbose), verbose=verbose)
#         out = new_out
#     return out.factor(View.get_falsum(), verbose=verbose)


def basic_step(v: tuple[View, ...], verbose: bool = False) -> View:
    out = View.get_verum()
    for i, view in enumerate(v):
        if i == 0:
            out = out.update(view.depose(verbose=verbose), verbose=verbose)
        else:
            out = out.update(view, verbose=verbose)
    return out.factor(View.get_falsum(), verbose=verbose)


def default_inference_procedure(v: tuple[View, ...], verbose: bool = False) -> View:
    g_prime = basic_step(v=v, verbose=verbose)
    for i, view in enumerate(v):
        if i == 0:
            g_prime = g_prime.factor(view.depose(verbose=verbose), verbose=verbose)
        else:
            g_prime = g_prime.factor(view, verbose=verbose)
    return g_prime


def default_procedure_what_is_prob(
    v: tuple[View, ...], prob_of: View, verbose: bool = False
):
    """
    Based on definition 5.20
    """
    g_prime = basic_step(v=v, verbose=verbose)
    if verbose:
        print(f"G prime: {g_prime}")
    g_prime_prime = g_prime.query(prob_of, verbose=verbose)
    out = g_prime_prime.stage.equilibrium_answer_potential(
        prob_of.stage,
        g_prime_prime.weights,  # TODO: Adjusted weight extraction point based on test and previous use
    )
    if isinstance(out.f, RealNumber) and out.f.num >= 0 and out.f.num <= 100:
        if verbose:
            print(f"Case 1, value: {out.f.num}")
        return g_prime_prime
    else:
        if verbose:
            print("Case 2")
        total: float = 0
        gammas_with_empty: list[State] = []
        for s, w in g_prime.weights.items():
            if w.is_null:
                gammas_with_empty.append(s)
            for t in w.multiplicative:
                if isinstance(t, FunctionalTerm) and isinstance(t.f, RealNumber):
                    total += t.f.num

        x = (100 - total) / len(gammas_with_empty)
        term_x = FunctionalTerm(RealNumber(x), t=[])

        res = g_prime
        for gamma in gammas_with_empty:
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
        g_prime_prime = res.query(prob_of, verbose=verbose)
        out = g_prime_prime.stage.equilibrium_answer_potential(
            prob_of.stage,
            g_prime_prime.weights,  # TODO: Adjusted weight extraction point based on test and previous use
        )
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
):
    result = dq
    for v in cv:
        result = result.update(v, verbose=verbose)
    result = result.factor(
        View.get_falsum(), verbose=verbose, absurd_states=absurd_states
    )
    for v in pr:
        result = result.update(v, verbose=verbose)
    return dq.answer(result, verbose=verbose)
