from pyetr import View
from pyetr.inference import default_decision

v = View.from_str("{do(Buy(Video()*)),~do(Buy(Video()))}")
cv = View.from_str("Ax {Fun()}^{do(Buy(x*))}")
pr = View.from_str("{1=+ 0} ^ {Fun()}")

result = default_decision(dq=v, cv=[cv], pr=[pr])
print(result)  # {do(Buy(Video()*))}
