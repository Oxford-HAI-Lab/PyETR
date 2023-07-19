from pyparsing import Forward, Group, Suppress, Word, alphas, infixNotation, opAssoc

# Define grammar
expr = Forward()

function_name = Word(alphas)
function_arg = expr | Word(alphas)

function_call = function_name + Suppress("(") + Group(function_arg) + Suppress(")")
expr <<= function_call | function_name

# Define operators precedence and associativity
precedence = []

# Create parser
parser = infixNotation(expr, precedence)

# Test input
input_expr = "f(g(x), f(x, y))"
result = parser.parseString(input_expr)[0]
print(result)
