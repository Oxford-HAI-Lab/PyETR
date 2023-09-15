__all__ = ["FunctionalTerm", "Function", "ArbitraryObject"]

from abc import abstractmethod

from pyetr.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractMultiset,
    AbstractTerm,
)

from .function import Function, RealNumber, Summation, XBar


class Term(AbstractTerm):
    @property
    @abstractmethod
    def arb_objects(self) -> set["ArbitraryObject"]:
        ...

    @abstractmethod
    def replace(
        self,
        replacements: dict["ArbitraryObject", "Term"],
    ) -> "Term":
        ...


class ArbitraryObject(AbstractArbitraryObject, Term):
    @property
    def arb_objects(self) -> set["ArbitraryObject"]:
        return {self}

    def replace(
        self,
        replacements: dict["ArbitraryObject", Term],
    ) -> Term:
        if self in replacements:
            return replacements[self]
        return self


class FunctionalTerm(AbstractFunctionalTerm[Term], Term):
    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        for term in self.t:
            if isinstance(term, FunctionalTerm) or isinstance(term, Multiset):
                output_set |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_set.add(term)
            else:
                assert False
        return output_set

    def replace(
        self,
        replacements: dict[ArbitraryObject, Term],
    ) -> "FunctionalTerm":
        new_terms = []
        for term in self.t:
            if term in replacements:
                replacement = replacements[term]
            else:
                if isinstance(term, FunctionalTerm):
                    replacement = term.replace(replacements)
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                elif isinstance(term, Multiset):
                    replacement = term.replace(replacements)
                else:
                    assert False
            new_terms.append(replacement)
        return FunctionalTerm(f=self.f, t=tuple(new_terms))


class Multiset(AbstractMultiset[Term], Term):
    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objs = set()
        for term in self:
            arb_objs |= term.arb_objects
        return arb_objs

    def replace(self, replacements: dict["ArbitraryObject", "Term"]) -> "Multiset":
        return Multiset(term.replace(replacements) for term in self)

    def __add__(self, other: "Multiset") -> "Multiset":
        return Multiset(self._items + other._items)


# Changed if clause in 4.2 to separate Arbitrary Objects from FunctionalTerm


def _process_func(term: Term) -> Term:
    if isinstance(term, FunctionalTerm) and term.f == Summation:
        return summation_func(term)
    elif isinstance(term, FunctionalTerm) and term.f == XBar:
        return multiplication_func(term)
    else:
        return term


def summation_func(term: FunctionalTerm) -> FunctionalTerm:
    # If all num are real, return Summation
    # Else return real
    if term.f != Summation:
        raise ValueError(f"Summation func must receive a summation")
    subterms = term.t
    assert len(subterms) == 1
    multiset = subterms[0]
    assert isinstance(multiset, Multiset)
    terms_to_sum: list[Term] = [_process_func(t) for t in multiset]
    new_total: float = 0
    for sum_term in terms_to_sum:
        if isinstance(sum_term, FunctionalTerm) and isinstance(term.f, RealNumber):
            new_total += term.f.num
        else:
            return FunctionalTerm(Summation, (Multiset(terms_to_sum),))
    return FunctionalTerm(RealNumber(new_total), ())


def multiplication_func(term: FunctionalTerm) -> FunctionalTerm:
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
        isinstance(processed_term1, FunctionalTerm)
        and isinstance(processed_term1.f, RealNumber)
        and isinstance(processed_term2, FunctionalTerm)
        and isinstance(processed_term2.f, RealNumber)
    ):
        return FunctionalTerm(
            RealNumber(processed_term1.f.num * processed_term2.f.num), ()
        )
    else:
        return FunctionalTerm(XBar, (processed_term1, processed_term2))
