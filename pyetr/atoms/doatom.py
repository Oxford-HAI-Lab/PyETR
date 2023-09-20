from typing import Self

from pyetr.atoms.terms.term import ArbitraryObject, Term

from .abstract import AbstractComplete
from .atom import Atom
from .atom_likes import DoAtomLike


class DoAtom(DoAtomLike[Atom], AbstractComplete):
    def __invert__(self):
        return DoAtom(atoms=self.atoms, polarity=(not self.polarity))

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs = set()
        for atom in self.atoms:
            output_objs |= atom.arb_objects
        return output_objs

    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        return DoAtom({atom.replace(replacements) for atom in self.atoms})

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> "DoAtom":
        return DoAtom({atom.replace_term(old_term, new_term) for atom in self.atoms})
