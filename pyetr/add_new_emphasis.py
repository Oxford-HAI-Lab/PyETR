__all__ = ["add_new_emphasis"]

import random
from functools import reduce
from typing import Optional

from pyetr.atom import Atom
from pyetr.term import ArbitraryObject, Emphasis, Function, Term

from .stateset import set_of_states, state


class AtomCandidate:
    """
    A candidate from an atom
    """

    term: ArbitraryObject | Function | Term
    term_idx: int
    atom_occurrences: int

    def __init__(self, term: ArbitraryObject | Function | Term, term_idx: int) -> None:
        self.term = term
        self.term_idx = term_idx
        self.atom_occurrences = 1

    def identical(self, other: "AtomCandidate") -> bool:
        return self.term.identical(other.term)

    @property
    def is_universal(self):
        return isinstance(self.term, ArbitraryObject) and not self.term.is_existential

    @property
    def is_existential(self):
        return isinstance(self.term, ArbitraryObject) and self.term.is_existential

    @property
    def is_const(self):
        return isinstance(self.term, Function) and self.term.arity == 0

    def __repr__(self) -> str:
        return f"<AtomCand term={self.term} term_idx={self.term_idx} occur={self.atom_occurrences}>"


def type_x_beats_y(x: AtomCandidate, y: AtomCandidate) -> bool:
    # Universals have priority over existentials
    # Existentials have priority over functions with 0 arity
    # Terms have lower priority than functions
    if x.is_universal and not y.is_universal:
        return True
    elif x.is_existential and not y.is_existential:
        return True
    elif x.is_const and not y.is_const:
        return True
    else:
        return False


def compare_type(
    candidate1: AtomCandidate, candidate2: AtomCandidate
) -> Optional[AtomCandidate]:
    if type_x_beats_y(candidate1, candidate2):
        return candidate1
    elif type_x_beats_y(candidate2, candidate1):
        return candidate2
    else:
        return None


def get_atom_candidate(atom: Atom) -> AtomCandidate:
    current_candidate: Optional[AtomCandidate] = None
    for i, term in enumerate(atom.terms):
        assert not isinstance(term, Emphasis)
        new_candidate = AtomCandidate(term=term, term_idx=i)
        if current_candidate is None:
            current_candidate = new_candidate
        elif current_candidate.identical(new_candidate):
            current_candidate.atom_occurrences += 1
        else:
            comparison = compare_type(current_candidate, new_candidate)
            # If it's a draw, previous candidate in atom wins
            if comparison is not None:
                current_candidate = new_candidate
    assert current_candidate is not None
    return current_candidate


class Candidate:
    atom_candidate: AtomCandidate
    occurrences: int

    def __init__(self, initial_cand: AtomCandidate) -> None:
        self.atom_candidate = initial_cand
        self.term = initial_cand.term
        self.occurrences = initial_cand.atom_occurrences

    def append_if_equal(self, new_cand: AtomCandidate) -> None:
        if new_cand.identical(self.atom_candidate):
            self.occurrences += new_cand.atom_occurrences

    def __repr__(self) -> str:
        return f"<Candidate occurrences={self.occurrences} atom_cand={self.atom_candidate}>"


def extract_candidates(s: set_of_states) -> list[Candidate]:
    new_candidates: list[Candidate] = []
    atomics_visited: list[AtomCandidate] = []
    for state in s:
        for atom in state:
            atom_cand = get_atom_candidate(atom)
            if [
                atom_cand.identical(a)
                for a in atomics_visited
                if atom_cand.identical(a)
            ]:
                for cand in new_candidates:
                    cand.append_if_equal(atom_cand)
            else:
                new_candidates.append(Candidate(atom_cand))
                atomics_visited.append(atom_cand)
    return new_candidates


def compare_candidate(candidate1: Candidate, candidate2: Candidate) -> Candidate:
    type_result = compare_type(candidate1.atom_candidate, candidate2.atom_candidate)
    if type_result is not None:
        if type_result.identical(candidate1.atom_candidate):
            return candidate1
        else:
            return candidate2
    elif candidate1.occurrences > candidate2.occurrences:
        ### QUANTITY ###
        # Lower priority than type (applies to objects of the same type)
        # Most wins
        return candidate1
    elif candidate2.occurrences > candidate1.occurrences:
        return candidate2
    else:
        if random.randint(0, 1) == 0:
            return candidate1
        else:
            return candidate2


def count_candidates(set_s: set_of_states, atom_candidate: AtomCandidate) -> int:
    instances_encountered = 0
    for s in set_s:
        for atom in s:
            if get_atom_candidate(atom).identical(atom_candidate):
                instances_encountered += 1
    return instances_encountered


def get_new_state(set_s: set_of_states, atom_candidate: AtomCandidate) -> set_of_states:
    count_candidates(set_s, atom_candidate)
    instance_num = random.randint(0, count_candidates(set_s, atom_candidate) - 1)
    instances_encountered = 0

    new_set_of_states = set()
    for s in set_s:
        new_states = set()
        for atom in s:
            current_atom_candidate = get_atom_candidate(atom)
            if current_atom_candidate.identical(atom_candidate):
                instances_encountered += 1
                if instance_num == instances_encountered - 1:
                    new_terms: list[Term | ArbitraryObject | Emphasis] = []
                    for i, term in enumerate(atom.terms):
                        if atom_candidate.term_idx == i:
                            assert not isinstance(term, Emphasis)
                            new_terms.append(Emphasis(term))
                        else:
                            new_terms.append(term)
                    new_atom = Atom(predicate=atom.predicate, terms=tuple(new_terms))
                else:
                    new_atom = atom
            else:
                new_atom = atom
            new_states.add(new_atom)
        new_set_of_states.add(state(new_states))
    return set_of_states(new_set_of_states)


def add_new_emphasis(
    stage: set_of_states, supposition: set_of_states
) -> tuple[set_of_states, set_of_states]:
    if not (supposition.is_verum or supposition.is_falsum):
        candidates = extract_candidates(supposition)
        final_candidate = reduce(compare_candidate, candidates)
        return stage, get_new_state(supposition, final_candidate.atom_candidate)
    elif not (stage.is_verum or stage.is_falsum):
        candidates = extract_candidates(stage)
        final_candidate = reduce(compare_candidate, candidates)
        return get_new_state(stage, final_candidate.atom_candidate), supposition
    else:
        return stage, supposition
