__all__ = [
    "Variable",
    "Predicate",
    "Quantified",
    "BoolNot",
    "BoolAnd",
    "BoolOr",
    "Implies",
    "Equals",
    "Item",
    "parse_string",
]

from functools import cache
from typing import ClassVar

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


class BoolNot:
    arg: "Item"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<BoolNot arg={self.arg}>"


class TwoOperand:
    name: ClassVar[str]
    left: "Item"
    right: "Item"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 2
        self.left = t[0][0]
        self.right = t[0][1]

    def __repr__(self) -> str:
        return f"<{self.name} left={self.left} right={self.right}>"


class MultiOperand:
    name: ClassVar[str]
    operands: list["Item"]

    def __init__(self, t) -> None:
        assert len(t) == 1
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<{self.name} operands={self.operands}>"


class BoolAnd(MultiOperand):
    name = "BoolAnd"


class BoolOr(MultiOperand):
    name = "BoolOr"


class Comma(MultiOperand):
    name = "Comma"


class Implies(TwoOperand):
    name = "Implies"


class Equals(TwoOperand):
    name = "Equals"


class Truth:
    def __init__(self, t) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Truth>"


class Falsum:
    def __init__(self, t) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Falsum>"


class Predicate:
    variables: list["Item"]
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
        return f"<Predicate args={self.args} name={self.name}>"


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

    predicate_word = pp.Word(pp.alphas, pp.alphanums).setResultsName("predicate")
    predicate_0 = pp.Group(predicate_word + pp.Suppress("()")).setParseAction(Predicate)

    truth = pp.Char("⊤").setParseAction(Truth)
    falsum = pp.Char("⊥").setParseAction(Falsum)
    comma = pp.Suppress(",")
    nested_and = pp.infixNotation(
        predicate_0 | variable | truth | falsum,
        [
            (predicate_word, 1, pp_right, Predicate),
            (bool_not, 1, pp_right, BoolNot),
            (bool_and, 2, pp_left, BoolAnd),
            (bool_or, 2, pp_left, BoolOr),
            (equals, 2, pp_left, Equals),
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
    | Predicate
    | Quantified
    | BoolNot
    | BoolAnd
    | BoolOr
    | Implies
    | Equals
    | Truth
    | Falsum
)


def parse_string(input_string: str) -> list[Item]:
    expr = get_expr()
    return expr.parse_string(input_string, parseAll=True).as_list()
