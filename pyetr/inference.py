from typing import Iterable, Optional

from pyetr.atoms.terms.function import RealNumber
from pyetr.stateset import State

from .view import View


def basic_step(*, v: tuple[View, ...], verbose: bool = False) -> View:
    out = View.get_verum()

    for view in v:
        new_out = out.update(view, verbose=verbose)
        if new_out == out:
            new_out = out.update(view.depose(verbose=verbose), verbose=verbose)
        out = new_out
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
    g_prime_prime = g_prime.query(prob_of, verbose=verbose)
    out = g_prime_prime.stage.equilibrium_answer_potential(
        prob_of.stage, prob_of.weights
    )
    if isinstance(out.f, RealNumber) and out.f.num >= 0 and out.f.num <= 100:
        return g_prime_prime
    else:
        raise NotImplementedError
        # x = (100 - sum([s for s in ])


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
