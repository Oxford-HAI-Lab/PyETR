import pyparsing as pp

pp_left = pp.opAssoc.LEFT  # type:ignore
pp_right = pp.opAssoc.RIGHT  # type:ignore
expr = pp.Forward()


class Predicate:
    variables: list
    name: str

    def __init__(self, t) -> None:
        print(t)
        self.name = t[0][0]
        self.args = t[0][1:]

    def __repr__(self) -> str:
        return f"<Predicate args={self.args} name={self.name}>"


variable = pp.Word(pp.alphas, pp.alphanums)

predicate_word = pp.Word(pp.alphas, pp.alphanums)

predicate_0 = pp.Group(predicate_word + pp.Suppress("()")).setParseAction(Predicate)
comma = pp.Suppress(",")
infix = pp.infixNotation(
    predicate_0 | variable,
    [(predicate_word, 1, pp_right, Predicate), (comma, 2, pp_left)],
)
expr <<= infix

input_string = "y(x(a,b), z(x,y()))"
out = expr.parse_string(input_string, parseAll=True).as_list()
print(out)
