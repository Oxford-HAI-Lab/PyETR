import math

from pyetr.atoms.terms import Function


def div(x: float, y: float) -> float:
    return x / y


def power(x: float, y: float) -> float:
    return x**y


def log(x: float) -> float:
    return math.log(x, 10)
