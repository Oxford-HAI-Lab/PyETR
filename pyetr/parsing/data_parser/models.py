import base64
import marshal
import types
from typing import Optional

from pydantic import BaseModel

from pyetr.atoms.terms.function import NumFunc

"""
This file contains a number of pydantic models that correspond to parts of a view
"""


class Predicate(BaseModel):
    name: str
    arity: int
    verifier: bool


class FuncCaller(BaseModel):
    code: str
    name: str

    @classmethod
    def from_func(cls, func: NumFunc):
        if not callable(func):
            raise ValueError("Input must be a callable function")
        return cls(
            code=base64.b64encode(marshal.dumps(func.__code__)).decode("utf-8"),
            name=func.__name__,
        )

    def to_func(self) -> NumFunc:
        code = marshal.loads(base64.b64decode(self.code.encode("utf-8")))
        return types.FunctionType(code, globals(), self.name)


class Function(BaseModel):
    name: str
    arity: Optional[int]
    func_caller: Optional[FuncCaller] = None


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
    polarity: bool


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
