from .abstract_term import AbstractFunctionalTerm, AbstractMultiset, AbstractTerm
from .function import Function, RealNumber


def _process_func(term: AbstractTerm) -> AbstractTerm:
    if isinstance(term, AbstractFunctionalTerm) and term.f == Summation:
        return summation_func(term)
    elif isinstance(term, AbstractFunctionalTerm) and term.f == XBar:
        return multiplication_func(term)
    else:
        return term


def summation_func(term: AbstractFunctionalTerm) -> AbstractFunctionalTerm:
    # If all num are real, return Summation
    # Else return real

    if term.f != Summation:
        raise ValueError(f"Summation func must receive a summation")
    subterms = term.t
    assert len(subterms) == 1
    multiset = subterms[0]
    assert isinstance(multiset, AbstractMultiset)
    terms_to_sum: list[AbstractTerm] = [_process_func(t) for t in multiset]
    new_total: float = 0
    for sum_term in terms_to_sum:
        if isinstance(sum_term, AbstractFunctionalTerm) and isinstance(
            sum_term.f, RealNumber
        ):
            new_total += sum_term.f.num
        else:
            if terms_to_sum == list(multiset):
                return term
            else:
                return AbstractFunctionalTerm(
                    Summation, (AbstractMultiset(terms_to_sum),)
                )
    return AbstractFunctionalTerm(RealNumber(new_total), ())


def multiplication_func(term: AbstractFunctionalTerm) -> AbstractFunctionalTerm:
    # If all num are real, return XBar
    # Else return real
    if term.f != XBar:
        raise ValueError(f"multiplication func must receive an XBar")
    subterms = term.t
    assert len(subterms) == 2
    term1, term2 = subterms
    processed_term1 = _process_func(term1)
    processed_term2 = _process_func(term2)
    if (
        isinstance(processed_term1, AbstractFunctionalTerm)
        and isinstance(processed_term1.f, RealNumber)
        and isinstance(processed_term2, AbstractFunctionalTerm)
        and isinstance(processed_term2.f, RealNumber)
    ):
        return AbstractFunctionalTerm(
            RealNumber(processed_term1.f.num * processed_term2.f.num), ()
        )
    else:
        if processed_term1 == term1 and processed_term2 == term2:
            return term
        else:
            return AbstractFunctionalTerm(XBar, (processed_term1, processed_term2))


XBar = Function("XBar", 2, func_caller=multiplication_func)
Summation = Function("Summation", 1, func_caller=summation_func)
