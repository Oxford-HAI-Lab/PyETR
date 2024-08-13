__all__ = ["Function", "RealNumber"]


from typing import TYPE_CHECKING, Callable, Optional, cast

if TYPE_CHECKING:  # pragma: not covered
    from .abstract_term import AbstractFunctionalTerm, TermType

from inspect import Parameter, signature

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
            arity (Optional[int]): The arity of the function; how many arguments it receives. If None, then the function
                applies to a multiset of terms.
            func_caller (Optional[NumFunc], optional): A numerical function to convert received numeric terms.
                If None is provided, no conversion will take place. Defaults to None.

        Raises:
            ValueError: Negative arity
        """
        if arity is not None and arity < 0:
            raise ValueError("arity must not be less than 0")

        # If func_caller is defined, check arity matches

        if func_caller is not None:
            params = list(signature(func_caller).parameters.values())
            if arity is None:
                # Multiset case
                if not (
                    len(params) == 1 and params[0].kind == Parameter.VAR_POSITIONAL
                ):
                    raise ValueError(
                        "Multiset case must accept only one argument, and it must be var positional (like *args)"
                    )
            else:
                if not (
                    (len(params) == arity)
                    and all(
                        p.kind
                        in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
                        for p in params
                    )
                ):
                    raise ValueError(
                        "Arity for function must match in tuple case, and all args must be positional"
                    )

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
    def numeric(
        cls, func_caller: NumFunc, name_override: Optional[str] = None
    ) -> "Function":
        """
        Creates a function purely based on a python function.

        Args:
            func_caller (NumFunc): The python function.

        Returns:
            Function: The output function.
        """
        if name_override is not None:
            name = name_override
        else:
            name = func_caller.__name__
        params = list(signature(func_caller).parameters.values())
        if len(params) == 1 and params[0].kind == Parameter.VAR_POSITIONAL:
            # Multiset case
            return cls(
                name=name,
                arity=None,
                func_caller=func_caller,
            )
        else:
            return cls(
                name=name,
                arity=len(params),
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
        return self.name == other.name and self.arity == other.arity

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.arity)


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
