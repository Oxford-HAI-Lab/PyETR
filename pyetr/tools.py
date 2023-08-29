__all__ = ["ArbitraryObjectGenerator"]

import typing
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .view import View

from .term import ArbitraryObject, Term


class NameScheme(Enum):
    alphabet = "alphabet"


class BaseNameGen(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, arb_objs: set[ArbitraryObject]) -> None:
        super().__init__()

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self) -> str:
        ...


class AlphabetGenerator(BaseNameGen):
    names: list[str]
    current_letter: str

    def __init__(self, arb_objs: set[ArbitraryObject]) -> None:
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
    gen: BaseNameGen

    def __init__(
        self, existing_arb_objs: set[ArbitraryObject], *, scheme=NameScheme.alphabet
    ) -> None:
        self.i = 0
        self.scheme = scheme
        if scheme == NameScheme.alphabet:
            self.gen = AlphabetGenerator(existing_arb_objs)
        else:
            assert False

    def get_arb_obj(self) -> ArbitraryObject:
        return ArbitraryObject(name=next(self.gen))

    def redraw(
        self, arb_objects: set[ArbitraryObject]
    ) -> dict[ArbitraryObject, ArbitraryObject]:
        draws: dict[ArbitraryObject, ArbitraryObject] = {}
        for arb_obj in arb_objects:
            draws[arb_obj] = self.get_arb_obj()
        return draws

    def novelise(self, arb_objects: set[ArbitraryObject], view: "View") -> "View":
        replacements = self.redraw(arb_objects)
        return view.replace(
            typing.cast(dict[ArbitraryObject, ArbitraryObject | Term], replacements)
        )

    def novelise_all(self, view: "View") -> "View":
        return self.novelise(view.stage_supp_arb_objects, view)
