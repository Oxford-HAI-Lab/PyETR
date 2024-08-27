from pyetr import View
from pyetr.inference import default_inference_procedure

p1 = View.from_str("{~King()Ace(),King()~Ace()}")
p2 = View.from_str("{King()}")
c = default_inference_procedure((p1, p2))
print(c)  # "{~Ace()}"
