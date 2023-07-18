from pprint import pprint

import pyparsing as pp

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore


expr = pp.Forward()
atom = pp.Word(pp.alphas, pp.alphanums).setResultsName("atom")

quantifier = pp.oneOf(
    "∃ ∀",
).setResultsName("quantifier")
quantified_expr = pp.Group(quantifier + atom).setResultsName(
    "quantified_expr", listAllMatches=True
)

operator = pp.oneOf("∧ ∨").setResultsName("operator", listAllMatches=True)
predicate = pp.Group(
    pp.Word(pp.alphas, pp.alphanums).setResultsName("predicate")
    + pp.Suppress("(")
    + atom
    + pp.Suppress(")")
).setResultsName("predicate_grp", listAllMatches=True)
nested_and = pp.infixNotation(predicate, [(operator, 2, pp_left)]).setResultsName(
    "logical", listAllMatches=True
)
expr <<= pp.ZeroOrMore(quantified_expr) + pp.nestedExpr(
    opener="[", closer="]", content=nested_and
).setResultsName("bracketed", listAllMatches=True)


def parse_formula(input_string):
    return expr.parse_string(input_string, parseAll=True)


# Test the parsing function
# input_string = '∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(z) → z = x] ∧ [Queen(w) → w = y]]'
input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ King(x)]"  # ∧ Jack(y)]]'
result = parse_formula(input_string)


print(result.as_list())
print()
pprint(result.as_dict())
print()
# print(result.dump())

# bits to add
# negation '~'
# conjunction '&'
# disjunction = pp.Group(expr + pp.Suppress('|') + expr)
# implication = pp.Group(expr + pp.Suppress('→') + expr)
