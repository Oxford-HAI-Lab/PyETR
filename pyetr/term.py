__all__ = ["Term", "Function", "Emphasis", "ArbitraryObject"]

from typing import Optional


class Function:
    name: str
    arity: int

    def __init__(self, name: str, arity: int) -> None:
        if arity < 0:
            raise ValueError("arity must not be less than 0")
        self.name = name
        self.arity = arity

    def __repr__(self) -> str:
        return f"Function({self.name}, {self.arity})"

    def identical(self, other) -> bool:
        if not isinstance(other, Function):
            return False
        return self.name == other.name and self.arity == other.arity


class ArbitraryObject:
    name: str
    is_existential: bool

    def __init__(self, name: str, *, is_existential: bool):
        self.name = name
        self.is_existential = is_existential

    def __repr__(self) -> str:
        if self.is_existential:
            s = "Exi"
        else:
            s = "Uni"
        return f"<ArbitraryObject ({s}) name={self.name}>"

    def identical(self, other) -> bool:
        if not isinstance(other, ArbitraryObject):
            return False
        return self.name == other.name and self.is_existential == other.is_existential


class Emphasis:
    term: "Term | ArbitraryObject"

    def __init__(self, t: "Term | ArbitraryObject") -> None:
        self.term = t

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        subterm = self.term
        if isinstance(subterm, Term):
            output_set |= subterm.arb_objects
        elif isinstance(subterm, ArbitraryObject):
            output_set.add(subterm)
        else:
            assert False
        return output_set

    def __repr__(self) -> str:
        return f"<Emphasis term={self.term}>"

    def identical(self, other) -> bool:
        if not isinstance(other, Emphasis):
            return False
        return self.term == other.term


class Term:
    f: Function
    t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]]
    has_emphasis: bool

    def __init__(
        self,
        f: Function,
        t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]] = None,
    ):
        if t is None and f.arity > 0:
            raise ValueError("Term not supplied when Function arity is greater than 0")
        elif t is not None and (len(t) != f.arity):
            raise ValueError(f"Term length {len(t)} did not match arity {f.arity}")
        self.f = f
        self.t = t
        if t is None:
            self.has_emphasis = False
        else:
            emphasis_count = self._count_emphasis(t)
            if emphasis_count > 1:
                raise ValueError(
                    f"Emphasis in term with func: {self.f} greater than 1. Count: {emphasis_count})"
                )
            else:
                self.has_emphasis = emphasis_count == 1

    def identical(self, other: "Term | ArbitraryObject | Function") -> bool:
        if not isinstance(other, Term):
            return False
        if self.t is None and other.t is None:
            terms_equal = True
        elif self.t is None or other.t is None:
            terms_equal = False
        else:
            terms_equal = True
            for i, term in enumerate(self.t):
                other_term = other.t[i]
                if term != other_term:
                    terms_equal = False

        return self.f == other.f and terms_equal

    @staticmethod
    def _count_emphasis(t: tuple["Term | ArbitraryObject | Emphasis", ...]) -> int:
        emphasis_count = 0
        for element in t:
            if isinstance(element, Emphasis):
                emphasis_count += 1
            elif isinstance(element, Term):
                emphasis_count += element.has_emphasis

        return emphasis_count

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        if self.t is None:
            return output_set
        else:
            for term in self.t:
                if isinstance(term, Term) or isinstance(term, Emphasis):
                    output_set |= term.arb_objects
                elif isinstance(term, ArbitraryObject):
                    output_set.add(term)
                else:
                    assert False
            return output_set

    def __repr__(self) -> str:
        return f"<Term f={self.f} t={self.t}>"


# Changed if clause in 4.2 to separate Arbitrary Objects from Term
