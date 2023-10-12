import math

from pyetr.atoms.terms import Function


def div(x: float, y: float) -> float:
    return x / y


div_func = Function(name="div", arity=2, func_caller=div)


def power(x: float, y: float) -> float:
    return x**y


power_func = Function(name="power", arity=2, func_caller=power)


def log(x: float) -> float:
    return math.log(x)


log_func = Function(name="log", arity=1, func_caller=log)
