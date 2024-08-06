from .abstract import Atom, OpenAtom
from .atom_likes import DoAtomLike
from .doatom import DoAtom
from .open_predicate_atom import OpenPredicateAtom
from .predicate_atom import PredicateAtom
from .terms import ArbitraryObject, Term


def set_context_equals(
    open_atom_set: set[OpenPredicateAtom],
    pred_atom_set: set[PredicateAtom],
    question_term: "Term",
) -> bool:
    if len(open_atom_set) != len(pred_atom_set):
        return False
    open_items = list(open_atom_set)
    pred_items = list(pred_atom_set)
    items_found = 0
    while open_items and pred_items:
        open_pred = open_items.pop()
        for pred_atom in pred_items:
            if open_pred.context_equals(pred_atom, question_term):
                pred_items.remove(pred_atom)
                items_found += 1
                break
    return items_found == len(open_atom_set)


class OpenDoAtom(DoAtomLike[OpenPredicateAtom], OpenAtom):
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> "OpenDoAtom":
        return OpenDoAtom({atom.replace(replacements) for atom in self.atoms})

    def __invert__(self) -> "OpenDoAtom":
        return OpenDoAtom(self.atoms, not self.polarity)

    def __call__(self, term: Term) -> DoAtom:
        return DoAtom(atoms={atom(term) for atom in self.atoms})

    def question_count(self) -> int:
        question_count = 0
        for atom in self.atoms:
            question_count += atom.question_count()
        return question_count

    def context_equals(self, atom: "Atom", question_term: "Term") -> bool:
        if not isinstance(atom, DoAtom):
            return False
        return self.polarity == atom.polarity and set_context_equals(
            self.atoms, atom.atoms, question_term
        )
