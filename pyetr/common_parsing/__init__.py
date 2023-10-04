from copy import copy

from pyetr.atoms.open_predicate_atom import OpenPredicateAtom, get_open_atom_equivalent
from pyetr.atoms.predicate_atom import PredicateAtom
from pyetr.atoms.terms import ArbitraryObject, OpenTerm, Term, get_open_equivalent
from pyetr.dependency import DependencyRelation, dependencies_from_sets

Universal = ArbitraryObject
Existential = ArbitraryObject


class Variable:
    name: str

    def __init__(self, t) -> None:
        self.name = t[0]

    def __repr__(self) -> str:
        return f"<Variable name={self.name}>"

    def to_string(self) -> str:
        return self.name


class Quantified:
    variable: Variable
    quantifier: str

    def __init__(self, t) -> None:
        variables = t[0].variables
        assert len(variables) == 1
        quantifier = t[0].quantifier
        if quantifier == "A":
            self.quantifier = "∀"
        elif quantifier == "E":
            self.quantifier = "∃"
        else:
            self.quantifier = quantifier
        self.variable = variables[0]

    def __repr__(self) -> str:
        return f"<Quantified variable={self.variable} quantifier={self.quantifier}>"

    def to_string(self) -> str:
        return self.quantifier + self.variable.to_string()


def get_variable_map_and_dependencies(
    quantifieds: list[Quantified],
) -> tuple[dict[str, ArbitraryObject], DependencyRelation]:
    variable_map: dict[str, ArbitraryObject] = {}
    encountered_universals: list[tuple[Universal, set[Existential]]] = []
    existentials: set[Existential] = set()
    universals: set[Universal] = set()
    for quantified in quantifieds:
        if quantified.quantifier == "∃":
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            existentials.add(arb_obj)
            for _, exi_set in encountered_universals:
                exi_set.add(arb_obj)
        else:
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            universals.add(arb_obj)
            encountered_universals.append((arb_obj, set()))

        if quantified.variable.name not in variable_map:
            variable_map[quantified.variable.name] = arb_obj
        else:
            raise ValueError(
                f"Variable {quantified.variable.name} appears twice in quantifiers"
            )

    return variable_map, DependencyRelation(
        universals=universals,
        existentials=existentials,
        dependencies=dependencies_from_sets(encountered_universals),
    )


def merge_terms_with_opens(
    terms: list[Term], open_term_sets: list[list[tuple[Term, OpenTerm]]]
) -> list[tuple[Term, list[OpenTerm]]]:
    new_terms = [get_open_equivalent(t) for t in terms]
    new_terms_sets: list[tuple[Term, list[OpenTerm]]] = []
    for i, open_terms in enumerate(open_term_sets):
        if len(open_terms) > 0:
            for t, open_term in open_terms:
                fresh_terms = copy(new_terms)
                fresh_terms[i] = open_term
                new_terms_sets.append((t, fresh_terms))
    return new_terms_sets


def merge_atoms_with_opens(
    atoms: list[PredicateAtom],
    open_atom_sets: list[list[tuple[Term, OpenPredicateAtom]]],
) -> list[tuple[Term, list[OpenPredicateAtom]]]:
    new_atoms = [get_open_atom_equivalent(a) for a in atoms]
    new_atoms_sets: list[tuple[Term, list[OpenPredicateAtom]]] = []
    for i, open_atoms in enumerate(open_atom_sets):
        if len(open_atoms) > 0:
            for t, open_atom in open_atoms:
                fresh_atoms = copy(new_atoms)
                fresh_atoms[i] = open_atom
                new_atoms_sets.append((t, fresh_atoms))
    return new_atoms_sets
