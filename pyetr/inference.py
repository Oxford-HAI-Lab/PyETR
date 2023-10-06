from typing import Iterable

from .view import View


def basic_step(*, v: tuple[View, ...], verbose: bool = False) -> View:
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


def default_decision(
    dq: View, cv: Iterable[View], pr: Iterable[View], verbose: bool = False
):
    result = dq
    for v in cv:
        result = result.update(v, verbose=verbose)
    result.factor(View.get_falsum(), verbose=verbose)
    for v in pr:
        result = result.update(v, verbose=verbose)
    return dq.answer(result, verbose=verbose)
