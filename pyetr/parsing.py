import pyparsing as pp

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore


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


class BoolAnd:
    def __init__(self, t) -> None:
        self.operands = t[0]

    def __repr__(self) -> str:
        return f"<BoolAnd operands={self.operands}>"


expr = pp.Forward()
atom = pp.Word(pp.alphas, pp.alphanums).setResultsName("atom")

quantifier = pp.oneOf(
    "∃ ∀",
).setResultsName("quantifier")
quantified_expr = pp.Group(quantifier + atom).setParseAction(Quantified)

bool_and = pp.Suppress(pp.Char("∧").setResultsName("bool_and", listAllMatches=True))
# ∨
predicate = (
    pp.Group(
        pp.Word(pp.alphas, pp.alphanums).setResultsName("predicate")
        + pp.Suppress("(")
        + atom
        + pp.Suppress(")")
    )
    .setResultsName("predicate_grp", listAllMatches=True)
    .setParseAction(Pred)
)

nested_and = pp.infixNotation(
    predicate,
    [(bool_and, 2, pp_left, BoolAnd)],
    lpar=pp.Suppress("("),
    rpar=pp.Suppress(")"),
).setResultsName("logical", listAllMatches=True)
expr <<= pp.ZeroOrMore(quantified_expr) + nested_and


def parse_formula(input_string):
    return expr.parse_string(input_string, parseAll=True)


# input_string = '∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(z) → z = x] ∧ [Queen(w) → w = y]]'
# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
input_string = "∃x ∃y ∀z ∀w (King(x) ∧ Queen(y) ∧ (King(x) ∧ Jack(y)))"
result = parse_formula(input_string)

print(result.as_list())

# bits to add
# negation '~'
# conjunction '&'
# disjunction = pp.Group(expr + pp.Suppress('|') + expr)
# implication = pp.Group(expr + pp.Suppress('→') + expr)
