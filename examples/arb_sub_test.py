from pyetr import parse_string_to_view

input_string1 = "∃a ∃b ∃c (X(Phil(), a, b) ∨ P(Susan(), c, c*))"

input_string2 = "∃x ∃y ∃z (P(Susan(), z, z*)) ∨ X(Phil(), y, x)"

v1 = parse_string_to_view(input_string1)
v2 = parse_string_to_view(input_string2)
print(v1)
print(v2)
# This should be false
assert v1.is_equivalent_under_arb_sub(v2)

input_string3 = "∃x ∃y ∃z (P(Susan(), z, z*)) ∨ X(Phil(), x, y)"
v3 = parse_string_to_view(input_string3)
assert v1.is_equivalent_under_arb_sub(v3)
