__all__ = ["ArbitraryObjectGenerator"]

from enum import Enum

from pyetr.view import View

from .term import ArbitraryObject


class NameScheme(Enum):
    alphabet = "alphabet"


class ArbitraryObjectGenerator:
    def __init__(
        self, existing_arb_objs: set[ArbitraryObject], *, scheme=NameScheme.alphabet
    ) -> None:
        self.i = 0

        # Generate a letter excluding those provided

    def get_existential(self) -> ArbitraryObject:
        raise NotImplementedError

    def get_universal(self) -> ArbitraryObject:
        raise NotImplementedError

    def redraw(
        self, arb_objects: set[ArbitraryObject]
    ) -> dict[ArbitraryObject, ArbitraryObject]:
        # Draw new object with get uni and exi - create mapping
        raise NotImplementedError

    def novelise(self, arb_objects: set[ArbitraryObject], view: View) -> View:
        # Create new view with arb objects specified replaced
        raise NotImplementedError
