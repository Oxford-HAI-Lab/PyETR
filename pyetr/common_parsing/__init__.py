class Variable:
    name: str

    def __init__(self, t) -> None:
        self.name = t[0]

    def __repr__(self) -> str:
        return f"<Variable name={self.name}>"

    def to_string(self) -> str:
        return self.name


class Quantified:
    variable: Variable
    quantifier: str

    def __init__(self, t) -> None:
        variables = t[0].variables
        assert len(variables) == 1
        quantifier = t[0].quantifier
        if quantifier == "A":
            self.quantifier = "∀"
        elif quantifier == "E":
            self.quantifier = "∃"
        else:
            self.quantifier = quantifier
        self.variable = variables[0]

    def __repr__(self) -> str:
        return f"<Quantified variable={self.variable} quantifier={self.quantifier}>"

    def to_string(self) -> str:
        return self.quantifier + self.variable.to_string()
