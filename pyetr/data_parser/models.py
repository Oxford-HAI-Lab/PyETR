from typing import Optional

from pydantic import BaseModel


class Predicate(BaseModel):
    name: str
    arity: int
    verifier: bool


class Function(BaseModel):
    name: str
    arity: Optional[int]


class RealNumber(BaseModel):
    num: float


class ArbitraryObject(BaseModel):
    name: str


class QuestionMark(BaseModel):
    pass


class FunctionalTerm(BaseModel):
    function: Function | RealNumber
    terms: "list[FunctionalTerm | ArbitraryObject | QuestionMark]"


class Atom(BaseModel):
    predicate: Predicate
    terms: list[FunctionalTerm | ArbitraryObject | QuestionMark]


class DoAtom(BaseModel):
    atoms: list[Atom]


class Weight(BaseModel):
    multiplicative: list[FunctionalTerm | ArbitraryObject | QuestionMark]
    additive: list[FunctionalTerm | ArbitraryObject | QuestionMark]


class WeightPair(BaseModel):
    state: list[Atom | DoAtom]
    weight: Weight


class Dependency(BaseModel):
    existential: ArbitraryObject
    universal: ArbitraryObject


class DependencyRelation(BaseModel):
    universals: list[ArbitraryObject]
    existentials: list[ArbitraryObject]
    dependencies: list[Dependency]


class View(BaseModel):
    stage: list[list[Atom | DoAtom]]
    supposition: list[list[Atom | DoAtom]]
    weights: list[WeightPair]
    issues: list[tuple[FunctionalTerm | ArbitraryObject | QuestionMark, Atom | DoAtom]]
    dependency_relation: DependencyRelation
