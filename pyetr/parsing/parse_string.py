__all__ = [
    "Variable",
    "LogicFunction",
    "LogicPredicate",
    "LogicEmphasis",
    "Constant",
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
from pyparsing import ParserElement

ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore


class Variable:
    name: str

    def __init__(self, t) -> None:
        self.name = t[0]

    def __repr__(self) -> str:
        return f"<Variable name={self.name}>"

    def to_string(self) -> str:
        return self.name


class Constant:
    name: str

    def __init__(self, t) -> None:
        self.name = t[0][0]

    def __repr__(self) -> str:
        return f"<Constant name={self.name}>"

    def to_string(self) -> str:
        return self.name + "()"


class Quantified:
    variable: Variable
    quantifier: str

    def __init__(self, t) -> None:
        variables = t[0].variables.as_list()
        assert len(variables) == 1
        self.variable = variables[0]
        self.quantifier = t[0].quantifier

    def __repr__(self) -> str:
        return f"<Quantified variable={self.variable} quantifier={self.quantifier}>"

    def to_string(self) -> str:
        return self.quantifier + self.variable.to_string()


class SingleOperand:
    name: ClassVar[str]
    arg: "Item"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<{self.name} arg={self.arg}>"


class BoolNot(SingleOperand):
    name = "BoolNot"

    def to_string(self):
        return "~" + self.arg.to_string()


class LogicEmphasis(SingleOperand):
    name = "LogicEmphasis"

    def to_string(self):
        return "*" + self.arg.to_string()


class MultiOperand:
    name: ClassVar[str]
    operands: list["Item"]

    def __init__(self, t) -> None:
        assert len(t) == 1
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<{self.name} operands={self.operands}>"

    def _operand_string(self, operand: str, with_brackets: bool) -> str:
        inner = operand.join([o.to_string() for o in self.operands])
        if with_brackets:
            return "(" + inner + ")"
        else:
            return inner


class BoolAnd(MultiOperand):
    name = "BoolAnd"

    def to_string(self) -> str:
        return self._operand_string(" ∧ ", with_brackets=True)


class BoolOr(MultiOperand):
    name = "BoolOr"

    def to_string(self) -> str:
        return self._operand_string(" ∨ ", with_brackets=True)


class Comma(MultiOperand):
    name = "Comma"

    def to_string(self) -> str:
        return self._operand_string(",", with_brackets=False)


class Implies:
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
        return self.left.to_string() + "->" + self.right.to_string()


def equals(t):
    assert len(t[0]) == 2
    return LogicPredicate([["=", t[0]]])


class Truth:
    def __init__(self, t: Optional[Any] = None) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Truth>"

    def to_string(self) -> str:
        return "⊤"


class Falsum:
    def __init__(self, t) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Falsum>"

    def to_string(self) -> str:
        return "⊥"


class LogicPredicate:
    args: list["Item"]
    name: str

    def __init__(self, t) -> None:
        self.name = t[0][0]
        if len(t[0]) > 1:
            other = t[0][1]
            if isinstance(other, Comma):
                self.args = t[0][1].operands
            else:
                self.args = [t[0][1]]
        else:
            self.args = []

    def __repr__(self) -> str:
        return f"<LogicPredicate args={self.args} name={self.name}>"

    def to_string(self) -> str:
        return self.name + "(" + ", ".join([a.to_string() for a in self.args]) + ")"


class LogicFunction:
    args: list["Item"]
    name: str

    def __init__(self, t) -> None:
        self.name = t[0][1]
        if len(t[0]) > 2:
            other = t[0][2]
            if isinstance(other, Comma):
                self.args = t[0][2].operands
            else:
                self.args = [t[0][2]]
        else:
            self.args = []

    def __repr__(self) -> str:
        return f"<LogicFunction args={self.args} name={self.name}>"

    def to_string(self) -> str:
        return (
            "f_" + self.name + "(" + ",".join([a.to_string() for a in self.args]) + ")"
        )


@cache
def get_expr():
    expr = pp.Forward()
    variable = (
        pp.Word(pp.alphas, pp.alphanums)
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
    equals = pp.Suppress(pp.Char("="))
    emphasis = pp.Suppress(pp.Char("*"))

    predicate_word = pp.Word(pp.alphas, pp.alphanums).setResultsName("predicate")
    function_word = pp.Literal("f_") + predicate_word
    predicate_0 = pp.Group(predicate_word + pp.Suppress("()")).setParseAction(Constant)

    truth = pp.Char("⊤").setParseAction(Truth)
    falsum = pp.Char("⊥").setParseAction(Falsum)
    comma = pp.Suppress(",")
    nested_and = pp.infixNotation(
        predicate_0 | variable | truth | falsum,
        [
            (function_word, 1, pp_right, LogicFunction),
            (predicate_word, 1, pp_right, LogicPredicate),
            (emphasis, 1, pp_right, LogicEmphasis),
            (bool_not, 1, pp_right, BoolNot),
            (bool_and, 2, pp_left, BoolAnd),
            (bool_or, 2, pp_left, BoolOr),
            (equals, 2, pp_left, equals),
            (implies, 2, pp_left, Implies),
            (comma, 2, pp_left, Comma),
        ],
        lpar=pp.Suppress("("),
        rpar=pp.Suppress(")"),
    )
    expr <<= pp.ZeroOrMore(quantified_expr) + nested_and
    return expr


Item = (
    Variable
    | LogicFunction
    | LogicPredicate
    | LogicEmphasis
    | Constant
    | Quantified
    | BoolNot
    | BoolAnd
    | BoolOr
    | Implies
    | Truth
    | Falsum
)


def parse_string(input_string: str) -> list[Item]:
    expr = get_expr()
    return expr.parse_string(input_string, parseAll=True).as_list()
