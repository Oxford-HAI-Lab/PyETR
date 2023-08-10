from .stateset import SetOfStates, State
from .view import View


def basic_step(v: tuple[View, ...], verbose: bool = False) -> View:
    verum = SetOfStates({State({})})
    falsum = SetOfStates({})
    empty_dep = frozenset({})
    out = View.from_deps(verum, verum, empty_dep)
    for i, view in enumerate(v):
        if i == 0:
            out = out.update(view.depose(verbose=verbose), verbose=verbose)
        else:
            out = out.update(view, verbose=verbose)
    return out.factor(View.from_deps(falsum, verum, empty_dep), verbose=verbose)


def default_inference_procedure(v: tuple[View, ...], verbose: bool = False) -> View:
    g_prime = basic_step(v, verbose=verbose)
    for i, view in enumerate(v):
        if i == 0:
            g_prime = g_prime.factor(view.depose(verbose=verbose), verbose=verbose)
        else:
            g_prime = g_prime.factor(view, verbose=verbose)
    return g_prime
