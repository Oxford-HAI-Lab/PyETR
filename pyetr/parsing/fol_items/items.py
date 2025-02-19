__all__ = [
    "Variable",
    "LogicPredicate",
    "LogicEmphasis",
    "Quantified",
    "BoolNot",
    "BoolAnd",
    "BoolOr",
    "Implies",
    "Truth",
    "Falsum",
    "Item",
]

from typing import Any, ClassVar, Optional

from pyetr.parsing.common import Quantified, Variable


class SingleOperand:
    """
    Base class used for single operand parser operations
    """

    name: ClassVar[str]
    arg: "Item"

    def __init__(self, t: Any) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<{self.name} arg={self.arg}>"


class BoolNot(SingleOperand):
    """
    Used for parsing "not" or ~
    """

    name = "BoolNot"

    def to_string(self) -> str:
        return "~" + self.arg.to_string()


class LogicEmphasis(SingleOperand):
    """
    Used for parsing *
    """

    name = "LogicEmphasis"

    def to_string(self) -> str:
        return self.arg.to_string() + "*"


class MultiOperand:
    """
    Base class used for multi operand parser operations
    """

    name: ClassVar[str]
    operands: list["Item"]

    def __init__(self, t) -> None:
        assert len(t) == 1
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<{self.name} operands={self.operands}>"

    def _operand_string(self, operand: str) -> str:
        inner = operand.join([o.to_string() for o in self.operands])
        return "(" + inner + ")"


class BoolAnd(MultiOperand):
    """
    Used for parsing conjunctions.
    """

    name = "BoolAnd"

    def to_string(self) -> str:
        return self._operand_string(" ∧ ")


class BoolOr(MultiOperand):
    """
    Used for parsing disjunctions.
    """

    name = "BoolOr"

    def to_string(self) -> str:
        return self._operand_string(" ∨ ")


class Implies:
    """
    Used for parsing a → b
    """

    left: "Item"
    right: "Item"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 2
        self.left = t[0][0]
        self.right = t[0][1]

    def __repr__(self) -> str:
        return f"<Implies left={self.left} right={self.right}>"

    def to_string(self) -> str:
        return self.left.to_string() + "→" + self.right.to_string()


class Truth:
    """
    Used for parsing ⊤
    """

    def __init__(self, t: Optional[Any] = None) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Truth>"

    def to_string(self) -> str:
        return "⊤"


class Falsum:
    """
    Used for parsing ⊥
    """

    def __init__(self, t) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Falsum>"

    def to_string(self) -> str:
        return "⊥"


class LogicPredicate:
    """
    The parser logic predicate.
    """

    args: list["Item"]
    name: str

    def __init__(self, t: Any) -> None:
        if isinstance(t[0], str):
            self.name = t[0]
            self.args = t[1:]
        else:
            self.name = t[0][0]
            self.args = t[0][1:]

    def __repr__(self) -> str:
        return f"<LogicPredicate args={self.args} name={self.name}>"

    def to_string(self) -> str:
        return self.name + "(" + ", ".join([a.to_string() for a in self.args]) + ")"


AtomicItem = Variable | LogicEmphasis | LogicPredicate

StatementItem = Quantified | BoolNot | BoolAnd | BoolOr | Implies | Truth | Falsum

Item = AtomicItem | StatementItem
