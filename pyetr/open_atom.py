

from abc import abstractmethod
from typing import Optional
from pyetr.abstract_atom import AbstractPredicate

from pyetr.multiset import Multiset
from .atom import Atom
from .abstract_atom import AbstractAtom
from .function import Function

class OpenTerm:
    @abstractmethod
    def question_count(self) -> int:
        ...
    
    @abstractmethod
    def is_same_emphasis_context(
        self, other: "OpenTerm"
    ) -> bool:
        ...

class OpenArbitraryObject(OpenTerm):
    name: str

    def __init__(self, name: str):
        self.name = name

    def question_count(self) -> int:
        return 0

class OpenFunctionalTerm(OpenTerm):
    f: Function
    t: Optional[tuple[OpenTerm, ...]]

    def __init__(self, f: Function, t: Optional[tuple[OpenTerm, ...]]) -> None:
        self.f = f
        self.t = t

    def question_count(self) -> int:
        if self.t is None:
            return 0
        c = 0
        for i in self.t:
            c+= i.question_count()
        return c


class OpenSummation(OpenTerm):
    t: Multiset[OpenTerm]

    def question_count(self) -> int:
        c = 0
        for i in self.t:
            c+= i.question_count()
        return c

class QuestionMark(OpenTerm):
    def question_count(self) -> int:
        return 1



class OpenAtom(AbstractAtom[OpenTerm]):
    def __init__(self, predicate: AbstractPredicate[OpenTerm], terms: tuple[OpenTerm, ...]) -> None:
        super().__init__(predicate=predicate, terms=terms)
        self.validate()

    def question_count(self):
        question_count = 0
        for term in self.terms:
            question_count += term.question_count()
    
    def validate(self):
        if self.question_count() != 1:
            raise ValueError(f"Open atom {self} must contain exactly one question mark")

    def refers_to_atom(self, atom: Atom) -> bool:
        raise NotImplementedError

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