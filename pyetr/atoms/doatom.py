from typing import Self

from .abstract import AbstractComplete
from .atom_likes import DoAtomLike
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, Term


class DoAtom(DoAtomLike[PredicateAtom], AbstractComplete):
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
