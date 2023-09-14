from abc import abstractmethod

from pyetr.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractSummation,
    AbstractTerm,
)
from pyetr.term import ArbitraryObject, FunctionalTerm, Summation, Term


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
        if self.t is None:
            return FunctionalTerm(f=self.f, t=None)
        else:
            return FunctionalTerm(f=self.f, t=tuple([i(term) for i in self.t]))

    def question_count(self) -> int:
        if self.t is None:
            return 0
        c = 0
        for i in self.t:
            c += i.question_count()
        return c

    def replace(
        self, replacements: dict[ArbitraryObject, Term]
    ) -> "OpenFunctionalTerm":
        if self.t is None:
            return OpenFunctionalTerm(f=self.f, t=None)
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenFunctionalTerm(f=self.f, t=new_terms)


class OpenSummation(AbstractSummation, OpenTerm):
    def __call__(self, term: Term) -> Summation:
        return Summation(t=tuple([i(term) for i in self.t]))

    def question_count(self) -> int:
        c = 0
        for i in self.t:
            c += i.question_count()
        return c

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenSummation":
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenSummation(t=new_terms)


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


def get_open_equivalent(term: Term) -> OpenTerm:
    if isinstance(term, ArbitraryObject):
        return OpenArbitraryObject(term.name)
    elif isinstance(term, FunctionalTerm):
        if term.t is None:
            new_terms = None
        else:
            new_terms = tuple([get_open_equivalent(i) for i in term.t])
        return OpenFunctionalTerm(f=term.f, t=new_terms)
    elif isinstance(term, Summation):
        return OpenSummation(t=(get_open_equivalent(i) for i in term.t))
    else:
        assert False
