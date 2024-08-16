from typing import Iterable

from pyetr.atoms.terms.multiset import Multiset

from .abstract import Atom
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, Term


class DoAtom(Atom):
    """
    This "AtomLike" is a mixin for the doatom-like properties associated
    with DoAtom and OpenDoAtom
    """

    atoms: set[PredicateAtom]
    polarity: bool

    def __init__(self, atoms: Iterable[PredicateAtom], polarity: bool = True) -> None:
        self.atoms = set(atoms)
        self.polarity = polarity

    @property
    def detailed(self) -> str:
        return f"<{type(self).__name__} polarity={self.polarity} atoms=({','.join(a.detailed for a in self.atoms)})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.atoms == other.atoms and self.polarity == other.polarity

    def __hash__(self) -> int:
        return hash((type(self).__name__, frozenset(self.atoms), self.polarity))

    def __repr__(self) -> str:
        terms = "".join([repr(i) for i in self.atoms])
        if self.polarity:
            tilde = ""
        else:
            tilde = "~"
        return f"{tilde}do({terms})"

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
