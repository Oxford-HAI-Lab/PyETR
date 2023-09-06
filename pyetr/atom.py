__all__ = ["Predicate", "Atom", "equals_predicate"]


from typing import cast

from .term import ArbitraryObject, Emphasis, Term


class Atom:
    predicate: "Predicate"
    terms: tuple[Term | ArbitraryObject | Emphasis, ...]
    emphasis_count: int

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
                emphasis_count += term.emphasis_count
            elif isinstance(term, Emphasis):
                emphasis_count += 1
        self.emphasis_count = emphasis_count
        self.terms = terms

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
        if self.emphasis_count == 1:
            for term in self.terms:
                if isinstance(term, Emphasis):
                    return term.term
                elif isinstance(term, Term) and term.emphasis_count > 0:
                    assert term.emphasis_count == 1
                    return term.emphasis_term
            assert False
        else:
            raise ValueError(
                f"Emphasis term requested for atom {self} - atom does not have exactly one emphasis"
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
        new_terms = [term.excluding_emphasis for term in self.terms]
        return Atom(predicate=self.predicate, terms=tuple(new_terms))

    def is_same_emphasis_context(self, other: "Atom") -> bool:
        if self.predicate != other.predicate and self.predicate != ~other.predicate:
            return False
        else:
            for x, y in zip(self.terms, other.terms):
                if not x.is_same_emphasis_context(y):
                    return False
            return True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Atom):
            return False
        return self.predicate == other.predicate and self.terms == other.terms

    def __hash__(self) -> int:
        return hash((self.predicate, self.terms))

    def get_issue_atoms(self) -> set["Atom"]:
        # Each atom is represented by a list of terms
        def _get_issue_terms(
            term: "Term | ArbitraryObject | Emphasis",
        ) -> list[Term] | list[Emphasis]:
            if isinstance(term, Term):
                if term.t is not None:
                    term_sets: list[Term] = []
                    for i, subterm in enumerate(term.t):
                        subterm_issues = _get_issue_terms(subterm)
                        for subterm_issue in subterm_issues:
                            new_terms = list(term.t)
                            new_terms[i] = subterm_issue
                            term_sets.append(Term(f=term.f, t=tuple(new_terms)))
                    return term_sets
                else:
                    return []
            elif isinstance(term, ArbitraryObject):
                return []
            elif isinstance(term, Emphasis):
                active_issue = Emphasis(term.term.excluding_emphasis)
                return [active_issue] + [
                    Emphasis(cast(Term, issue)) for issue in _get_issue_terms(term.term)
                ]
            else:
                assert False

        final_atoms: set[Atom] = set()
        for i, term in enumerate(self.terms):
            issue_terms = _get_issue_terms(term)
            for issue_term in issue_terms:
                new_terms = list(self.terms)
                new_terms[i] = issue_term

                final_atoms.add(Atom(predicate=self.predicate, terms=tuple(new_terms)))
        return final_atoms

    def integrate_issue_atoms(self, atoms: list["Atom"]) -> "Atom":
        return Atom(
            predicate=self.predicate,
            terms=tuple(
                [
                    term.integrate_issue_atoms([atom.terms[i] for atom in atoms])
                    for i, term in enumerate(self.terms)
                ]
            ),
        )


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
