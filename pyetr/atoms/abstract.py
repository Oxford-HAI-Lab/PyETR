from abc import abstractmethod
from typing import Self

from .terms import ArbitraryObject, Term


class AbstractAtom:
    @property
    @abstractmethod
    def detailed(self) -> str:
        ...


class AbstractOpen(AbstractAtom):
    pass


class AbstractComplete(AbstractAtom):
    @property
    @abstractmethod
    def arb_objects(self) -> set[ArbitraryObject]:
        ...

    @abstractmethod
    def __invert__(self) -> Self:
        ...

    @abstractmethod
    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> Self:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        ...
