__all__ = [
    "parse_string",
]

from functools import cache

import pyparsing as pp
from pyparsing import ParseException, ParserElement

from pyetr.parsing.common import ParsingError, Quantified, Variable
from pyetr.parsing.fol_items import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicPredicate,
    Truth,
)
from pyetr.parsing.fol_items.items import LogicReal

ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT
pp_right = pp.opAssoc.RIGHT


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
        .setParseAction(Variable.from_pyparsing)
    )

    quantifier = pp.oneOf(
        "∃ ∀",
    ).setResultsName("quantifier")
    quantified_expr = pp.Group(quantifier + variable).setParseAction(
        Quantified.from_pyparsing
    )
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
    ).setParseAction(LogicPredicate.from_pyparsing)
    real_word = (
        pp.Optional(pp.Literal("-"))
        + pp.Word(pp.nums)
        + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))
    )
    reals = real_word.setResultsName("reals").setParseAction(LogicReal.from_pyparsing)

    truth = pp.Char("⊤").setParseAction(Truth)
    falsum = pp.Char("⊥").setParseAction(Falsum)
    nested_and = pp.infix_notation(
        predicate | reals | variable | truth | falsum,
        op_list=[
            (predicate_word, 1, pp_right, LogicPredicate.from_pyparsing),
            (emphasis, 1, pp_left, LogicEmphasis.from_pyparsing),
            (bool_not, 1, pp_right, BoolNot.from_pyparsing),
            (bool_and, 2, pp_left, BoolAnd.from_pyparsing),
            (bool_or, 2, pp_left, BoolOr.from_pyparsing),
            (implies, 2, pp_left, Implies.from_pyparsing),
        ],
        lpar=pp.Suppress("("),
        rpar=pp.Suppress(")"),
    )
    term <<= nested_and
    expr <<= pp.ZeroOrMore(quantified_expr) + nested_and
    return expr


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
