__all__ = ["ArbitraryObjectGenerator"]

from .term import ArbitraryObject


class ArbitraryObjectGenerator:
    def __init__(self, is_existential: bool) -> None:
        self.i = 0
        self.is_existential = is_existential

    def __next__(self):
        self.i += 1
        if self.is_existential:
            name_prefix = "x"
        else:
            name_prefix = "y"
        return ArbitraryObject(
            name=f"{name_prefix}{self.i}", is_existential=self.is_existential
        )

    def __iter__(self):
        return self
