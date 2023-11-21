from .abstract import Atom
from .atom_likes import DoAtomLike
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, Term


class DoAtom(DoAtomLike[PredicateAtom], Atom):
    def __invert__(self):
        return DoAtom(atoms=self.atoms, polarity=(not self.polarity))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs: set[ArbitraryObject] = set()
        for atom in self.atoms:
            output_objs |= atom.arb_objects
        return output_objs

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "DoAtom":
        return DoAtom({atom.replace(replacements) for atom in self.atoms})

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> "DoAtom":
        return DoAtom({atom.replace_term(old_term, new_term) for atom in self.atoms})
