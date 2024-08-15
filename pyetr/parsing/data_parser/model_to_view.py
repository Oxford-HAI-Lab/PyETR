from typing import cast, overload

import pyetr.parsing.data_parser.models as models
from pyetr.atoms.abstract import Atom
from pyetr.atoms.doatom import DoAtom
from pyetr.atoms.open_predicate_atom import OpenPredicateAtom
from pyetr.atoms.predicate import Predicate
from pyetr.atoms.predicate_atom import PredicateAtom
from pyetr.atoms.terms.function import Function, RealNumber
from pyetr.atoms.terms.multiset import Multiset
from pyetr.atoms.terms.open_term import (
    OpenArbitraryObject,
    OpenFunctionalTerm,
    QuestionMark,
)
from pyetr.atoms.terms.term import ArbitraryObject, FunctionalTerm, Term
from pyetr.dependency import Dependency, DependencyRelation
from pyetr.issues import IssueStructure
from pyetr.parsing.view_storage import ViewStorage
from pyetr.stateset import SetOfStates, State
from pyetr.weight import Weight, Weights


def model_to_function(f: models.Function | models.RealNumber) -> Function:
    if isinstance(f, models.RealNumber):
        return RealNumber(num=f.num)
    else:
        if f.func_caller is None:
            new_func_caller = None
        else:
            new_func_caller = f.func_caller.to_func()
        return Function(name=f.name, arity=f.arity, func_caller=new_func_caller)


@overload
def model_to_term(t: models.FunctionalTerm) -> FunctionalTerm:
    ...


@overload
def model_to_term(t: models.ArbitraryObject) -> ArbitraryObject:
    ...


@overload
def model_to_term(
    t: models.ArbitraryObject | models.FunctionalTerm,
) -> FunctionalTerm | ArbitraryObject:
    ...


def model_to_term(
    t: models.ArbitraryObject | models.FunctionalTerm,
) -> FunctionalTerm | ArbitraryObject:
    if isinstance(t, models.ArbitraryObject):
        return ArbitraryObject(name=t.name)
    else:
        return FunctionalTerm(
            f=model_to_function(t.function),
            t=[
                model_to_term(cast(models.ArbitraryObject | models.FunctionalTerm, i))
                for i in t.terms
            ],
        )


@overload
def model_to_open_term(t: models.FunctionalTerm) -> OpenFunctionalTerm:
    ...


@overload
def model_to_open_term(t: models.ArbitraryObject) -> OpenArbitraryObject:
    ...


@overload
def model_to_open_term(t: models.QuestionMark) -> QuestionMark:
    ...


@overload
def model_to_open_term(
    t: models.ArbitraryObject | models.FunctionalTerm | models.QuestionMark,
) -> OpenFunctionalTerm | OpenArbitraryObject | QuestionMark:
    ...


def model_to_open_term(
    t: models.ArbitraryObject | models.FunctionalTerm | models.QuestionMark,
) -> OpenFunctionalTerm | OpenArbitraryObject | QuestionMark:
    if isinstance(t, models.ArbitraryObject):
        return OpenArbitraryObject(name=t.name)

    elif isinstance(t, models.FunctionalTerm):
        return OpenFunctionalTerm(
            f=model_to_function(t.function), t=[model_to_open_term(i) for i in t.terms]
        )
    else:
        return QuestionMark()


@overload
def model_to_open_atom(a: models.DoAtom) -> list[OpenPredicateAtom]:
    ...


@overload
def model_to_open_atom(a: models.Atom) -> OpenPredicateAtom:
    ...


@overload
def model_to_open_atom(
    a: models.Atom | models.DoAtom,
) -> OpenPredicateAtom | list[OpenPredicateAtom]:
    ...


def model_to_open_atom(
    a: models.Atom | models.DoAtom,
) -> OpenPredicateAtom | list[OpenPredicateAtom]:
    """
    Converts a pydantic form atom to view openatom
    Args:
        a (models.Atom | models.DoAtom): Pydantic model atom

    Returns:
        OpenAtom: View OpenAtom
    """
    if isinstance(a, models.Atom):
        return OpenPredicateAtom(
            predicate=Predicate(
                name=a.predicate.name,
                arity=a.predicate.arity,
                _verifier=a.predicate.verifier,
            ),
            terms=tuple([model_to_open_term(t) for t in a.terms]),
        )
    else:
        final_atoms: list[OpenPredicateAtom] = []
        for atom in a.atoms:
            new_atom = model_to_open_atom(atom)
            if new_atom.question_count != 0:
                final_atoms.append(new_atom)
        return final_atoms


@overload
def model_to_atom(a: models.DoAtom) -> DoAtom:
    ...


@overload
def model_to_atom(a: models.Atom) -> PredicateAtom:
    ...


@overload
def model_to_atom(a: models.Atom | models.DoAtom) -> Atom:
    ...


def model_to_atom(a: models.Atom | models.DoAtom) -> Atom:
    """
    Converts a pydantic form atom to view atom

    Args:
        a (models.Atom | models.DoAtom): Pydantic model atom

    Returns:
        Atom: View atom
    """
    if isinstance(a, models.Atom):
        return PredicateAtom(
            predicate=Predicate(
                name=a.predicate.name,
                arity=a.predicate.arity,
                _verifier=a.predicate.verifier,
            ),
            terms=tuple(
                [
                    model_to_term(
                        cast(models.FunctionalTerm | models.ArbitraryObject, t)
                    )
                    for t in a.terms
                ]
            ),
        )
    else:
        return DoAtom([model_to_atom(atom) for atom in a.atoms], polarity=a.polarity)


def model_to_state(s: list[models.Atom | models.DoAtom]) -> State:
    return State([model_to_atom(atom) for atom in s])


def model_to_weight(w: models.Weight) -> Weight:
    """
    Converts from the pydantic weight model to the view form.

    Args:
        w (models.Weight): The pydantic weights model

    Returns:
        Weight: The weight in view form
    """
    multi = Multiset[Term](
        [
            model_to_term(cast(models.FunctionalTerm | models.ArbitraryObject, t))
            for t in w.multiplicative
        ]
    )
    additive = Multiset[Term](
        [
            model_to_term(cast(models.FunctionalTerm | models.ArbitraryObject, t))
            for t in w.additive
        ]
    )
    return Weight(multiplicative=multi, additive=additive)


def model_to_view(v: models.View) -> ViewStorage:
    """
    Converts pydantic model View to View

    Args:
        v (models.View): Pydantic model of views

    Returns:
        ViewStorage: The output view object
    """
    issues_list: list[tuple[Term, OpenPredicateAtom]] = []
    for t, a in v.issues:
        new_term = model_to_term(
            cast(models.ArbitraryObject | models.FunctionalTerm, t)
        )
        new_atoms = model_to_open_atom(a)
        if isinstance(new_atoms, list):
            for open_atom in new_atoms:
                issues_list.append((new_term, open_atom))
        else:
            issues_list.append((new_term, new_atoms))
    issues = IssueStructure(issues_list)
    return ViewStorage(
        stage=SetOfStates([model_to_state(state) for state in v.stage]),
        supposition=SetOfStates([model_to_state(state) for state in v.supposition]),
        weights=Weights(
            {
                model_to_state(weight_pair.state): model_to_weight(weight_pair.weight)
                for weight_pair in v.weights
            }
        ),
        issue_structure=issues,
        dependency_relation=DependencyRelation(
            universals={model_to_term(a) for a in v.dependency_relation.universals},
            existentials={model_to_term(a) for a in v.dependency_relation.existentials},
            dependencies=frozenset(
                [
                    Dependency(
                        existential=model_to_term(dep.existential),
                        universal=model_to_term(dep.universal),
                    )
                    for dep in v.dependency_relation.dependencies
                ]
            ),
        ),
    )
