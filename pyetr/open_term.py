from abc import abstractmethod

from pyetr.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractMultiset,
    AbstractTerm,
)
from pyetr.term import ArbitraryObject, FunctionalTerm, Multiset, Term


class OpenTerm(AbstractTerm):
    @abstractmethod
    def question_count(self) -> int:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenTerm":
        ...

    @abstractmethod
    def __call__(self, term: Term) -> Term:
        ...


class OpenArbitraryObject(AbstractArbitraryObject, OpenTerm):
    def __call__(self, term: Term) -> ArbitraryObject:
        return ArbitraryObject(name=self.name)

    def question_count(self) -> int:
        return 0

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> OpenTerm:
        for arb_obj in replacements:
            if arb_obj.name == self.name:
                return get_open_equivalent(replacements[arb_obj])
        return self


class OpenFunctionalTerm(AbstractFunctionalTerm[OpenTerm], OpenTerm):
    def __call__(self, term: Term) -> FunctionalTerm:
        return FunctionalTerm(f=self.f, t=tuple([i(term) for i in self.t]))

    def question_count(self) -> int:
        c = 0
        for i in self.t:
            c += i.question_count()
        return c

    def replace(
        self, replacements: dict[ArbitraryObject, Term]
    ) -> "OpenFunctionalTerm":
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenFunctionalTerm(f=self.f, t=new_terms)


class QuestionMark(OpenTerm):
    def __eq__(self, other) -> bool:
        if isinstance(other, QuestionMark):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return "?"

    def __hash__(self) -> int:
        return hash("?")

    @property
    def detailed(self) -> str:
        return f"<QuestionMark>"

    def __call__(self, term: Term) -> Term:
        return term

    def question_count(self) -> int:
        return 1

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "QuestionMark":
        return self


class OpenMultiset(AbstractMultiset[OpenTerm], OpenTerm):
    def __call__(self, term: Term) -> Multiset:
        return Multiset(tuple([i(term) for i in self]))

    def question_count(self) -> int:
        c = 0
        for i in self:
            c += i.question_count()
        return c

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenMultiset":
        return OpenMultiset(tuple([term.replace(replacements) for term in self]))

    def __add__(self, other: "OpenMultiset") -> "OpenMultiset":
        return OpenMultiset(self._items + other._items)


def get_open_equivalent(term: Term) -> OpenTerm:
    if isinstance(term, ArbitraryObject):
        return OpenArbitraryObject(term.name)
    elif isinstance(term, FunctionalTerm):
        return OpenFunctionalTerm(
            f=term.f, t=tuple([get_open_equivalent(i) for i in term.t])
        )
    elif isinstance(term, Multiset):
        return OpenMultiset(get_open_equivalent(i) for i in term)
    else:
        assert False
