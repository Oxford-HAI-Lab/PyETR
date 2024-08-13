# First Steps

## Intro

For this example we'll be basing it on Example 17 from the book.
!!! quote "Example 17, p83"

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.

    P2 There is a king in the hand.

    C There isn't an ace in the hand.

For the full code see [here](#full-example)
## Step 1: Import package
```python
from pyetr import View
from pyetr.inference import default_inference_procedure
```
Import the parsing object

## Step 2: Create object form of views

P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.

```py
p1 = View.from_str(
    "{~King(k())Ace(a()),King(k())~Ace(a())}"
)
```
P2 There is a king in the hand.
```py
p2 = View.from_str("{King(k())}")
```

## Step 3: Check result
```py
c = default_inference_procedure((p1, p2))
print(c) #"{~Ace(a())}"
```

## Full Example

```py
from pyetr import View
from pyetr.inference import default_inference_procedure

p1 = View.from_str(
    "{~King(k())Ace(a()),King(k())~Ace(a())}"
)
p2 = View.from_str("{King(k())}")
c = default_inference_procedure((p1, p2))
print(c) #"{~Ace(a())}"
```
