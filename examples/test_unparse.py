from pyetr import parse_string_to_view
from pyetr.parsing import parse_view_to_string
from pyetr.parsing.parse_item import parse_items
from pyetr.parsing.parse_string import parse_string
from pyetr.parsing.unparse_item import unparse_items
from pyetr.parsing.unparse_view import unparse_view

input_string = "∃x ∀y ∃z ∃w ((P(Mary(), x) ∨ P(f_Ace(y), x)) ∨ ((P(z, f_King(y))) ∧ (P(John(), x) ∨ (P(w, f_Queen(z)) ∨ P(w, f_Jack(y))))))"
input_string = "∃x (P(Mary(), x) ∨ P(Mary(), x))"
# input_string = "(InHand(*Ace()) ∧ InHand(Queen())) ∨ (InHand(Jack()))"
print(input_string)
intermed = parse_string(input_string)
# print(intermed)
view = parse_items(intermed)
# print(view)
out = unparse_view(view)
# print(out)
output_string = unparse_items(out)
print(output_string)

previous_strings = []
for i in range(100):
    new_out = parse_view_to_string(parse_string_to_view(output_string))
    if new_out in previous_strings:
        print(new_out)
        print(i)
        raise ValueError("Gotcha!")
    previous_strings.append(new_out)
    # print(new_out)
