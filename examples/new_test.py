from io import StringIO
from pprint import pprint

from pysmt.environment import Environment
from pysmt.fnode import SYMBOL, FNode
from pysmt.shortcuts import get_env, to_smtlib
from pysmt.smtlib.parser import SmtLibParser
from pysmt.smtlib.script import SmtPrinter

from pyetr import View
from pyetr.parsing.smt_parser import smt_to_view, view_to_smt

DEMO_SMTLIB = """
(declare-fun Professor (Bool) Bool)
(declare-fun Teaches (Bool Bool) Bool)
(declare-fun Student (Bool) Bool)
(assert (forall 
  (
    (x Bool)) 
  (exists 
    (
      (y Bool)) 
    (=> 
      (Professor x) 
      (and 
        (Teaches x y) 
        (Student y) 
        (Professor x))))) )
"""
parser = SmtLibParser(Environment())
script = parser.get_script(StringIO(DEMO_SMTLIB))

print(script.get_last_formula())
formula = script.get_last_formula()


parsed = View.from_smt(formula)
pprint(parsed)
pprint(parsed.to_smt())
pprint(View.from_smt(parsed.to_smt()))
print()


def test(formula):
    buf = StringIO()
    p = SmtPrinter(buf)
    p.printer(formula)
    res = buf.getvalue()
    buf.close()
    return res


def convert_symbol(fnode: FNode):
    t = fnode.get_type()
    if t.is_function_type():
        return (
            f"(declare-fun {fnode.symbol_name()} "
            + "("
            + " ".join(str(arg) for arg in t.param_types)
            + ") "
            + str(t.return_type)
            + ")"
        )
    else:
        return None


def format_brackets(text, indent_size=2):
    indent_level = 0
    result = ""
    indent = " " * indent_size
    i = 0
    while i < len(text):
        char = text[i]
        if char == "(":
            if indent_level == 0:
                result += "("
            else:
                result += "\n" + indent * indent_level + "("
            indent_level += 1
        elif char == ")":
            indent_level = max(0, indent_level - 1)
            result += ")"
        else:
            result += char
        i += 1
    return result


output_string = test(parsed.to_smt(get_env()))
ret = []
for x in get_env().formula_manager.get_all_symbols():
    out = convert_symbol(x)
    if out is not None:
        ret.append(out)
ret.append(f"(assert {format_brackets(output_string)} )")
print("\n".join(ret))
