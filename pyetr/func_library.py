import math

from pyetr.atoms.terms import Function


def div(x: float, y: float) -> float:
    return x / y


div_func = Function.numeric(div)


def power(x: float, y: float) -> float:
    return x**y


power_func = Function.numeric(power)


def log(x: float) -> float:
    return math.log(x, 10)


log_func = Function.numeric(log)
