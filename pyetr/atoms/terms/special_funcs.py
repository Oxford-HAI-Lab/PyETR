from pyetr.atoms.terms.term import FunctionalTerm, Term

from .function import Function
from .multiset import Multiset


def multi_func_new(i: float, j: float):
    return i * j


def sum_func_new(*x: float):
    return sum(x)


XBar = Function("XBar", 2, func_caller=multi_func_new)
Summation = Function("Summation", None, func_caller=sum_func_new)


def multiset_product(m1: Multiset[Term], m2: Multiset[Term]) -> Multiset[Term]:
    """
    Based on Definition 5.15, p208-209

    Args:
        m1 (Multiset[Term]): The first multiset in the product
        m2 (Multiset[Term]): The second multiset in the product

    Returns:
        Multiset[Term]: The product of the two multisets.
    """
    if len(m1) == 0:
        return m2
    elif len(m2) == 0:
        return m1
    else:
        return Multiset(
            [FunctionalTerm(f=XBar, t=(s_i, t_j)) for s_i in m1 for t_j in m2]
        )
