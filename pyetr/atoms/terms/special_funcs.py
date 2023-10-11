from .function import Function


def multi_func_new(i: float, j: float):
    return i * j


def sum_func_new(*x: float):
    return sum(x)


XBar = Function("XBar", 2, func_caller=multi_func_new)
Summation = Function("Summation", 1, func_caller=sum_func_new)
