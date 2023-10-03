from pyetr.new_parsing.parse_string import parse_string

test_string = "Ax Ey {Test(x,1003)~Test2(y)~do(A(x)B(y))Test3()do()~do(),Test4(y()),0,0,P(x**y)G(34,56.6,-78.4,-4,5==4)}"  # {John()|x=* Mary()|0.004=+ Teaches(x, Fred())P(), y|4|6.2=+ Teaches(y*, John())} ^{Q(4.5*)}"
# test_string = "Ax Ey {Test3(g(x,z(),y**z(o,p)))Test4()}"  # {John()|x=* Mary()|0.004=+ Teaches(x, Fred())P(), y|4|6.2=+ Teaches(y*, John())} ^{Q(4.5*)}"
test_string = "Ax Ey {John()|x=* Mary()|0.004=+ Teaches(x, Fred())P(), y|4|6.2=+ Teaches(y*, John())} ^{Q(4.5*)}"
# test_string = "Ax Ey {y|4|6.2=+ Teaches(y*, John())}"
out = parse_string(test_string)

print(test_string)
print(out.to_string())

# def log_func(x):
#     return 1 + math.log(1 + x)

# f = Function("log_func", 1,  func_caller=log_func)

# out = parse_string(test_string, custom_funcs = [f])

# def div_func(x: float,y: float):
#     return x / y

# f = Function("div_func", 2,  func_caller=div_func)

# out = parse_string(test_string, custom_funcs = [f])

# "Ax Ey {Test(x,div_func(2,3))}"
