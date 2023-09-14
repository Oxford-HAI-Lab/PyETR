from abc import ABC, abstractmethod
from typing import Iterable, Optional

from pyetr.multiset import Multiset
from pyetr.term import ArbitraryObject, FunctionalTerm, Summation, Term

from .abstract_atom import AbstractAtom, Predicate
from .atom import Atom
from .function import Function


class OpenTerm(ABC):
    @abstractmethod
    def question_count(self) -> int:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenTerm":
        ...

    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def __call__(self, term: Term) -> Term:
        ...


class OpenArbitraryObject(OpenTerm):
    name: str

    def __init__(self, name: str):
        self.name = name

    def __call__(self, term: Term) -> ArbitraryObject:
        return ArbitraryObject(name=self.name)

    def question_count(self) -> int:
        return 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, OpenArbitraryObject):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> OpenTerm:
        for arb_obj in replacements:
            if arb_obj.name == self.name:
                return get_open_equivalent(replacements[arb_obj])
        return self

    @property
    def detailed(self) -> str:
        return f"<ArbitraryObject name={self.name}>"

    def __repr__(self) -> str:
        return f"{self.name}"


class OpenFunctionalTerm(OpenTerm):
    f: Function
    t: Optional[tuple[OpenTerm, ...]]

    def __init__(self, f: Function, t: Optional[tuple[OpenTerm, ...]]) -> None:
        self.f = f
        self.t = t

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, OpenFunctionalTerm):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((self.f, self.t))

    def replace(
        self, replacements: dict[ArbitraryObject, Term]
    ) -> "OpenFunctionalTerm":
        if self.t is None:
            return OpenFunctionalTerm(f=self.f, t=None)
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenFunctionalTerm(f=self.f, t=new_terms)

    @property
    def detailed(self) -> str:
        if self.t is None:
            return f"<OpenFunctionalTerm f={self.f.detailed} t=()>"
        return f"<OpenFunctionalTerm f={self.f.detailed} t=({','.join(t.detailed for t in self.t)},)>"

    def __repr__(self) -> str:
        if self.f.arity == 0:
            return f"{self.f.name}"
        else:
            assert self.t is not None
            terms = ",".join([repr(i) for i in self.t])
            return f"{self.f.name}({terms})"


class OpenSummation(OpenTerm):
    t: Multiset[OpenTerm]

    def __init__(
        self,
        t: Iterable[OpenTerm],
    ):
        self.t = Multiset[OpenTerm](t)

    def __call__(self, term: Term) -> Summation:
        return Summation(t=tuple([i(term) for i in self.t]))

    def question_count(self) -> int:
        c = 0
        for i in self.t:
            c += i.question_count()
        return c

    def __eq__(self, other) -> bool:
        if not isinstance(other, OpenFunctionalTerm):
            return False
        return self.t == other.t

    def __hash__(self) -> int:
        return hash(self.t)

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenSummation":
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenSummation(t=new_terms)

    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def detailed(self) -> str:
        return f"<OpenSummation {self.t}>"


class QuestionMark(OpenTerm):
    def question_count(self) -> int:
        return 1

    def __eq__(self, other) -> bool:
        if isinstance(other, QuestionMark):
            return True
        else:
            return False

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "QuestionMark":
        return self

    def __repr__(self) -> str:
        return "?"

    def __hash__(self) -> int:
        return hash("?")

    @property
    def detailed(self) -> str:
        return f"<QuestionMark>"

    def __call__(self, term: Term) -> Term:
        return term


class OpenAtom(AbstractAtom[OpenTerm]):
    def __init__(self, predicate: Predicate, terms: tuple[OpenTerm, ...]) -> None:
        super().__init__(predicate=predicate, terms=terms)
        self.validate()

    def __call__(self, term: Term) -> Atom:
        return Atom(
            predicate=self.predicate, terms=tuple([t(term) for t in self.terms])
        )

    def question_count(self) -> int:
        question_count = 0
        for term in self.terms:
            question_count += term.question_count()
        return question_count

    def validate(self):
        if self.question_count() != 1:
            raise ValueError(f"Open atom {self} must contain exactly one question mark")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OpenAtom):
            return False
        return self.predicate == other.predicate and self.terms == other.terms

    def __hash__(self) -> int:
        return hash((self.predicate, self.terms))

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenAtom":
        new_terms = tuple([term.replace(replacements) for term in self.terms])
        return OpenAtom(predicate=self.predicate, terms=new_terms)

    def __invert__(self):
        return OpenAtom(~self.predicate, self.terms)

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self.terms])
        if self.predicate.verifier:
            tilda = ""
        else:
            tilda = "~"
        return f"{tilda}{self.predicate.name}({terms})"

    @property
    def detailed(self) -> str:
        return f"<OpenAtom predicate={self.predicate.detailed} terms=({','.join(t.detailed for t in self.terms)})>"


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
