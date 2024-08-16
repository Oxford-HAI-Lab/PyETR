# Troubleshooting with verbose mode

It may be that the output of the program doesn't produce what you expected. If this is the case, there is a feature that might be useful to you. You can inspect the internal operations that occur during another operation.

Let's take for example an update and factor operation:

```py
from pyetr import View

v1 = View.from_str("{~Q(q())~P(p()), 0}^{~Q(q())}")
        
v2 = View.from_str("{P(p())}")

v3 = v1.update(v2) # {P(p()),P(p())~P(p())~Q(q())}^{~Q(q())}
print(v3.to_str())

falsum = View.from_str("{}")
v4 = v3.factor(falsum) # {P(p())}^{~Q(q())}
print(v4.to_str())
```

But suppose I wanted to know what was happening in side the update operation, I could enable verbose mode:

```py
from pyetr import View

v1 = View.from_str("{~Q(q())~P(p()), 0}^{~Q(q())}")
        
v2 = View.from_str("{P(p())}")

v3 = v1.update(v2, verbose=True)
```
...and the output shows:

```
UpdateInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
UniProdInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
UniProdOutput: {~P(p)~Q(q),0}^{~Q(q)}
ExiSumInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
ExiSumOutput: {~P(p)~Q(q),0}^{~Q(q)}
AnswerInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
EquilibriumAnswerInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
Potentials: [(0, ~P(p)~Q(q)), (0, 0)]
EquilibriumAnswerOutput: {~P(p)~Q(q),0}^{~Q(q)}
AtomicAnswerInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
AtomicAnswerOutput: {~P(p)~Q(q),0}^{~Q(q)}
AnswerOutput: {~P(p)~Q(q),0}^{~Q(q)}
MergeInput: External: {~P(p)~Q(q),0}^{~Q(q)} Internal {P(p)}^{0}
MergeOutput: {~P(p)~Q(q)P(p),P(p)}^{~Q(q)}
UpdateOutput: {~P(p)~Q(q)P(p),P(p)}^{~Q(q)}
```

Here we see that the only operation that actually affecting the output is the "merge" operation. This shows that we can both learn more about the internal operations using this, and also see which step is behaving unusually for troubleshooting.
