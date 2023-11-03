__all__ = ["ArbitraryObjectGenerator"]

import typing
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Iterable, TypeVar

if TYPE_CHECKING:
    from .view import View

from itertools import chain, combinations

from .atoms.terms import ArbitraryObject, Term


class NameScheme(Enum):
    """
    Enum to determine available naming schemes for arbitrary object
    generation.
    """

    alphabet = "alphabet"


class _BaseNameGen(metaclass=ABCMeta):
    """
    The template generator for arbitrary objects.
    """

    @abstractmethod
    def __init__(self, arb_objs: set[ArbitraryObject]) -> None:
        super().__init__()

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self) -> str:
        ...


class _AlphabetGenerator(_BaseNameGen):
    names: list[str]
    current_letter: str

    def __init__(self, arb_objs: set[ArbitraryObject]) -> None:
        """
        A Generator used to generate arbitrary objects based on the letters of the alphabet

        Args:
            arb_objs (set[ArbitraryObject]): The set of existing arbitrary objects to prevent
                name clashes.

        """
        self.names = [a.name for a in arb_objs]
        self.current_letter = ""

    @staticmethod
    def _get_next_letter(s: str):
        if not s.islower:
            raise ValueError("Input must be lowercase")
        if len(s) == 0:
            return "a"
        code = ord(s[-1])
        rest = s[0:-1]
        next_code = code + 1
        if next_code > ord("z"):
            return rest + "aa"
        else:
            return rest + chr(next_code)

    def __next__(self) -> str:
        candidate = self._get_next_letter(self.current_letter)
        while candidate in self.names:
            candidate = self._get_next_letter(candidate)
        self.current_letter = candidate
        return self.current_letter


class ArbitraryObjectGenerator:
    gen: _BaseNameGen

    def __init__(
        self,
        existing_arb_objs: set[ArbitraryObject],
        *,
        scheme: NameScheme = NameScheme.alphabet
    ) -> None:
        """
        A generator for arbitrary objects that based on the naming scheme provided, generates
        new arbitrary objects.

        Args:
            existing_arb_objs (set[ArbitraryObject]): The existing arbitrary objects, to exclude
                them from generation.
            scheme (NameScheme, optional): The naming scheme set for generation. Defaults to NameScheme.alphabet.
        """
        self.i = 0
        self.scheme = scheme
        if scheme == NameScheme.alphabet:
            self.gen = _AlphabetGenerator(existing_arb_objs)
        else:
            assert False

    def _get_arb_obj(self) -> ArbitraryObject:
        return ArbitraryObject(name=next(self.gen))

    def redraw(
        self, arb_objects: set[ArbitraryObject]
    ) -> dict[ArbitraryObject, ArbitraryObject]:
        """
        Redraw the arbitrary objects provided and produce a mapping for
            their replacements.

        Args:
            arb_objects (set[ArbitraryObject]): The arbitrary objects for replacement.

        Returns:
            dict[ArbitraryObject, ArbitraryObject]: The resultant mapping.
        """
        return {arb_obj: self._get_arb_obj() for arb_obj in arb_objects}

    def novelise(self, arb_objects: set[ArbitraryObject], view: "View") -> "View":
        """
        Redraw specified arbitrary objects within a view.

        Args:
            arb_objects (set[ArbitraryObject]): The arbitrary objects to replace.
            view (View): The current view

        Returns:
            View: The new view with arbirary objects replaced.
        """
        return view.replace(
            typing.cast(dict[ArbitraryObject, Term], self.redraw(arb_objects))
        )

    def novelise_all(self, view: "View") -> "View":
        """
        Redraw all arbitrary objects within a view.

        Args:
            view (View): The current view

        Returns:
            View: The new view with all arbirary objects replaced.
        """
        return self.novelise(view.stage_supp_arb_objects, view)


IterType = TypeVar("IterType")


def powerset(iterable: Iterable[IterType]) -> list[set[IterType]]:
    """
    Return the powerset of the given iterable

    Args:
        iterable (Iterable[IterType]): The input iterable

    Returns:
        list[set[IterType]: The powersets of the iterable.
    """
    s = list(iterable)
    return [
        set(i)
        for i in (chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))
    ]
