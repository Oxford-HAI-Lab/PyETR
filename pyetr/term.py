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

    @property
    def detailed(self) -> str:
        return repr(self)

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

    def is_same_emphasis_context(
        self, other: "Term | ArbitraryObject | Emphasis"
    ) -> bool:
        return self == other

    @property
    def excluding_emphasis(self) -> "ArbitraryObject":
        return self

    @property
    def arb_objects(self) -> set["ArbitraryObject"]:
        return {self}

    def integrate_issue_atoms(
        self, terms: list["Term | ArbitraryObject | Emphasis"]
    ) -> "Emphasis | ArbitraryObject":
        for term in terms:
            if isinstance(term, Emphasis):
                return term
        return self

    def emphasis_count(self) -> int:
        return 0


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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Emphasis):
            return False
        return self.term == other.term

    def __hash__(self) -> int:
        return hash(("Emphasis", self.term))

    def replace(
        self,
        replacements: dict[ArbitraryObject, "Term | ArbitraryObject"],
    ) -> "Emphasis":
        if self.term in replacements:
            replacement = replacements[self.term]
        else:
            if isinstance(self.term, Term):
                replacement = self.term.replace(replacements)
            elif isinstance(self.term, ArbitraryObject):
                replacement = self.term
            else:
                assert False
        return Emphasis(t=replacement)

    @property
    def detailed(self) -> str:
        return f"<Emphasis term={self.term.detailed}>"

    def __repr__(self) -> str:
        return f"{self.term}*"

    def is_same_emphasis_context(
        self, other: "Term | ArbitraryObject | Emphasis"
    ) -> bool:
        return isinstance(other, Emphasis)

    @property
    def excluding_emphasis(self) -> "Term | ArbitraryObject":
        return self.term.excluding_emphasis

    def emphasis_count(self) -> int:
        return 1

    def integrate_issue_atoms(
        self, terms: list["Term | ArbitraryObject | Emphasis"]
    ) -> "Emphasis":
        return self


class Term:
    f: Function
    t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]]
    emphasis_count: int

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
            self.emphasis_count = 0
        else:
            self.emphasis_count = self._count_emphasis(t)

    @staticmethod
    def _count_emphasis(t: tuple["Term | ArbitraryObject | Emphasis", ...]) -> int:
        emphasis_count = 0
        for element in t:
            if isinstance(element, Emphasis):
                emphasis_count += 1
            elif isinstance(element, Term):
                emphasis_count += element.emphasis_count

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

    @property
    def detailed(self) -> str:
        if self.t is None:
            return f"<Term f={self.f.detailed} t=()>"
        return f"<Term f={self.f.detailed} t=({','.join(t.detailed for t in self.t)},)>"

    def __repr__(self) -> str:
        if self.f.arity == 0:
            return f"{self.f.name}"
        else:
            assert self.t is not None
            terms = ",".join([repr(i) for i in self.t])
            return f"f_{self.f.name}({terms})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Term):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((self.f, self.t))

    @property
    def excluding_emphasis(self) -> "Term":
        if self.t is None:
            return self
        else:
            new_subterms: list["Term | ArbitraryObject | Emphasis"] = [
                subterm.excluding_emphasis for subterm in self.t
            ]
            return Term(f=self.f, t=tuple(new_subterms))

    def integrate_issue_atoms(
        self, terms: list["Term | ArbitraryObject | Emphasis"]
    ) -> "Emphasis | Term":
        for term in terms:
            if isinstance(term, Emphasis):
                return term
        if self.t is None:
            return self

        return Term(
            f=self.f,
            t=tuple([t.integrate_issue_atoms(terms) for i, t in enumerate(self.t)]),
        )

    def replace_emphasis(
        self, existing: Emphasis, new: "Term | ArbitraryObject | Emphasis"
    ) -> "Term":
        new_terms = []
        if self.t is None:
            return self
        for term in self.t:
            if term == existing:
                replacement = new
            else:
                if isinstance(term, Term) and term.t is not None:
                    replacement = term.replace_emphasis(existing, new)
                elif isinstance(term, Emphasis):
                    assert False
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return Term(f=self.f, t=tuple(new_terms))

    def is_same_emphasis_context(
        self, other: "Term | ArbitraryObject | Emphasis"
    ) -> bool:
        if (
            isinstance(other, Emphasis)
            or isinstance(other, ArbitraryObject)
            or self.f != other.f
        ):
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

    def replace(
        self,
        replacements: dict[ArbitraryObject, "Term | ArbitraryObject"],
    ) -> "Term":
        new_terms = []
        if self.t is None:
            return self
        for term in self.t:
            if term in replacements:
                replacement = replacements[term]
            else:
                if isinstance(term, Term) and term.t is not None:
                    replacement = term.replace(replacements)
                elif isinstance(term, Emphasis):
                    replacement = term.replace(replacements)
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return Term(f=self.f, t=tuple(new_terms))

    @property
    def emphasis_term(self) -> "Term | ArbitraryObject":
        if self.emphasis_count == 1 and self.t is not None:
            for term in self.t:
                if isinstance(term, Emphasis):
                    return term.term
                elif isinstance(term, Term):
                    if term.emphasis_count > 0:
                        assert term.emphasis_count == 1
                        return term.emphasis_term
            assert False
        else:
            raise ValueError(
                f"Emphasis term requested for term {self} - term does not have exactly one emphasis"
            )


# Changed if clause in 4.2 to separate Arbitrary Objects from Term
