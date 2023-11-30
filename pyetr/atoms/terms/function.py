__all__ = ["Function", "RealNumber"]


from typing import TYPE_CHECKING, Callable, Optional, cast

if TYPE_CHECKING:  # pragma: not covered
    from .abstract_term import AbstractFunctionalTerm, TermType

from inspect import getsource, signature

NumFunc = Callable[..., float]


def apply_func(
    term: "AbstractFunctionalTerm[TermType]", f: NumFunc
) -> "AbstractFunctionalTerm[TermType]":
    """
    Applies a numeric function to an abstract functional term, producing a new functional term.

    Args:
        term (AbstractFunctionalTerm[TermType]): The FunctionalTerm to apply the numeric function to.
        f (NumFunc): A function that takes a number of numeric arguments and returns a float

    Returns:
        AbstractFunctionalTerm[TermType]: The new FunctionalTerm
    """
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
    """
    The function to be used in a functional term
    """

    name: str
    arity: Optional[int]
    func_caller: Optional[NumFunc]

    def __init__(
        self,
        name: str,
        arity: Optional[int],
        func_caller: Optional[NumFunc] = None,
    ) -> None:
        """
        Create a function

        Args:
            name (str): The name of the function
            arity (Optional[int]): The arity of the function; how many arguments it receives.
            func_caller (Optional[NumFunc], optional): A numerical function to convert received numeric terms.
                If None is provided, no conversion will take place. Defaults to None.

        Raises:
            ValueError: Negative arity
        """
        if arity is not None and arity < 0:
            raise ValueError("arity must not be less than 0")
        self.name = name
        self.arity = arity
        self.func_caller = func_caller

    def __call__(
        self, func_term: "AbstractFunctionalTerm[TermType]"
    ) -> Optional["AbstractFunctionalTerm[TermType]"]:
        """
        Args:
            func_term (AbstractFunctionalTerm): The Functional Term to be converted

        Returns:
            Optional["AbstractFunctionalTerm"]: The converted functional term, or None
                if no conversion takes place.
        """
        if self.func_caller is None:
            return None
        return apply_func(func_term, self.func_caller)

    @classmethod
    def numeric(cls, func_caller: NumFunc) -> "Function":
        """
        Creates a function purely based on a python function.

        Args:
            func_caller (NumFunc): The python function.

        Returns:
            Function: The output function.
        """
        return cls(
            name=func_caller.__name__,
            arity=len(signature(func_caller).parameters),
            func_caller=func_caller,
        )

    def __repr__(self) -> str:
        return f"Function({self.name}, {self.arity})"

    @property
    def detailed(self) -> str:
        return repr(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Function):
            return False
        if self.func_caller is not None:
            func_caller1 = getsource(self.func_caller)
        else:
            func_caller1 = None

        if other.func_caller is not None:
            func_caller2 = getsource(other.func_caller)
        else:
            func_caller2 = None

        if self.name == other.name and not (self.arity == other.arity):
            raise ValueError(
                f"Equality on two functions of same name {self.name}, {other.name}, different arity {self.arity}, {other.arity}"
            )
        if (
            self.name == other.name
            and self.arity == other.arity
            and not (func_caller1 == func_caller2)
        ):
            raise ValueError(
                f"Equality on two functions of same name {self.name}, {other.name}, arity, but not func caller: {func_caller1}, {func_caller2}"
            )
        return (
            self.name == other.name
            and self.arity == other.arity
            and func_caller1 == func_caller2
        )

    def __hash__(self) -> int:
        if self.func_caller is not None:
            func_caller1 = getsource(self.func_caller)
        else:
            func_caller1 = None

        return hash(self.name) + hash(self.arity) + hash(func_caller1)


class RealNumber(Function):
    """
    A type of function used to express real numbers
    """

    def __init__(self, num: float) -> None:
        super().__init__(str(num), 0)

    @property
    def num(self) -> float:
        """
        Get the number associated with the RealNumber class

        Returns:
            float: The number
        """
        return float(self.name)

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.arity) + hash("num")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RealNumber):
            return False
        return self.name == other.name

    def __repr__(self) -> str:
        return f"RealNumber({self.name}, {self.arity})"
