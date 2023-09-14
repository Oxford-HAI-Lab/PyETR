__all__ = ["FunctionalTerm", "Function", "ArbitraryObject"]

from abc import abstractmethod

from pyetr.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractSummation,
    AbstractTerm,
)

from .function import Function


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
            if isinstance(term, FunctionalTerm) or isinstance(term, Summation):
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
                elif isinstance(term, Summation):
                    replacement = term.replace(replacements)
                else:
                    assert False
            new_terms.append(replacement)
        return FunctionalTerm(f=self.f, t=tuple(new_terms))


# Changed if clause in 4.2 to separate Arbitrary Objects from FunctionalTerm


class Summation(AbstractSummation[Term], Term):
    @property
    def arb_objects(self) -> set["ArbitraryObject"]:
        a_objs = set()
        for term in self.t:
            a_objs |= term.arb_objects
        return a_objs

    def replace(
        self,
        replacements: dict["ArbitraryObject", "Term"],
    ) -> "Summation":
        return Summation(i.replace(replacements) for i in self.t)
