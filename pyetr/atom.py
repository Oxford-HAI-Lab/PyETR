__all__ = ["Atom"]


from pyetr.abstract_atom import AbstractAtom

from .term import ArbitraryObject, FunctionalTerm, Summation, Term


class Atom(AbstractAtom[Term]):
    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs = set()
        for term in self.terms:
            if isinstance(term, FunctionalTerm) or isinstance(term, Summation):
                output_objs |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_objs.add(term)
            else:
                assert False
        return output_objs

    def __invert__(self):
        return Atom(~self.predicate, self.terms)

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "Atom":
        new_terms = []
        for term in self.terms:
            if term in replacements:
                assert not isinstance(term, FunctionalTerm)
                replacement = replacements[term]
            else:
                if isinstance(term, FunctionalTerm) and term.t is not None:
                    replacement = term.replace(replacements)
                elif isinstance(term, FunctionalTerm) and term.t is None:
                    replacement = term
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return Atom(predicate=self.predicate, terms=tuple(new_terms))

    def replace_low_level(
        self,
        old_term: Term,
        new_term: Term,
    ) -> "Atom":
        new_terms = []
        for term in self.terms:
            if old_term == term:
                new_terms.append(new_term)
            elif isinstance(term, ArbitraryObject):
                new_terms.append(old_term)

        return Atom(predicate=self.predicate, terms=tuple(new_terms))
