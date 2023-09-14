from abc import abstractmethod
from types import NoneType
from typing import Iterable, Optional

from pyetr.multiset import Multiset
from pyetr.term import ArbitraryObject, FunctionalTerm, Summation, Term

from .abstract_atom import AbstractAtom, Predicate
from .atom import Atom
from .function import Function


class OpenTerm:
    @abstractmethod
    def question_count(self) -> int:
        ...

    @abstractmethod
    def is_same_emphasis_context(self, other: "OpenTerm") -> bool:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenTerm":
        ...

    @abstractmethod
    def refers_to_term(self, term: Term) -> bool:
        ...

    @classmethod
    @abstractmethod
    def get_open_equiv(cls, term: Term) -> "OpenTerm":
        ...

    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def get_question_term(self, term: Term) -> Optional["Term"]:
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

    def is_same_emphasis_context(self, other: OpenTerm) -> bool:
        return self == other

    def __eq__(self, other) -> bool:
        if not isinstance(other, OpenArbitraryObject):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def refers_to_term(self, term: ArbitraryObject) -> bool:
        return term.name == self.name

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> OpenTerm:
        for arb_obj in replacements:
            if self.refers_to_term(arb_obj):
                return get_open_equivalent(replacements[arb_obj])
        return self

    @property
    def detailed(self) -> str:
        raise NotImplementedError

    def get_question_term(self, term: ArbitraryObject) -> NoneType:
        return None


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

    def is_same_emphasis_context(self, other: OpenTerm) -> bool:
        if not isinstance(other, OpenFunctionalTerm) or self.f != other.f:
            return False
        if self.t is None and other.t is None:
            return True
        elif self.t is None or other.t is None:
            return False
        else:
            for x, y in zip(self.t, other.t):
                if not x.is_same_emphasis_context(y):
                    return False
            return True

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
        raise NotImplementedError

    def get_question_term(self, term: FunctionalTerm) -> Optional[Term]:
        if self.t is None:
            return None
        for open_term in self.t:
            q_term = open_term.get_question_term(term)
            if q_term is not None:
                return q_term
        return None


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

    def is_same_emphasis_context(self, other: OpenTerm) -> bool:
        if not isinstance(other, OpenFunctionalTerm):
            return False
        if self.t is None and other.t is None:
            return True
        elif self.t is None or other.t is None:
            return False
        else:
            for x, y in zip(self.t, other.t):
                if not x.is_same_emphasis_context(y):
                    return False
            return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, OpenFunctionalTerm):
            return False
        return self.t == other.t

    def __hash__(self) -> int:
        return hash(self.t)

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenSummation":
        new_terms = tuple([term.replace(replacements) for term in self.t])
        return OpenSummation(t=new_terms)

    @property
    def detailed(self) -> str:
        return f"<OpenSummation {self.t}>"

    def get_question_term(self, term: FunctionalTerm) -> Optional[Term]:
        if self.t is None:
            return None
        for open_term in self.t:
            q_term = open_term.get_question_term(term)
            if q_term is not None:
                return q_term
        return None


class QuestionMark(OpenTerm):
    def question_count(self) -> int:
        return 1

    def is_same_emphasis_context(self, other: OpenTerm) -> bool:
        return True

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

    def get_question_term(self, term: Term) -> Optional[Term]:
        return term

    def refers_to_term(self, term: Term) -> bool:
        assert False


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

    def refers_to_atom(self, atom: Atom) -> bool:
        if self.predicate != atom.predicate and self.predicate != ~atom.predicate:
            return False
        all_terms_match = True
        for i, term in enumerate(atom.terms):
            alt_open_term = get_open_equivalent(term)
            open_term = self.terms[i]
            if not open_term.is_same_emphasis_context(alt_open_term):
                all_terms_match = False
        return all_terms_match

    def present_in_atoms(self, atoms: set[Atom]) -> bool:
        return any([self.refers_to_atom(a) for a in atoms])

    def is_same_question_context(self, other: "OpenAtom") -> bool:
        if self.predicate != other.predicate and self.predicate != ~other.predicate:
            return False
        else:
            for x, y in zip(self.terms, other.terms):
                if not x.is_same_emphasis_context(y):
                    return False
            return True

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

    def get_question_term_for_atom(self, atom: Atom) -> Term:
        assert self.predicate.name == atom.predicate.name
        assert len(self.terms) == len(atom.terms)
        for i, open_term in enumerate(self.terms):
            term = atom.terms[i]
            new_q_term = open_term.get_question_term(term)
            if new_q_term is not None:
                return new_q_term
        assert False


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
