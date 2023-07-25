from pyetr import parse_string_to_view
from pyetr.atom import Atom, Predicate
from pyetr.parsing.parse_item import parse_items
from pyetr.parsing.parse_string import parse_string
from pyetr.stateset import set_of_states, state
from pyetr.term import ArbitraryObject

# input_string = (
#     "∃x ∃y ∀z ∀w (King(x,y) ∧ Queen(y) ∧ (Jack() → z = x) ∧ (Queen(w) → w = y)) ∨ ⊥"
# )
input_string1 = "∃x ∀y ∃z ∃w ((P(Mary(), x) ∨ P(*f_Ace(y), x)) ∨ ((P(z, f_King(y))) ∨ (P(John(), x) ∨ (P(w, f_Queen(z)) ∨ P(w, f_Jack(y))))))"
input_string2 = "∃x P(*x, Mary())"
# input_string = "∃x ∃y ∀z ∀w [King(x) ∧ Queen(y) ∧ [King(x) ∧ Jack(y)]]"
# input_string = "∃x ∃y ∀z ∀w (King(x(y)) ∨ ~Queen(y) ∧ (King(x) ∧ Jack(y)))"
# input1 = "∃x ∃y ∃z ∃w [Pro(Mary(), x) ∧ Ace(y)]"# ∧ ((P(z, King(y))) ∨ (P(John, x) ∧ (P(w, Queen(z)) ∧ P(w, Jack(y))))))"
# input_string = "∃x ∃y ∀z ∀w y(x(a,b,c()), d)"
# result = parse_string(input_string1)
# print(result)
# out = parse_items(result)

# print(out)


out1 = parse_string_to_view(input_string1)
out2 = parse_string_to_view(input_string2)
result = out1.answer(out2)

print(result)


# input_string1 = "(InHand(*Ace()) ∧ InHand(Queen())) ∨ (InHand(Jack()))"
# input_string2 = "(InHand(*Ace))"
# result = parse_string(input_string1)
# print(result)
# out = parse_items(result)
