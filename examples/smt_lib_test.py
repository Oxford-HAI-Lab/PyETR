from pysmt.environment import Environment

from pyetr import View

v = View.from_str("{==(f(),3)}")
print(v)
parsed = v.to_smt_lib()
print(parsed)
v = View.from_smt_lib(parsed)
print(v)
