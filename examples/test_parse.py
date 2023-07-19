from pyetr.parsing.parse_item import gather_variables, parse_items
from pyetr.parsing.parse_string import Variable, parse_string

input_string = (
    "∃x ∃y ∀z ∀w (King(x,y) ∧ Queen(y) ∧ (Jack() → z = x) ∧ (Queen(w) → w = y)) ∨ ⊥"
)
# input_string = "∃x ∃y ∃z ∃w ((P(Mary, x) ∧ Ace(x)) ∧ P(z, King(y)) ∨ (P(John, z) ∧ Queen(z))) ∧ (P(w, Jack(y))))"

# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
# input_string = "∃x ∃y ∀z ∀w (King(x) ∨ ~Queen(y) ∧ (King(x) ∧ Jack(y)))"
result = parse_string(input_string)
print(result)
out = parse_items(result)

print(out)
