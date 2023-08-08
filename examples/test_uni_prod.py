from pyetr.inference import default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View

p1 = ps("∀x ∃a (P(x*) ∧ E(x,a)) ∨ ~P(x)")
p2 = ps("P(j()*)")
c = ps("∃a (P(j()*) ∧ E(j(),a)) ∨ ~P(j())")

result = p1.universal_product(p2)
print(result)
print(c)
assert result.is_equivalent_under_arb_sub(c)
