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

from typing import Any, ClassVar, Sequence

from pyetr.parsing.common import Quantified, Variable


class SingleOperand:
    """
    Base class used for single operand parser operations
    """

    name: ClassVar[str]
    arg: "Item"

    def __init__(self, arg: "Item") -> None:
        self.arg = arg

    def __repr__(self) -> str:
        return f"<{self.name} arg={self.arg}>"

    @classmethod
    def from_pyparsing(cls, t: Any):
        assert len(t) == 1
        assert len(t[0]) == 1
        return cls(t[0][0])


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
    operands: Sequence["Item"]

    def __init__(self, items: Sequence["Item"]) -> None:
        self.operands = items

    def __repr__(self) -> str:
        return f"<{self.name} operands={self.operands}>"

    def _operand_string(self, operand: str) -> str:
        inner = operand.join([o.to_string() for o in self.operands])
        return "(" + inner + ")"

    @classmethod
    def from_pyparsing(cls, t: Any):
        assert len(t) == 1
        return cls(items=t[0])


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

    def __init__(self, left: "Item", right: "Item") -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<Implies left={self.left} right={self.right}>"

    def to_string(self) -> str:
        return self.left.to_string() + "→" + self.right.to_string()

    @classmethod
    def from_pyparsing(cls, t: Any):
        assert len(t) == 1
        assert len(t[0]) == 2
        left = t[0][0]
        right = t[0][1]
        return cls(left=left, right=right)


class Truth:
    """
    Used for parsing ⊤
    """

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Truth>"

    def to_string(self) -> str:
        return "⊤"

    @classmethod
    def from_pyparsing(cls, t: Any):
        return cls()


class Falsum:
    """
    Used for parsing ⊥
    """

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Falsum>"

    def to_string(self) -> str:
        return "⊥"

    @classmethod
    def from_pyparsing(cls, t: Any):
        return cls()


class LogicPredicate:
    """
    The parser logic predicate.
    """

    args: Sequence["Item"]
    name: str

    def __init__(self, name: str, args: Sequence["Item"]) -> None:
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        return f"<LogicPredicate args={self.args} name={self.name}>"

    def to_string(self) -> str:
        return self.name + "(" + ", ".join([a.to_string() for a in self.args]) + ")"

    @classmethod
    def from_pyparsing(cls, t: Any):
        if isinstance(t[0], str):
            name = t[0]
            args = t[1:]
        else:
            name = t[0][0]
            args = t[0][1:]
        return cls(name=name, args=args)


AtomicItem = Variable | LogicEmphasis | LogicPredicate

StatementItem = Quantified | BoolNot | BoolAnd | BoolOr | Implies | Truth | Falsum

Item = AtomicItem | StatementItem
