from functools import cache

import pyparsing as pp
from pyparsing import ParserElement

from pyetr.common_parsing import Quantified, Variable

ParserElement.enablePackrat()


class Atom:
    predicate_name: str
    contents: str
    verifier: bool

    def __init__(self, t) -> None:
        if len(t) == 1:
            self.contents = ""
            self.predicate_name = t[0]
            self.verifier = True
        elif t[0] == "~":
            self.verifier = False
            self.predicate_name = t[1]
            self.contents = t[2]
        else:
            self.verifier = True
            self.predicate_name = t[0]
            self.contents = t[1]

    def __repr__(self) -> str:
        return f"<Atom name={self.predicate_name} contents={self.contents} verifier={self.verifier}>"


class DoAtom:
    atoms: list[Atom]

    def __init__(self, t) -> None:
        if len(t) == 0:
            self.atoms = []
            self.polarity = True
        elif t[0] == "~":
            self.polarity = False
            self.atoms = t[1:]
        else:
            self.polarity = True
            self.atoms = t

    def __repr__(self) -> str:
        return f"<DoAtom atoms={self.atoms}> polarity={self.polarity}"


class Supposition:
    def __init__(self, t) -> None:
        self.atoms = t

    def __repr__(self) -> str:
        return f"<Supposition atoms={self.atoms}>"


@cache
def get_expr():
    expr = pp.Forward()

    new_alphanums = pp.alphanums.replace("A", "").replace("E", "")

    variable = (
        pp.Word(new_alphanums)
        .setResultsName("variables", listAllMatches=True)
        .setParseAction(Variable)
    )

    quantifier = pp.oneOf(
        "∃ ∀ E A",
    ).setResultsName("quantifier")
    quantified_expr = pp.Group(quantifier + variable).setParseAction(Quantified)

    do_word = pp.Literal("do")
    predicate_word = pp.Word(pp.alphanums) + ~do_word

    atom_contents = pp.ZeroOrMore(pp.Word(pp.alphanums))

    atom = (
        pp.Optional("~")
        + predicate_word
        + pp.Suppress("(")
        + atom_contents
        + pp.Suppress(")").setResultsName("atom", listAllMatches=True)
    ).setParseAction(Atom)
    doatom = (
        (
            pp.Optional("~")
            + pp.Suppress(do_word)
            + pp.Suppress("(")
            + pp.Optional(pp.DelimitedList(atom, ","))
            + pp.Suppress(")")
        )
        .setResultsName("doatom", listAllMatches=True)
        .setParseAction(DoAtom)
    )
    supposition = (
        (pp.Suppress("{") + pp.ZeroOrMore(doatom | atom) + pp.Suppress("}"))
        .setResultsName("supposition", listAllMatches=False)
        .setParseAction(Supposition)
    )

    expr <<= pp.ZeroOrMore(quantified_expr) + supposition
    return expr


def parse_string(input_string: str):
    expr = get_expr()
    return expr.parse_string(input_string, parseAll=True).as_list()
