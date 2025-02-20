from pysmt.environment import Environment

from pyetr import View

v = View.from_str("{==(4,3)}")
v = View.from_str("{==(f(),g())}")
# v = View.from_str("{==(3,3)}")
# v = View.from_str("Ax {P(x*)}")

print(v)
parsed = v.to_smt_lib()
print(parsed)
v = View.from_smt_lib(parsed)
print(v)
