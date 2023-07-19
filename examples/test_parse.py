from pyetr.parsing.parse_item import parse_items
from pyetr.parsing.parse_string import parse_string

# input_string = (
#     "∃x ∃y ∀z ∀w (King(x,y) ∧ Queen(y) ∧ (Jack() → z = x) ∧ (Queen(w) → w = y)) ∨ ⊥"
# )
input_string = "∃x ∃y ∃z ∃w ((P(Mary, x) ∧ Ace(y)) ∧ ((P(z, King(y))) ∨ (P(John, x) ∧ (P(w, Queen(z)) ∧ P(w, Jack(y))))))"

# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
# input_string = "∃x ∃y ∀z ∀w (King(x(y)) ∨ ~Queen(y) ∧ (King(x) ∧ Jack(y)))"
# input1 = "∃x ∃y ∃z ∃w [Pro(Mary(), x) ∧ Ace(y)]"# ∧ ((P(z, King(y))) ∨ (P(John, x) ∧ (P(w, Queen(z)) ∧ P(w, Jack(y))))))"
# input_string = "∃x ∃y ∀z ∀w y(x(a,b,c()), d)"
result = parse_string(input_string)
print(result)
out = parse_items(result)

print(out)
