from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

from pyetr.function import Function
from pyetr.multiset import Multiset


class AbstractTerm(ABC):
    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


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

    @property
    def detailed(self) -> str:
        return f"<{type(self).__name__} name={self.name}>"

    def __repr__(self) -> str:
        return f"{self.name}"


TermType = TypeVar("TermType", bound=AbstractTerm)


class AbstractFunctionalTerm(Generic[TermType], AbstractTerm):
    f: Function
    t: Optional[tuple[TermType, ...]]

    def __init__(
        self,
        f: Function,
        t: Optional[tuple[TermType, ...]] = None,
    ):
        if t is None and f.arity > 0:
            raise ValueError(
                f"{type(self).__name__} not supplied when Function arity is greater than 0"
            )
        elif t is not None and (len(t) != f.arity):
            raise ValueError(
                f"{type(self).__name__} length {len(t)} did not match arity {f.arity}"
            )
        self.f = f
        self.t = t

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.f == other.f and self.t == other.t

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.f, self.t))

    @property
    def detailed(self) -> str:
        if self.t is None:
            return f"<{type(self).__name__} f={self.f.detailed} t=()>"
        return f"<{type(self).__name__} f={self.f.detailed} t=({','.join(t.detailed for t in self.t)},)>"

    def __repr__(self) -> str:
        if self.f.arity == 0:
            return f"{self.f.name}"
        else:
            assert self.t is not None
            terms = ",".join([repr(i) for i in self.t])
            return f"{self.f.name}({terms})"


class AbstractSummation(Generic[TermType], AbstractTerm):
    t: Multiset[TermType]

    def __init__(
        self,
        t: Iterable[TermType],
    ):
        self.t = Multiset[TermType](t)

    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def detailed(self) -> str:
        return f"<OpenSummation {self.t}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.t == other.t

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.t))
