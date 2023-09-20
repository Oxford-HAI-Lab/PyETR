__all__ = ["PredicateAtom"]


from .abstract import AbstractComplete
from .atom_likes import PredicateAtomLike
from .terms import ArbitraryObject, FunctionalTerm, Multiset, Term


class PredicateAtom(PredicateAtomLike[Term], AbstractComplete):
    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs = set()
        for term in self.terms:
            if isinstance(term, FunctionalTerm) or isinstance(term, Multiset):
                output_objs |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_objs.add(term)
            else:
                assert False
        return output_objs

    def __invert__(self):
        return PredicateAtom(~self.predicate, self.terms)

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "PredicateAtom":
        new_terms = []
        for term in self.terms:
            if term in replacements:
                assert not isinstance(term, FunctionalTerm)
                replacement = replacements[term]
            else:
                if isinstance(term, FunctionalTerm):
                    replacement = term.replace(replacements)
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return PredicateAtom(predicate=self.predicate, terms=tuple(new_terms))

    def replace_low_level(
        self,
        old_term: Term,
        new_term: Term,
    ) -> "PredicateAtom":
        new_terms = []
        for term in self.terms:
            if old_term == term:
                new_terms.append(new_term)
            elif isinstance(term, ArbitraryObject):
                new_terms.append(old_term)

        return PredicateAtom(predicate=self.predicate, terms=tuple(new_terms))

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ):
        new_terms = [
            term.replace_term(old_term=old_term, new_term=new_term)
            for term in self.terms
        ]
        return PredicateAtom(predicate=self.predicate, terms=tuple(new_terms))
