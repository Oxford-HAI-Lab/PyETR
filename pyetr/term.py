__all__ = ["FunctionalTerm", "Function", "ArbitraryObject"]

from abc import abstractmethod

from pyetr.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractMultiset,
    AbstractTerm,
)

from .function import Function, RealNumber


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


def all_real(terms: Multiset) -> bool:
    for term in terms:
        if not isinstance(term, RealNumber):
            return False
    return True


def summation_func(terms: Multiset) -> FunctionalTerm:
    # If all num are real, return Summation
    # Else return real
    # if all_real(terms):

    raise NotImplementedError
    # if True:
    #     return FunctionalTerm(
    #         f=Summation,
    #         t=
    #     )
    # else:
    #     return FunctionalTerm(
    #         f=RealNumber,
    #         t=
    #     )


def multiplication_func(t1: Term, t2: Term) -> FunctionalTerm:
    # If all num are real, return XBar
    # Else return real
    raise NotImplementedError
    # if True:
    #     return FunctionalTerm(
    #         f=XBar,
    #         t=
    #     )
    # else:
    #     return FunctionalTerm(
    #         f=RealNumber,
    #         t=
    #     )
