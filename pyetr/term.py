__all__ = ["FunctionalTerm", "Function", "ArbitraryObject"]

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .function import Function
from .multiset import Multiset


class Term(ABC):
    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def replace(
        self,
        replacements: dict["ArbitraryObject", "Term"],
    ) -> "Term":
        ...

    @property
    @abstractmethod
    def arb_objects(self) -> set["ArbitraryObject"]:
        ...


class ArbitraryObject(Term):
    name: str

    def __init__(self, name: str):
        self.name = name

    @property
    def detailed(self) -> str:
        return f"<ArbitraryObject name={self.name}>"

    def __repr__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ArbitraryObject):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

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


class FunctionalTerm(Term):
    f: Function
    t: Optional[tuple[Term, ...]]

    def __init__(
        self,
        f: Function,
        t: Optional[tuple[Term, ...]] = None,
    ):
        if t is None and f.arity > 0:
            raise ValueError(
                "FunctionalTerm not supplied when Function arity is greater than 0"
            )
        elif t is not None and (len(t) != f.arity):
            raise ValueError(
                f"FunctionalTerm length {len(t)} did not match arity {f.arity}"
            )
        self.f = f
        self.t = t

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        if self.t is None:
            return output_set
        else:
            for term in self.t:
                if isinstance(term, FunctionalTerm) or isinstance(term, Summation):
                    output_set |= term.arb_objects
                elif isinstance(term, ArbitraryObject):
                    output_set.add(term)
                else:
                    assert False
            return output_set

    @property
    def detailed(self) -> str:
        if self.t is None:
            return f"<FunctionalTerm f={self.f.detailed} t=()>"
        return f"<FunctionalTerm f={self.f.detailed} t=({','.join(t.detailed for t in self.t)},)>"

    def __repr__(self) -> str:
        if self.f.arity == 0:
            return f"{self.f.name}"
        else:
            assert self.t is not None
            terms = ",".join([repr(i) for i in self.t])
            return f"{self.f.name}({terms})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionalTerm):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((self.f, self.t))

    def replace(
        self,
        replacements: dict[ArbitraryObject, Term],
    ) -> "FunctionalTerm":
        new_terms = []
        if self.t is None:
            return self
        for term in self.t:
            if term in replacements:
                replacement = replacements[term]
            else:
                if isinstance(term, FunctionalTerm) and term.t is not None:
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


class Summation(Term):
    t: Multiset[Term]

    def __init__(
        self,
        t: Iterable[Term],
    ):
        self.t = Multiset[Term](t)

    @property
    def detailed(self) -> str:
        raise NotImplementedError

    def replace(
        self,
        replacements: dict["ArbitraryObject", "Term"],
    ) -> "Summation":
        return Summation(i.replace(replacements) for i in self.t)

    @property
    def arb_objects(self) -> set["ArbitraryObject"]:
        a_objs = set()
        for term in self.t:
            a_objs |= term.arb_objects
        return a_objs
