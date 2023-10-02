from pyetr.new_parsing.parse_string import parse_string

test_string = "Ax Ey {Test(x)~Test2(y)~do(A(x),B(y))Test3()do()~do(),Test4(y()),0,0}"  # {John()|x=* Mary()|0.004=+ Teaches(x, Fred())P(), y|4|6.2=+ Teaches(y*, John())} ^{Q(4.5*)}"
# test_string = "Ax Ey {Test3(g(x,z(),y**z(o,p)))Test4()}"  # {John()|x=* Mary()|0.004=+ Teaches(x, Fred())P(), y|4|6.2=+ Teaches(y*, John())} ^{Q(4.5*)}"

out = parse_string(test_string)
print(out)
print(" ".join([i.to_string() for i in out]))
