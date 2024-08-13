from pyetr import View
from pyetr.inference import default_inference_procedure

p1 = View.from_str("{~King(k())Ace(a()),King(k())~Ace(a())}")
p2 = View.from_str("{King(k())}")
c = default_inference_procedure((p1, p2))
print(c)  # "{~Ace(a())}"
