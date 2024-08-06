from abc import abstractmethod

from pyetr.atoms.terms import Multiset

from .abstract_term import AbstractArbitraryObject, AbstractFunctionalTerm, AbstractTerm
from .term import ArbitraryObject, FunctionalTerm, Term


def multiset_context_equals(
    open_term_set: Multiset["OpenTerm"],
    term_set: Multiset["Term"],
    question_term: "Term",
) -> bool:
    if len(open_term_set) != len(term_set):
        return False
    open_items = list(open_term_set)
    pred_items = list(term_set)
    items_found = 0
    while open_items and pred_items:
        open_pred = open_items.pop()
        for pred_atom in pred_items:
            if open_pred.context_equals(pred_atom, question_term):
                pred_items.remove(pred_atom)
                items_found += 1
                break
    return items_found == len(open_term_set)


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

    @abstractmethod
    def context_equals(self, term: "Term", question_term: "Term") -> bool:
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

    def context_equals(self, term: "Term", question_term: "Term") -> bool:
        if not isinstance(term, ArbitraryObject):
            return False
        return get_open_equivalent(term) == self


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

    def context_equals(self, term: "Term", question_term: "Term") -> bool:
        if not isinstance(term, FunctionalTerm) or self.f != term.f:
            return False
        if isinstance(self.t, Multiset):
            assert isinstance(term.t, Multiset)
            return multiset_context_equals(self.t, term.t, question_term)
        else:
            assert isinstance(term.t, tuple)
            return all(
                t.context_equals(term.t[i], question_term) for i, t in enumerate(self.t)
            )


class QuestionMark(OpenTerm):
    def __eq__(self, other: object) -> bool:
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

    def context_equals(self, term: "Term", question_term: "Term") -> bool:
        return term == question_term


def get_open_equivalent(term: Term) -> OpenTerm:
    """
    Gets the open equivalent of a term replacing all terms with
    their open counterparts.

    Args:
        term (Term): Input term

    Returns:
        OpenTerm: Output open term
    """
    if isinstance(term, ArbitraryObject):
        return OpenArbitraryObject(term.name)
    elif isinstance(term, FunctionalTerm):
        if term.f.arity is None:
            return OpenFunctionalTerm(
                f=term.f, t=Multiset[OpenTerm]([get_open_equivalent(i) for i in term.t])
            )
        else:
            return OpenFunctionalTerm(
                f=term.f, t=tuple([get_open_equivalent(i) for i in term.t])
            )
    else:
        assert False
