from __future__ import annotations

import typing
from typing import cast, overload

import pyetr.parsing.data_parser.models as models
from pyetr.atoms.abstract import AbstractAtom
from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_predicate_atom import OpenPredicateAtom
from pyetr.atoms.predicate_atom import PredicateAtom
from pyetr.atoms.terms.abstract_term import (
    AbstractArbitraryObject,
    AbstractFunctionalTerm,
    AbstractTerm,
    TermType,
)
from pyetr.atoms.terms.function import RealNumber
from pyetr.atoms.terms.open_term import QuestionMark
from pyetr.dependency import DependencyRelation

if typing.TYPE_CHECKING:
    from pyetr.view import View


@overload
def term_to_model(t: AbstractFunctionalTerm[TermType]) -> models.FunctionalTerm:
    ...


@overload
def term_to_model(t: AbstractArbitraryObject) -> models.ArbitraryObject:
    ...


@overload
def term_to_model(t: QuestionMark) -> models.QuestionMark:
    ...


@overload
def term_to_model(
    t: AbstractTerm,
) -> models.ArbitraryObject | models.FunctionalTerm | models.QuestionMark:
    ...


def term_to_model(
    t: AbstractTerm,
) -> models.ArbitraryObject | models.FunctionalTerm | models.QuestionMark:
    """
    Converts a term to pydantic model form

    Args:
        t (AbstractTerm): The term

    Returns:
        models.ArbitraryObject | models.FunctionalTerm | models.QuestionMark: The pydantic model
            form of the term.
    """
    if isinstance(t, AbstractFunctionalTerm):
        if isinstance(t.f, RealNumber):
            new_f = models.RealNumber(num=t.f.num)
        else:
            if t.f.func_caller is None:
                new_func = None
            else:
                new_func = models.FuncCaller.from_func(t.f.func_caller)
            new_f = models.Function(
                name=t.f.name, arity=t.f.arity, func_caller=new_func
            )
        return models.FunctionalTerm(
            function=new_f,
            terms=[
                term_to_model(term)
                for term in cast(AbstractFunctionalTerm[AbstractTerm], t).t
            ],
        )
    elif isinstance(t, AbstractArbitraryObject):
        return models.ArbitraryObject(name=t.name)
    elif isinstance(t, QuestionMark):
        return models.QuestionMark()
    else:
        assert False


def atom_to_model(a: AbstractAtom) -> models.Atom | models.DoAtom:
    """
    Converts an atom to pydantic model form

    Args:
        a (AbstractAtom): An atom or open atom

    Returns:
        models.Atom | models.DoAtom: The pydantic model form of the atom.
    """
    if isinstance(a, (PredicateAtom, OpenPredicateAtom)):
        return models.Atom(
            predicate=models.Predicate(
                name=a.predicate.name,
                arity=a.predicate.arity,
                verifier=a.predicate.verifier,
            ),
            terms=[term_to_model(term) for term in a.terms],
        )
    elif isinstance(a, DoAtom):
        return models.DoAtom(
            atoms=cast(list[models.Atom], [atom_to_model(atom) for atom in a.atoms]),
            polarity=a.polarity,
        )
    else:
        assert False


def dependency_rel_to_model(dep_rel: DependencyRelation) -> models.DependencyRelation:
    """
    Converts a dependency relation to pydantic model form.

    Args:
        dep_rel (DependencyRelation): The dependency relation.

    Returns:
        models.DependencyRelation: The pydantic model form of the dependency relation.
    """
    universals = [term_to_model(i) for i in dep_rel.universals]
    existentials = [term_to_model(i) for i in dep_rel.existentials]
    dependencies = [
        models.Dependency(
            existential=term_to_model(i.existential),
            universal=term_to_model(i.universal),
        )
        for i in dep_rel.dependencies
    ]
    return models.DependencyRelation(
        universals=universals, existentials=existentials, dependencies=dependencies
    )


def view_to_model(v: View) -> models.View:
    """
    Converts a View to pydantic model form

    Args:
        v (View): View

    Returns:
        models.View: Pydantic model view
    """
    return models.View(
        stage=[[atom_to_model(atom) for atom in state] for state in v.stage],
        supposition=[
            [atom_to_model(atom) for atom in state] for state in v.supposition
        ],
        weights=[
            models.WeightPair(
                state=[atom_to_model(atom) for atom in s],
                weight=models.Weight(
                    multiplicative=[term_to_model(i) for i in w.multiplicative],
                    additive=[term_to_model(i) for i in w.additive],
                ),
            )
            for s, w in v.weights.items()
        ],
        issues=[
            (term_to_model(term), atom_to_model(atom))
            for term, atom in v.issue_structure
        ],
        dependency_relation=dependency_rel_to_model(v.dependency_relation),
    )
