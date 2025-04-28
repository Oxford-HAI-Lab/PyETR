from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from .terms import ArbitraryObject, Term

if TYPE_CHECKING:  # pragma: not covered
    from pyetr.types import MatchCallback, MatchItem


class AbstractAtom(ABC):
    """
    The abstract base class of all atoms and open atoms.
    """

    @property
    @abstractmethod
    def detailed(self) -> str: ...

    @abstractmethod
    def _replace_arbs(self, replacements: dict[ArbitraryObject, Term]) -> Self:
        """
        Replaces one arbitrary object found in the atom with another term from a mapping.

        Args:
            replacements (dict[ArbitraryObject, Term]): Mapping of replacements.

        Returns:
            Self: The atom with replacements made.
        """
        ...

    @abstractmethod
    def __invert__(self) -> Self:
        """
        Inverts and produces a new atom
        """
        ...


class Atom(AbstractAtom):
    """
    The abstract base class of all atoms (not opens).
    """

    @property
    @abstractmethod
    def arb_objects(self) -> set[ArbitraryObject]:
        """
        Gets the arbitrary objects found in the atom.

        Returns:
            set[ArbitraryObject]: The arbitrary objects in the atom.
        """
        ...

    @abstractmethod
    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> Self:
        """
        Replaces a single term with a another single term.

        Args:
            old_term (Term): The term to be replaced
            new_term (Term): The new term

        Returns:
            Self: The new instance of the atom
        """
        ...

    @abstractmethod
    def match(
        self,
        old_item: "MatchItem",
        callback: "MatchCallback",
    ) -> Self: ...
