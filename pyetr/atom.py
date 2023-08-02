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
            raise ValueError(
                f"Inconsistent - number of terms does not equal arity in {terms} for predicate {predicate}"
            )
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

    @property
    def detailed(self) -> str:
        return f"<Atom predicate={self.predicate.detailed} terms=({','.join(t.detailed for t in self.terms)})>"

    def __repr__(self) -> str:
        terms = ",".join([repr(i) for i in self.terms])
        if self.predicate.verifier:
            tilda = ""
        else:
            tilda = "~"
        return f"{tilda}{self.predicate.name}({terms})"

    def __invert__(self):
        return Atom(~self.predicate, self.terms)

    @property
    def emphasis_term(self) -> Term | ArbitraryObject:
        if self.has_emphasis:
            for term in self.terms:
                if isinstance(term, Emphasis):
                    return term.term
                elif isinstance(term, Term) and term.has_emphasis:
                    return term.emphasis_term
            assert False
        else:
            raise ValueError(
                f"Emphasis term requested for atom {self} - atom has no emphasis"
            )

    def replace_emphasis(
        self, existing: Emphasis, new: Term | ArbitraryObject | Emphasis
    ) -> "Atom":
        new_terms = []
        for term in self.terms:
            if term == existing:
                replacement = new
            else:
                if isinstance(term, Term) and term.t is not None:
                    replacement = term.replace_emphasis(existing=existing, new=new)
                elif isinstance(term, Term) and term.t is None:
                    replacement = term
                elif isinstance(term, Emphasis):
                    assert False
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return Atom(predicate=self.predicate, terms=tuple(new_terms))

    def replace(
        self, replacements: dict[ArbitraryObject, Term | ArbitraryObject]
    ) -> "Atom":
        new_terms = []
        for term in self.terms:
            if term in replacements:
                assert not isinstance(term, Term)
                replacement = replacements[term]
            else:
                if isinstance(term, Term) and term.t is not None:
                    replacement = term.replace(replacements)
                elif isinstance(term, Term) and term.t is None:
                    replacement = term
                elif isinstance(term, Emphasis):
                    replacement = term.replace(replacements)
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return Atom(predicate=self.predicate, terms=tuple(new_terms))

    def replace_low_level(
        self,
        old_term: Term | ArbitraryObject | Emphasis,
        new_term: Term | ArbitraryObject | Emphasis,
    ) -> "Atom":
        new_terms = []
        for term in self.terms:
            if old_term == term:
                new_terms.append(new_term)
            elif isinstance(term, ArbitraryObject):
                new_terms.append(old_term)

        return Atom(predicate=self.predicate, terms=tuple(new_terms))

    @property
    def excluding_emphasis(self) -> "Atom":
        if self.has_emphasis:
            new_term = self.emphasis_term
            return self.replace_emphasis(existing=Emphasis(new_term), new=new_term)
        else:
            return self

    def is_same_excl_emphasis(self, other: "Atom") -> bool:
        if self.predicate != other.predicate:
            return False
        else:
            return self.excluding_emphasis == other.excluding_emphasis

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
        return Predicate(name=self.name, arity=self.arity, _verifier=not self.verifier)

    def __repr__(self) -> str:
        return f"<Predicate name={self.name} arity={self.arity}>"

    @property
    def detailed(self) -> str:
        return repr(self)

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
