# Example

## Intro

For this example we'll be basing it on Example 17 from the book.

Example 17, p83

P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.

P2 There is a king in the hand.

C There isn't an ace in the hand.

## Step 1: Import package
```py
from pyetr import ViewParser, default_inference_procedure
```
Import the parsing object

## Step 2: Create object form of views

P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.

```py
p1 = ViewParser.from_str(
    "{~King(k())Ace(a()),King(k())~Ace(a())}"
)
```
P2 There is a king in the hand.
```py
p2 = ViewParser.from_str("{King(k())}")
```

## Step 3: Check result
```py
c = default_inference_procedure((p1, p2))
print(c) #"{~Ace(a())}"
```

## Full Example

```py
from pyetr import ViewParser, default_inference_procedure
p1 = ViewParser.from_str(
    "{~King(k())Ace(a()),King(k())~Ace(a())}"
)
p2 = ViewParser.from_str("{King(k())}")
c = default_inference_procedure((p1, p2))
print(c) #"{~Ace(a())}"
```
# Case Example
```py
from pyetr.cases import e17
print(e17.v) # ({~King(k())Ace(a()),King(k())~Ace(a())}, {King(k())})
print(e17.__doc__) #  Example 17, p83 ...(description)
print(e17.c)
default_inference_procedure(e17.v)
```
# Object methods, update etc

# Default decision
