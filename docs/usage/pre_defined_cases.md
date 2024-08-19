# Exploring the pre-defined cases

All of the examples from the book "Reason and Inquiry" are available as part of the PyETR package. Below is shown an example detailing how to extract one of these from the package. This lets you get started with views without having to construct any yourself. If you would like to find another example, please see the [case index](../reference/case_index.md). If would like to learn how to construct them yourself, please see [here](./view_construction.md).

!!! Info
    All examples with the prefix "new_" are not found in the book, and test other operations that we considered during implementation of the package.

Let's start off by inspecting one of the examples:

```py
from pyetr.cases import e17
print(e17)
```
Which outputs:
```
description:
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    
v (Views): (
   {~King(k())Ace(a()),~Ace(a())King(k())},
   {King(k())}
)
c (Conclusion): {~Ace(a())}
test(verbose=False): Method used to test the example
```

This starts off by describing the problem as it's presented in the book. It then shows in string form each of the views used in the problem, as well as the resulting conclusion. The test method runs the expected problem, and verifies that the output matches what is expected.

By running the problem in verbose mode, we can see each of the steps involved:

```python
e17.test(verbose=True)
```
Which outputs:
```
DeposeInput: {~King(k)Ace(a),~Ace(a)King(k)}^{0}
DeposeOutput: {~King(k)Ace(a),~Ace(a)King(k)}^{0}

UpdateInput: External: T Internal {~King(k)Ace(a),~Ace(a)King(k)}^{0}
UniProdInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
UniProdOutput: T
ExiSumInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
ExiSumOutput: T
AnswerInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
EquilibriumAnswerInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
Potentials: [(0, 0)]
EquilibriumAnswerOutput: T
AtomicAnswerInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
AtomicAnswerOutput: T
AnswerOutput: T
MergeInput: External: T Internal {~Ace(a)King(k),~King(k)Ace(a)}^{0}
MergeOutput: {~Ace(a)King(k),~King(k)Ace(a)}^{0}
UpdateOutput: {~Ace(a)King(k),~King(k)Ace(a)}^{0}


UpdateInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
UniProdInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
UniProdOutput: {~Ace(a)King(k),~King(k)Ace(a)}^{0}
ExiSumInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
ExiSumOutput: {~Ace(a)King(k),~King(k)Ace(a)}^{0}
AnswerInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
EquilibriumAnswerInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
Potentials: [(0, ~Ace(a)King(k)), (0, ~King(k)Ace(a))]
EquilibriumAnswerOutput: {~Ace(a)King(k),~King(k)Ace(a)}^{0}
AtomicAnswerInput: External: {~Ace(a)King(k),~King(k)Ace(a)}^{0} Internal {King(k)}^{0}
AtomicAnswerOutput: {~Ace(a)King(k)}^{0}
AnswerOutput: {~Ace(a)King(k)}^{0}
MergeInput: External: {~Ace(a)King(k)}^{0} Internal {King(k)}^{0}
MergeOutput: {~Ace(a)King(k)}^{0}
UpdateOutput: {~Ace(a)King(k)}^{0}

FactorInput: External: {~Ace(a)King(k)}^{0} Internal F
Contradiction factor
FactorOutput: {~Ace(a)King(k)}^{0}
DeposeInput: {~King(k)Ace(a),~Ace(a)King(k)}^{0}
DeposeOutput: {~King(k)Ace(a),~Ace(a)King(k)}^{0}
FactorInput: External: {~Ace(a)King(k)}^{0} Internal {~King(k)Ace(a),~Ace(a)King(k)}^{0}
Central case factor
FactorOutput: {~Ace(a)King(k)}^{0}
FactorInput: External: {~Ace(a)King(k)}^{0} Internal {King(k)}^{0}
Central case factor
FactorOutput: {~Ace(a)}^{0}
```

We can also inspect the input and output views:

```python
print(e17.v) # ({~King(k())Ace(a()),King(k())~Ace(a())}, {King(k())})
print(e17.c) # {~Ace(a())}
```

## Example Broken Down
### The default inference way

So this example really shows to compactness of using the examples. As I broke this down into individual steps in [First Steps](./first_steps.md), here I will simply present the example in full:

```py
from pyetr.cases import e17
from pyetr.inference import default_inference_procedure

result = default_inference_procedure(e17.v)
assert result == e17.c
print(result)
print(e17.c)
```
### The view operation way

However, we could also have done this using each of the underlying operations. See here:

```py
from pyetr.cases import e17
from pyetr import View

# Basic step
first = View.get_verum().update(e17.v[0].depose())
print(first) # {King()~Ace(),~King()Ace()}
g_prime = first.update(e17.v[1])
print(g_prime) # {King()~Ace()}

# G prime ops
g_prime = g_prime.factor(e17.v[0].depose())
print(g_prime) # {King()~Ace()}
result = g_prime.factor(e17.v[1])

print(result) # {~Ace()}
assert result == e17.c
```

Some can be excluded as no ops:

```py
from pyetr.cases import e17

# Basic step
g_prime = e17.v[0].update(e17.v[1])
print(g_prime) # {King()~Ace()}

#G prime ops
result = g_prime.factor(e17.v[1])

print(result) # {~Ace()}
assert result == e17.c
```

...and we can even break `update` down into its fundamental operations:

```py
from pyetr.cases import e17

# Basic step
g_prime = e17.v[0].universal_product(e17.v[1])
print(g_prime) # {Ace()~King(),~Ace()King()}
g_prime = g_prime.existential_sum(e17.v[1])
print(g_prime) # {Ace()~King(),~Ace()King()}
g_prime = g_prime.answer(e17.v[1])
print(g_prime) # {King()~Ace()}
g_prime = g_prime.merge(e17.v[1])
print(g_prime) # {King()~Ace()}

#G prime ops
result = g_prime.factor(e17.v[1])
print(result) # {~Ace()}
assert result == e17.c
```
Again, let's remove the no ops:

```py
from pyetr.cases import e17

# Basic step
g_prime = e17.v[0].answer(e17.v[1])
print(g_prime) # {King()~Ace()}

# G prime ops
result = g_prime.factor(e17.v[1])
print(result) # {~Ace()}
assert result == e17.c
```

So here we see that, for this example, the problem is reducible to only a couple of much simpler operations. A useful property of PyETR is that problems can be expressed using very general functions, or at a very granular level depending on the exact nature of the problem.
