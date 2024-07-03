import pyetr.cases
from pyetr.cases import BaseExample

out = []
for name, case in vars(pyetr.cases).items():
    if isinstance(case, type) and issubclass(case, BaseExample) and case != BaseExample:
        out.append(name)
print(out)
