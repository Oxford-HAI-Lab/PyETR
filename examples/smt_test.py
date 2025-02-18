from pysmt.shortcuts import Exists, ForAll, Symbol
from pysmt.typing import BOOL

from pyetr.parsing.smt_parser import smt_to_view

Student = Symbol("Student", BOOL)
Reads = Symbol("Reads", BOOL)
Book = Symbol("Book", BOOL)
z1 = Symbol("z1", BOOL)
w1 = Symbol("w1", BOOL)

expr = ForAll([z1], Exists([w1], Reads.Iff(Book)))

smt_to_view(expr)
