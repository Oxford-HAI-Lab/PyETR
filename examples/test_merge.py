from pyetr.inference import default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View

p1 = ps("∀x ∃y ((IsPerson(x) → IsPerson(x) ∧ IsSugary(y*) ∧ Eats(x,y)))")
p2 = ps("∀a ∃b (IsSugary(a*) → Hates(b,a))")
c = ps("∀x ∃y ∃z ((IsPerson(x) → IsPerson(x) ∧ IsSugary(y*) ∧ Eats(x,y) ∧ Hates(z,y)))")

result = p1.merge(p2)
print(result)
print(c)
assert result.is_equivalent_under_arb_sub(c)
