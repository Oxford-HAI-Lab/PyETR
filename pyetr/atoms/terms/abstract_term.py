from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .function import Function
from .multiset import Multiset


class AbstractTerm(ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @property
    @abstractmethod
    def detailed(self) -> str:
        ...


TermType = TypeVar("TermType", bound=AbstractTerm)


class AbstractArbitraryObject(AbstractTerm):
    name: str

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(type(self).__name__ + self.name)

    def __repr__(self) -> str:
        return f"{self.name}"

    @property
    def detailed(self) -> str:
        return f"<{type(self).__name__} name={self.name}>"


class AbstractFunctionalTerm(Generic[TermType], AbstractTerm):
    f: Function
    t: tuple[TermType, ...] | Multiset[TermType]

    def __init__(
        self,
        f: Function,
        t: Iterable[TermType],
    ):
        if f.arity is None:
            self.t = Multiset[TermType](t)
        else:
            self.t = tuple(t)
        if f.arity is not None and len(self.t) != f.arity:
            raise ValueError(
                f"{type(self).__name__} length {len(self.t)} did not match arity {f.arity}"
            )

        self.f = f

        out = f(self)
        if out is not None:
            self.f = out.f
            self.t = out.t

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.f, self.t))

    def __repr__(self) -> str:
        if self.f.arity == 0:
            return f"{self.f.name}"
        else:
            terms = ",".join([repr(i) for i in self.t])
            return f"{self.f.name}({terms})"

    @property
    def detailed(self) -> str:
        return f"<{type(self).__name__} f={self.f.detailed} t=({','.join(t.detailed for t in self.t)},)>"
