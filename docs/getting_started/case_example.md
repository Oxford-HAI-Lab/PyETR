# Exploring the pre-defined cases

All of the examples from the book "Reason and Inquiry" are available as part of the PyETR package. Below is shown an example detailing how to extract one of these from the package. This lets you get started with views without having to construct any yourself. If you would like to find another example, please see the case index. If would like to learn how to construct them yourself, please see here.

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
```python
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
default_inference_procedure(e17.v)
### The view operation way
