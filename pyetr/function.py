__all__ = ["Function", "RealNumber"]


from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from pyetr.abstract_term import AbstractFunctionalTerm


class Function:
    name: str
    arity: int
    _func_caller: Optional[
        Callable[["AbstractFunctionalTerm"], Optional["AbstractFunctionalTerm"]]
    ]

    def __init__(
        self,
        name: str,
        arity: int,
        func_caller: Optional[
            Callable[["AbstractFunctionalTerm"], Optional["AbstractFunctionalTerm"]]
        ] = None,
    ) -> None:
        if arity < 0:
            raise ValueError("arity must not be less than 0")
        self.name = name
        self.arity = arity
        self._func_caller = func_caller

    def __call__(
        self, func_term: "AbstractFunctionalTerm"
    ) -> Optional["AbstractFunctionalTerm"]:
        if self._func_caller is None:
            return None
        return self._func_caller(func_term)

    def __repr__(self) -> str:
        return f"Function({self.name}, {self.arity})"

    @property
    def detailed(self) -> str:
        return repr(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Function):
            return False
        if self.name == other.name and not (self.arity == other.arity):
            raise ValueError(
                f"Equality on two functions of same name {self.name}, {other.name}, different arity {self.arity}, {other.arity}"
            )
        return self.name == other.name and self.arity == other.arity

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.arity)


class RealNumber(Function):
    def __init__(self, num: float) -> None:
        super().__init__(str(num), 0)

    @property
    def num(self) -> float:
        return float(self.name)

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.arity) + hash("num")

    def __eq__(self, other) -> bool:
        if not isinstance(other, RealNumber):
            return False
        return self.name == other.name
