from pyetr.parsing.parse_item import gather_atoms, parse_items
from pyetr.parsing.parse_string import Atom, parse_string

input_string = (
    "∃x ∃y ∀z ∀w (King(x,y) ∧ Queen(y) ∧ (King(z) → z = x) ∧ (Queen(w) → w = y))"
)
# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
# input_string = "∃x ∃y ∀z ∀w (King(x) ∨ ~Queen(y) ∧ (King(x) ∧ Jack(y)))"
result = parse_string(input_string)
print(result)
out = parse_items(result)

print(out)
