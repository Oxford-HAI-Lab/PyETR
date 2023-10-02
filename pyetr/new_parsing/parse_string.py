import sys
from functools import cache

import pyparsing as pp
from pyparsing import ParserElement

from pyetr.common_parsing import Quantified, Variable

sys.setrecursionlimit(10000)

ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore


class Atom:
    predicate_name: str
    terms: list["Term"]
    verifier: bool

    def __init__(self, t) -> None:
        if t[0] == "~":
            self.verifier = False
            self.predicate_name = t[1]
            self.terms = t[2:]
        else:
            self.verifier = True
            self.predicate_name = t[0]
            self.terms = t[1:]

    def __repr__(self) -> str:
        return f"<Atom name={self.predicate_name} terms={self.terms} verifier={self.verifier}>"

    def to_string(self):
        if self.verifier:
            not_str = ""
        else:
            not_str = "~"
        terms = ",".join([t.to_string() for t in self.terms])
        return f"{not_str}{self.predicate_name}({terms})"


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
        return f"<DoAtom atoms={self.atoms}> polarity={self.polarity}>"

    def to_string(self):
        if self.polarity:
            not_str = ""
        else:
            not_str = "~"
        out = ",".join([a.to_string() for a in self.atoms])
        return f"{not_str}do({out})"


class State:
    def __init__(self, t) -> None:
        self.atoms = t

    def __repr__(self) -> str:
        return f"<State atoms={self.atoms}>"

    def to_string(self) -> str:
        if len(self.atoms) == 0:
            return "0"
        else:
            return "".join([a.to_string() for a in self.atoms])


class Truth:
    def __init__(self, t) -> None:
        pass

    def __repr__(self) -> str:
        return f"<Truth>"

    def to_string(self) -> str:
        return "0"


class Supposition:
    def __init__(self, t) -> None:
        self.states = t

    def __repr__(self) -> str:
        return f"<Supposition states={self.states}>"

    def to_string(self) -> str:
        out = ",".join([s.to_string() for s in self.states])
        return "{" + f"{out}" + "}"


class Term:
    def to_string(self) -> str:
        raise NotImplementedError


class Comma:
    operands: list["Term"]

    def __init__(self, t) -> None:
        assert len(t) == 1
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<Comma operands={self.operands}>"

    def to_string(self):
        return ",".join([o.to_string() for o in self.operands])


class Function(Term):
    args: list["Term"]
    name: Comma

    def __init__(self, t) -> None:
        if len(t) == 1 and isinstance(t[0], str):
            self.name = t[0]
            self.args = []
        else:
            items = t[0]
            self.name = items[0]
            self.args = items[1].operands

    def __repr__(self) -> str:
        return f"<Function name={self.name} args={self.args}>"

    def to_string(self):
        out = ",".join([o.to_string() for o in self.args])
        return f"{self.name}({out})"


class Emphasis(Term):
    arg: "Term"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<Emphasis arg={self.arg}>"

    def to_string(self):
        return f"*{self.arg.to_string()}"


class Xbar(Term):
    left: Term
    right: Term

    def __init__(self, t) -> None:
        if len(t) == 1:
            items = t[0]
            self.left = items[0]
            self.right = items[2]

    def __repr__(self) -> str:
        return f"<Xbar left={self.left} right={self.right}>"

    def to_string(self):
        return f"{self.left.to_string()}**{self.right.to_string()}"


@cache
def get_terms(variable: ParserElement) -> ParserElement:
    function_word = (
        pp.Literal("++") | pp.Literal("σ") | pp.Word(pp.alphas, pp.alphanums)
    ).setResultsName("predicate")
    function_0 = (function_word + pp.Suppress("()")).setParseAction(Function)
    emphasis = pp.Suppress(pp.Char("*"))
    xbar = pp.Literal("**")
    comma = pp.Suppress(",")
    terms = pp.infixNotation(
        function_0 | variable,
        [
            (function_word, 1, pp_right, Function),
            (xbar, 2, pp_left, Xbar),
            (emphasis, 1, pp_left, Emphasis),
            (comma, 2, pp_left, Comma),
        ],
        lpar=pp.Suppress("("),
        rpar=pp.Suppress(")"),
    )
    return pp.ZeroOrMore(terms)


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

    atom_contents = get_terms(variable).setResultsName("terms", listAllMatches=True)

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
    verum = pp.Suppress(pp.Literal("0")).setParseAction(State)
    state = (
        pp.ZeroOrMore(doatom | atom)
        .setResultsName("state", listAllMatches=True)
        .setParseAction(State)
    )
    supposition = (
        (
            pp.Suppress("{")
            + pp.Optional(pp.DelimitedList(verum | state, ","))
            + pp.Suppress("}")
        )
        .setResultsName("supposition", listAllMatches=True)
        .setParseAction(Supposition)
    )

    expr <<= pp.ZeroOrMore(quantified_expr) + supposition
    return expr


def parse_string(input_string: str):
    expr = get_expr()
    return expr.parse_string(input_string, parseAll=True).as_list()
