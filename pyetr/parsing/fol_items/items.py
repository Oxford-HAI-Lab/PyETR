__all__ = [
    "Variable",
    "LogicPredicate",
    "LogicReal",
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

from pyetr.parsing.common import Quantified, Variable, convert_float_to_dec


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

    def to_string(self, **kwargs: Any) -> str:
        return "~" + self.arg.to_string(**kwargs)

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return self.arg.to_english(name_mappings, **kwargs).replace(" is ", " is not ")


class LogicEmphasis(SingleOperand):
    """
    Used for parsing *
    """

    name = "LogicEmphasis"

    def to_string(self, **kwargs: Any) -> str:
        return self.arg.to_string(**kwargs) + "*"

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return self.arg.to_english(name_mappings, **kwargs) + " (at emphasis)"


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

    def _operand_string(self, operand: str, **kwargs: Any) -> str:
        inner = operand.join([o.to_string(**kwargs) for o in self.operands])
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

    def to_string(self, **kwargs: Any) -> str:
        return self._operand_string(" ∧ ", **kwargs)

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return " and ".join(
            [i.to_english(name_mappings, **kwargs) for i in self.operands]
        )


class BoolOr(MultiOperand):
    """
    Used for parsing disjunctions.
    """

    name = "BoolOr"

    def to_string(self, **kwargs: Any) -> str:
        return self._operand_string(" ∨ ", **kwargs)

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return "either " + ", or ".join(
            [i.to_english(name_mappings, **kwargs) for i in self.operands]
        )


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

    def to_string(self, **kwargs: Any) -> str:
        return self.left.to_string(**kwargs) + "→" + self.right.to_string(**kwargs)

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        left = self.left.to_english(name_mappings, **kwargs)
        right = self.right.to_english(name_mappings, **kwargs)
        return f"if {left}, then {right}"

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

    def to_string(self, **kwargs: Any) -> str:
        return "⊤"

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return "true"

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

    def to_string(self, **kwargs: Any) -> str:
        return "⊥"

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return "false"

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

    def to_string(self, **kwargs: Any) -> str:
        return (
            self.name
            + "("
            + ", ".join([a.to_string(**kwargs) for a in self.args])
            + ")"
        )

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        if self.name == "==":
            assert len(self.args) == 2
            return f"{self.args[0].to_english(name_mappings, **kwargs)} if and only if {self.args[1].to_english(name_mappings, **kwargs)}"
        else:
            if self.name in name_mappings:
                new_name = name_mappings[self.name]
            else:
                new_name = self.name
            if len(self.args) == 0:
                return new_name
            elif len(self.args) == 1:
                return (
                    f"{self.args[0].to_english(name_mappings, **kwargs)} is {new_name}"
                )
            elif len(self.args) == 2:
                return f"{self.args[0].to_english(name_mappings, **kwargs)} {self.name} {self.args[1].to_english(name_mappings, **kwargs)}"
            else:
                raise ValueError(
                    "Predicates of more than 3 args cannot be made into english"
                )

    @classmethod
    def from_pyparsing(cls, t: Any):
        if isinstance(t[0], str):
            name = t[0]
            args = t[1:]
        else:
            name = t[0][0]
            args = t[0][1:]
        return cls(name=name, args=args)


class LogicReal(LogicPredicate):
    def __init__(self, num: float) -> None:
        self.num = num
        super().__init__(name=str(num), args=[])

    def to_string(self, *, round_ints: bool = False, **kwargs: Any):
        return f"{convert_float_to_dec(self.num, round_ints)}"

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        return self.to_string()

    @classmethod
    def from_pyparsing(cls, t: Any):
        return cls(float("".join([str(i) for i in t])))


AtomicItem = Variable | LogicEmphasis | LogicPredicate | LogicReal

StatementItem = Quantified | BoolNot | BoolAnd | BoolOr | Implies | Truth | Falsum

Item = AtomicItem | StatementItem
