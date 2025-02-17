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
    "parse_string",
]

from functools import cache
from typing import Any, ClassVar, Optional

import pyparsing as pp
from pyparsing import ParseException, ParserElement

from pyetr.parsing.common import ParsingError, Quantified, Variable

ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT
pp_right = pp.opAssoc.RIGHT


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


@cache
def get_expr() -> pp.Forward:
    """
    Generates the parsing expression

    Returns:
        Forward: the parsing expression
    """
    expr = pp.Forward()
    variable = (
        pp.Word(pp.alphas + "_", pp.alphanums + "_")
        .setResultsName("variables", listAllMatches=True)
        .setParseAction(Variable)
    )

    quantifier = pp.oneOf(
        "∃ ∀",
    ).setResultsName("quantifier")
    quantified_expr = pp.Group(quantifier + variable).setParseAction(Quantified)
    bool_not = pp.Suppress(pp.Char("~"))
    bool_or = pp.Suppress(pp.oneOf("∨ |"))
    bool_and = pp.Suppress(pp.oneOf("∧ &"))
    implies = pp.Suppress(pp.Char("→"))
    emphasis = pp.Suppress(pp.Char("*"))

    term = pp.Forward()

    predicate_word = pp.Word(pp.alphas + "_", pp.alphanums + "_").setResultsName(
        "predicate"
    ) | pp.Literal("==")
    predicate = (
        predicate_word
        + pp.Suppress("(")
        + pp.Optional(pp.delimitedList(term))
        + pp.Suppress(")")
    ).setParseAction(LogicPredicate)

    truth = pp.Char("⊤").setParseAction(Truth)
    falsum = pp.Char("⊥").setParseAction(Falsum)
    nested_and = pp.infix_notation(
        predicate | variable | truth | falsum,
        op_list=[
            (predicate_word, 1, pp_right, LogicPredicate),
            (emphasis, 1, pp_left, LogicEmphasis),
            (bool_not, 1, pp_right, BoolNot),
            (bool_and, 2, pp_left, BoolAnd),
            (bool_or, 2, pp_left, BoolOr),
            (implies, 2, pp_left, Implies),
        ],
        lpar=pp.Suppress("("),
        rpar=pp.Suppress(")"),
    )
    term <<= nested_and
    expr <<= pp.ZeroOrMore(quantified_expr) + nested_and
    return expr


AtomicItem = Variable | LogicEmphasis | LogicPredicate

StatementItem = Quantified | BoolNot | BoolAnd | BoolOr | Implies | Truth | Falsum

Item = AtomicItem | StatementItem


def parse_string(input_string: str) -> list[Item]:
    """
    Parses the input_string to a list of parsed items.

    Args:
        input_string (str): The input string

    Raises:
        ParsingError: Failed to parse

    Returns:
        list[Item]: The output list of items
    """
    expr = get_expr()
    try:
        new_string: list[Item] = expr.parse_string(
            input_string, parseAll=True
        ).as_list()
    except ParseException as e:
        raise ParsingError(e.msg)
    return new_string
