import sys
from dataclasses import dataclass
from functools import cache
from typing import Optional

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
        out = "".join([a.to_string() for a in self.atoms])
        return f"{not_str}do({out})"


class State:
    atoms: list[Atom | DoAtom]

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
    states: list[State]

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
    args: list["Term"]

    def __init__(self, t) -> None:
        assert len(t) == 1
        self.args = t[0]

    def __repr__(self) -> str:
        return f"<Comma args={self.args}>"

    def to_string(self):
        return ",".join([o.to_string() for o in self.args])


class Function(Term):
    args: list[Term]
    name: str

    def __init__(self, t) -> None:
        if len(t) == 1 and isinstance(t[0], str):
            self.name = t[0]
            self.args = []
        else:
            items = t[0]
            self.name = items[0]
            if len(items) == 2 and isinstance(items[1], Comma):
                self.args = items[1].args
            else:
                self.args = items[1:]

    def __repr__(self) -> str:
        return f"<Function name={self.name} args={self.args}>"

    def to_string(self):
        out = ",".join([o.to_string() for o in self.args])
        return f"{self.name}({out})"


class Summation(Term):
    args: list["Term"]

    def __init__(self, t) -> None:
        if len(t) == 1 and isinstance(t[0], str):
            self.args = []
        else:
            items = t[0]
            self.args = items[1].operands

    def __repr__(self) -> str:
        return f"<Summation args={self.args}>"

    def to_string(self):
        out = ",".join([o.to_string() for o in self.args])
        return f"σ({out})"


class Emphasis(Term):
    arg: "Term"

    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<Emphasis arg={self.arg}>"

    def to_string(self):
        return f"{self.arg.to_string()}*"


class Xbar(Term):
    left: Term
    right: Term

    def __init__(self, t) -> None:
        if len(t) == 1:
            items = t[0]
            self.left = items[0]
            self.right = items[1]

    def __repr__(self) -> str:
        return f"<Xbar left={self.left} right={self.right}>"

    def to_string(self):
        return f"{self.left.to_string()}**{self.right.to_string()}"


class Equals(Term):
    left: Term
    right: Term

    def __init__(self, t) -> None:
        if len(t) == 1:
            items = t[0]
            self.left = items[0]
            self.right = items[1]

    def __repr__(self) -> str:
        return f"<Equals left={self.left} right={self.right}>"

    def to_string(self):
        return f"{self.left.to_string()}=={self.right.to_string()}"


class Real(Term):
    num: float

    def __init__(self, t) -> None:
        self.num = float("".join(t))

    def to_string(self):
        return f"{self.num}"

    def __repr__(self) -> str:
        return f"<Real num={self.num}>"


class Weight:
    multiset: list["Term"]

    def __init__(self, t) -> None:
        self.multiset = t


class AdditiveWeight(Weight):
    def to_string(self):
        return f"{'|'.join([i.to_string() for i in self.multiset])}=+"

    def __repr__(self) -> str:
        return f"<AdditiveWeight num={self.multiset}>"


class MultiplicativeWeight(Weight):
    def to_string(self):
        return f"{'|'.join([i.to_string() for i in self.multiset])}=*"

    def __repr__(self) -> str:
        return f"<MultiplicativeWeight num={self.multiset}>"


class WeightedState:
    additive: Optional[AdditiveWeight]
    multiplicative: Optional[MultiplicativeWeight]
    state: State

    def __init__(self, t) -> None:
        self.additive = None
        self.multiplicative = None
        state = None
        for i in t:
            if isinstance(i, State):
                assert state is None
                state = i
            if isinstance(i, AdditiveWeight):
                assert self.additive is None
                self.additive = i
            if isinstance(i, MultiplicativeWeight):
                assert self.multiplicative is None
                self.multiplicative = i
        assert state is not None
        self.state = state

    def to_string(self):
        if self.additive:
            add_str = self.additive.to_string() + " "
        else:
            add_str = ""
        if self.multiplicative:
            mul_str = self.multiplicative.to_string() + " "
        else:
            mul_str = ""

        return f"{mul_str}{add_str}{self.state.to_string()}"

    def __repr__(self) -> str:
        return f"<WeightedState state={self.state} additive={self.additive} multiplicative={self.multiplicative}>"


class Stage:
    states: list[WeightedState]

    def __init__(self, t) -> None:
        self.states = t

    def __repr__(self) -> str:
        return f"<Stage states={self.states}>"

    def to_string(self) -> str:
        out = ",".join([s.to_string() for s in self.states])
        return "{" + f"{out}" + "}"


@cache
def get_terms(variable: ParserElement) -> ParserElement:
    function_word = (
        pp.Literal("++") | pp.Literal("σ") | pp.Word(pp.alphas, pp.alphanums)
    ).setResultsName("predicate")

    function_0 = (function_word + pp.Suppress("()")).setParseAction(Function)
    emphasis = pp.Suppress(pp.Char("*"))
    xbar = pp.Suppress(pp.Literal("**") | pp.Literal("x̄"))
    equals = pp.Suppress(pp.Literal("=="))
    comma = pp.Suppress(",")
    real_word = (
        pp.Optional(pp.Literal("-"))
        + pp.Word(pp.nums)
        + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))
    )
    reals = real_word.setResultsName("reals").setParseAction(Real)
    terms = pp.infixNotation(
        function_0 | reals | variable,
        [
            (function_word, 1, pp_right, Function),
            (xbar, 2, pp_left, Xbar),
            (equals, 2, pp_left, Equals),
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
    new_alphas = pp.alphas.replace("A", "").replace("E", "")
    variable = (
        pp.Word(init_chars=new_alphas, body_chars=new_alphanums)
        .setResultsName("variables", listAllMatches=True)
        .setParseAction(Variable)
    )

    quantifier = pp.oneOf(
        "∃ ∀ E A",
    ).setResultsName("quantifier")
    quantified_expr = pp.Group(quantifier + variable).setParseAction(Quantified)

    do_word = pp.Literal("do")
    predicate_word = pp.Word(pp.alphanums) + ~do_word

    terms = get_terms(variable).setResultsName("terms", listAllMatches=True)

    atom = (
        pp.Optional("~")
        + predicate_word
        + pp.Suppress("(")
        + terms
        + pp.Suppress(")").setResultsName("atom", listAllMatches=True)
    ).setParseAction(Atom)
    doatom = (
        (
            pp.Optional("~")
            + pp.Suppress(do_word)
            + pp.Suppress("(")
            + pp.ZeroOrMore(atom)
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
    weights = pp.DelimitedList(terms, "|")
    additive_weight = pp.Optional(
        (weights + pp.Suppress(pp.Literal("=+"))).setParseAction(AdditiveWeight)
    )
    multiplicative_weight = pp.Optional(
        (weights + pp.Suppress(pp.Literal("=*"))).setParseAction(MultiplicativeWeight)
    )
    weighted_state = (
        (multiplicative_weight + additive_weight) + (verum | state)
    ).setParseAction(WeightedState)
    stage = (
        (
            pp.Suppress("{")
            + pp.Optional(pp.DelimitedList(weighted_state, ","))
            + pp.Suppress("}")
        )
        .setResultsName("stage", listAllMatches=True)
        .setParseAction(Stage)
    )

    expr <<= (
        pp.ZeroOrMore(quantified_expr)
        + stage
        + pp.Optional(pp.Suppress(pp.Literal("^")) + supposition)
    )
    return expr


@dataclass
class ParserView:
    quantifiers: list[Quantified]
    stage: Stage
    supposition: Optional[Supposition]

    def to_string(self) -> str:
        if len(self.quantifiers) == 0:
            quant_str = ""
        else:
            quant_str = " ".join([s.to_string() for s in self.quantifiers]) + " "
        if self.supposition is None:
            supp_str = ""
        else:
            supp_str = f"^{self.supposition.to_string()}"
        return f"{quant_str}{self.stage.to_string()}{supp_str}"


def parse_string(input_string: str) -> ParserView:
    expr = get_expr()
    out = expr.parse_string(input_string, parseAll=True).as_list()
    quantifieds = []
    stage = None
    supposition = None
    for i in out:
        if isinstance(i, Quantified):
            quantifieds.append(i)
        elif isinstance(i, Stage):
            stage = i
        elif isinstance(i, Supposition):
            supposition = i
    assert stage is not None
    return ParserView(quantifiers=quantifieds, stage=stage, supposition=supposition)
