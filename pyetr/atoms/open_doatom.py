from typing import Self

from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_atom import OpenAtom
from pyetr.atoms.terms.term import ArbitraryObject, Term

from .abstract import AbstractOpen
from .atom_likes import DoAtomLike


class OpenDoAtom(DoAtomLike[OpenAtom], AbstractOpen):
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        return OpenDoAtom({atom.replace(replacements) for atom in self.atoms})

    def __invert__(self) -> Self:
        return OpenDoAtom(self.atoms, not self.polarity)

    def __call__(self, term: Term) -> DoAtom:
        return DoAtom(atoms={atom(term) for atom in self.atoms})
