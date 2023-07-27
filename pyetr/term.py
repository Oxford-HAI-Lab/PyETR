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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Function):
            return False
        if self.name == other.name and not (self.arity == other.arity):
            raise ValueError(
                f"Equality on two functions of same name {self.name}, {other.name}, different arity {self.arity}, {other.arity}"
            )
        return self.name == other.name and self.arity == other.arity

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.arity)


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

    def __eq__(self, other) -> bool:
        if not isinstance(other, ArbitraryObject):
            return False
        return self.name == other.name and self.is_existential == other.is_existential

    def __hash__(self) -> int:
        return hash((self.name, self.is_existential))


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

    def __eq__(self, other) -> bool:
        # TODO: Is this right?
        if not isinstance(other, Emphasis):
            return False
        return self.term == other.term

    def __hash__(self) -> int:
        return hash(("Emphasis", self.term))


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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Term):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((self.f, self.t))


# Changed if clause in 4.2 to separate Arbitrary Objects from Term
