from abc import ABC, abstractmethod
from typing import Self

from .terms import ArbitraryObject, Term


class AbstractAtom(ABC):
    """
    The abstract base class of all atoms and open atoms.
    """

    @property
    @abstractmethod
    def detailed(self) -> str:
        ...

    @abstractmethod
    def replace(self, replacements: dict[ArbitraryObject, Term]) -> Self:
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


class OpenAtom(AbstractAtom):
    """
    The abstract base class of all open atoms.
    """

    @abstractmethod
    def __call__(self, term: Term) -> "Atom":
        """
        Replaces the term given in place of the question mark in the
        open atom. This produces a regular Atom.

        Args:
            term (Term): The term to be replaced.

        Returns:
            Atom: The Atom with the question mark replaced
        """
        ...

    @abstractmethod
    def question_count(self) -> int:
        """
        Counts the question marks present in the open atom

        Returns:
            int: The number of Question Marks.
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
