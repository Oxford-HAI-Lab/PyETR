from .view import View


def basic_step(v: tuple[View, ...], verbose: bool = False) -> View:
    out = View.get_verum()
    for i, view in enumerate(v):
        if i == 0:
            out = out.update(view.depose(verbose=verbose), verbose=verbose)
        else:
            out = out.update(view, verbose=verbose)
    return out.factor(View.get_falsum(), verbose=verbose)


def default_inference_procedure(v: tuple[View, ...], verbose: bool = False) -> View:
    g_prime = basic_step(v, verbose=verbose)
    for i, view in enumerate(v):
        if i == 0:
            g_prime = g_prime.factor(view.depose(verbose=verbose), verbose=verbose)
        else:
            g_prime = g_prime.factor(view, verbose=verbose)
    return g_prime
