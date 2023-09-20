from abc import ABC, abstractmethod
from typing import Self

from .terms import ArbitraryObject, Term


class AbstractAtom(ABC):
    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        ...

    @abstractmethod
    def __invert__(self) -> Self:
        ...


class AbstractOpen(AbstractAtom):
    @abstractmethod
    def __call__(self, term: Term) -> "AbstractComplete":
        ...


class AbstractComplete(AbstractAtom):
    @property
    @abstractmethod
    def arb_objects(self) -> set[ArbitraryObject]:
        ...

    @abstractmethod
    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> Self:
        ...
