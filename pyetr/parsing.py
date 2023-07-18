import pyparsing as pp
from pyparsing import ParserElement

ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore


class Atom:
    var: str

    def __init__(self, t) -> None:
        self.var = t[0]

    def __repr__(self) -> str:
        return f"<Atom var={self.var}>"


class Pred:
    atom: str
    predicate: str

    def __init__(self, t) -> None:
        self.predicate = t[0].predicate
        self.atom = t[0].atom

    def __repr__(self) -> str:
        return f"<Pred atom={self.atom} predicate={self.predicate}>"


class Quantified:
    atom: str
    quantifier: str

    def __init__(self, t) -> None:
        self.atom = t[0].atom
        self.quantifier = t[0].quantifier

    def __repr__(self) -> str:
        return f"<Quantified atom={self.atom} quantifier={self.quantifier}>"


class BoolNot:
    def __init__(self, t) -> None:
        assert len(t) == 1
        assert len(t[0]) == 1
        self.arg = t[0][0]

    def __repr__(self) -> str:
        return f"<BoolNot arg={self.arg}>"


class BoolAnd:
    def __init__(self, t) -> None:
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<BoolAnd operands={self.operands}>"


class BoolOr:
    def __init__(self, t) -> None:
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<BoolOr operands={self.operands}>"


class Implies:
    def __init__(self, t) -> None:
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<Implies operands={self.operands}>"


class Equals:
    def __init__(self, t) -> None:
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<Equals operands={self.operands}>"


expr = pp.Forward()
atom = pp.Word(pp.alphas, pp.alphanums).setResultsName("atom").setParseAction(Atom)

quantifier = pp.oneOf(
    "∃ ∀",
).setResultsName("quantifier")
quantified_expr = pp.Group(quantifier + atom).setParseAction(Quantified)

bool_not = pp.Suppress(pp.oneOf("~"))
bool_or = pp.Suppress(pp.oneOf("∨ |"))
bool_and = pp.Suppress(pp.oneOf("∧ &"))
implies = pp.Suppress(pp.Char("→"))
equals = pp.Suppress(pp.oneOf("="))

predicate = pp.Group(
    pp.Word(pp.alphas, pp.alphanums).setResultsName("predicate")
    + pp.Suppress("(")
    + atom
    + pp.Suppress(")")
).setParseAction(Pred)

nested_and = pp.infixNotation(
    predicate | atom,
    [
        (bool_not, 1, pp_right, BoolNot),
        (bool_and, 2, pp_left, BoolAnd),
        (bool_or, 2, pp_left, BoolOr),
        (equals, 2, pp_left, Equals),
        (implies, 2, pp_left, Implies),
    ],
    lpar=pp.Suppress("("),
    rpar=pp.Suppress(")"),
)
expr <<= pp.ZeroOrMore(quantified_expr) + nested_and

Item = Atom | Pred | Quantified | BoolNot | BoolAnd | BoolOr | Implies | Equals


def parse_formula(input_string: str) -> list[Item]:
    return expr.parse_string(input_string, parseAll=True).as_list()


input_string = (
    "∃x ∃y ∀z ∀w (King(x) ∧ Queen(y) ∧ (King(z) → z = x) ∧ (Queen(w) → w = y))"
)
# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
# input_string = "∃x ∃y ∀z ∀w (King(x) ∨ ~Queen(y) ∧ (King(x) ∧ Jack(y)))"
result = parse_formula(input_string)
print(result)
