import sys

from pyetr import parse_string_to_view
from pyetr.parsing import parse_view_to_string
from pyetr.parsing.parse_item import parse_items
from pyetr.parsing.parse_string import parse_string
from pyetr.parsing.unparse_item import unparse_items
from pyetr.parsing.unparse_view import unparse_view

sys.setrecursionlimit(10000)
# NOTE: Recursion bug caused by limit not being high enough
# input_string = "∃x ∀y ∃z ∃w ((P(Mary(), x) ∨ P(f_Ace(y), x)) ∨ ((P(z, f_King(y))) ∧ (P(John(), x) ∨ (P(w, f_Queen(z)) ∨ P(w, f_Jack(y))))))"
input_string = "∃x ∃y ∃z (P(Mary(), z, y) ∨ P(John(), x, y*))"
bugged1 = "∃x ∀y ∃z ∃w P(w, f_Queen(z*)) ∨ P(w, f_Jack(y*))"
bugged2 = "∃x ∀y ∃z ∃w ((((P(w, f_Queen(z)) ∨ P(w, f_Jack(y)))))"
# input_string = "∃x ∀y ∃z ((P(Mary(), x) ∨ P(f_Ace(y), x)) ∨ ((P(z, f_King(y))) ∨ (P(John(), x))))"
# input_string = "∃x ∀w ∃z ∀y (P(John(), x,x) ∨ (P(w, f_Queen(z*),x) ∨ P(w, f_Jack(y*),x))) ∨ (P(Mary(), z, y) ∨ P(John(), x, y*))"
# # input_string = "(InHand(*Ace()) ∧ InHand(Queen())) ∨ (InHand(Jack()))"
print(bugged1)
intermed = parse_string(bugged1)
# print(intermed)
view = parse_items(intermed)
# print(view)
out = unparse_view(view)
# print(out)
output_string = unparse_items(out)
print(output_string)
# parse_string_to_view(input_string1).product(parse_string_to_view(input_string2))
