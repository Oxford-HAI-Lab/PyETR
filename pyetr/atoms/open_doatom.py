from typing import Self

from .abstract import AbstractOpen
from .atom_likes import DoAtomLike
from .doatom import DoAtom
from .open_predicate_atom import OpenPredicateAtom
from .terms import ArbitraryObject, Term


class OpenDoAtom(DoAtomLike[OpenPredicateAtom], AbstractOpen):
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        return OpenDoAtom({atom.replace(replacements) for atom in self.atoms})

    def __invert__(self) -> Self:
        return OpenDoAtom(self.atoms, not self.polarity)

    def __call__(self, term: Term) -> DoAtom:
        return DoAtom(atoms={atom(term) for atom in self.atoms})
