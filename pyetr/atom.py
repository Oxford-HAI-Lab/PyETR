__all__ = ["Predicate", "Atom", "equals_predicate"]

from .term import ArbitraryObject, Emphasis, Term


class Atom:
    predicate: "Predicate"
    terms: tuple[Term | ArbitraryObject | Emphasis, ...]
    has_emphasis: bool

    def __init__(
        self,
        predicate: "Predicate",
        terms: tuple[Term | ArbitraryObject | Emphasis, ...],
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError(f"Inconsistent - number of terms does not equal arity")
        self.predicate = predicate
        emphasis_count = 0
        for term in terms:
            if isinstance(term, Term):
                emphasis_count += term.has_emphasis
            elif isinstance(term, Emphasis):
                emphasis_count += 1
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in atom at: {emphasis_count}")
        else:
            self.has_emphasis = emphasis_count == 1
        self.terms = terms

        # Invarient: atom has one or 0 emphasis

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs = set()
        for term in self.terms:
            if isinstance(term, Term) or isinstance(term, Emphasis):
                output_objs |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_objs.add(term)
            else:
                assert False
        return output_objs

    def __repr__(self) -> str:
        return f"<Atom predicate={self.predicate} terms={self.terms}>"

    def __invert__(self):
        return Atom(~self.predicate, self.terms)

    def is_same_excl_emphasis(self, other: "Atom") -> bool:
        raise NotImplementedError

    @property
    def emphasis_term(self) -> Term | ArbitraryObject:
        raise NotImplementedError

    def replace(
        self,
        old_term: Term | ArbitraryObject | Emphasis,
        new_term: Term | ArbitraryObject | Emphasis,
    ) -> "Atom":
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Atom):
            return False
        return self.predicate == other.predicate and self.terms == other.terms

    def __hash__(self) -> int:
        return hash((self.predicate, self.terms))


class Predicate:
    name: str
    verifier: bool
    arity: int

    def __init__(self, name: str, arity: int, _verifier: bool = True) -> None:
        self.verifier = _verifier
        self.name = name
        self.arity = arity

    def __invert__(self):
        return Predicate(self.name, not self.verifier)

    def __repr__(self) -> str:
        return f"<Predicate name={self.name} arity={self.arity}>"

    def __call__(self, terms: tuple[Term | ArbitraryObject | Emphasis, ...]) -> Atom:
        return Atom(self, terms)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Predicate):
            return False
        return (
            self.name == other.name
            and self.arity == other.arity
            and self.verifier == other.verifier
        )

    def __hash__(self) -> int:
        return hash((self.name, self.arity, self.verifier))


equals_predicate = Predicate("=", 2)
