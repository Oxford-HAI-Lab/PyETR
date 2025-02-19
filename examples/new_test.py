# The last part of the example requires a QF_LIA solver to be installed.
#
#
# This example shows how to interact with files in the SMT-LIB
# format. In particular:
#
# 1. How to read a file in SMT-LIB format
# 2. How to write a file in SMT-LIB format
# 3. Formulas and SMT-LIB script
# 4. How to access annotations from SMT-LIB files
# 5. How to extend the parser with custom commands
#
from io import StringIO

from pysmt.smtlib.parser import SmtLibParser

from pyetr import View
from pyetr.parsing.smt_parser import smt_to_view

DEMO_SMTLIB = """
(declare-sort A 0)

(declare-const a Real)
(declare-const b Real)

(declare-fun f (Real Real) Real)

(assert (= (f 1.25 a) b))
"""
parser = SmtLibParser()
script = parser.get_script(StringIO(DEMO_SMTLIB))
# ∃x {Thermotogum(x*)StainsGramNegative(x)}
print(script.get_last_formula())
formula = script.get_last_formula()
if formula.is_and():
    out = [View._from_view_storage(smt_to_view(arg)) for arg in formula.args()]
else:
    out = View._from_view_storage(smt_to_view(script.get_last_formula()))
from pprint import pprint

pprint(out)
