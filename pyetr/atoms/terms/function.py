__all__ = ["Function", "RealNumber"]


from typing import TYPE_CHECKING, Callable, Optional, cast

from .multiset import Multiset

if TYPE_CHECKING:
    from .abstract_term import AbstractFunctionalTerm
    from .term import Term

NumFunc = Callable[..., float]


def apply_func(term: "AbstractFunctionalTerm", f: NumFunc) -> "AbstractFunctionalTerm":
    if all(
        [hasattr(i, "f") and isinstance(getattr(i, "f"), RealNumber) for i in term.t]
    ):
        sets_new = cast(list[RealNumber], [getattr(i, "f") for i in term.t])
        nums_to_add: list[float] = []
        for num in sets_new:
            nums_to_add.append(num.num)
        calculated_term = f(*nums_to_add)
        return type(term)(RealNumber(calculated_term), ())
    else:
        return term


class Function:
    name: str
    arity: Optional[int]
    _func_caller: Optional[NumFunc]

    def __init__(
        self,
        name: str,
        arity: Optional[int],
        func_caller: Optional[NumFunc] = None,
    ) -> None:
        if arity is not None and arity < 0:
            raise ValueError("arity must not be less than 0")
        self.name = name
        self.arity = arity
        self._func_caller = func_caller

    def __call__(
        self, func_term: "AbstractFunctionalTerm"
    ) -> Optional["AbstractFunctionalTerm"]:
        if self._func_caller is None:
            return None
        return apply_func(func_term, self._func_caller)

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

    def __repr__(self) -> str:
        return f"RealNumber({self.name}, {self.arity})"
