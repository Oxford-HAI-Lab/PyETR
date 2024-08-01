# View Equality and Equivalence (advanced)

This might be considered something of an advanced topic, as it concerns the exact conditions we consider views to equal or equivalent. To understand this, you should be familiar with the theoretical definition of views.

## A note for python programmers

If you're quite familiar with Python, you may be quite surprised to find two separate View instances are equal to each other. This isn't a mistake - it's by design. We wanted to ensure that no matter where a view is instantiated, the resulting object is not necessarily unique. Take a quick example:

```py
class X:
    pass

x1 = X()
x2 = X()
print(x1 == x2) # Returns False
```

As expected, these two separate instances are not equal. But if we take two views:

```py
from pyetr import View

v1 = View.from_str("{}")
v2 = View.from_str("{}")

print(v1 == v2) # Returns True
```

This is because in the PyETR package we say that two object are equal if that represent exactly the same object, no matter where they were instantiated.

## When are views equal

The considerations for if two views are equals are quite simple. 

## When are views are equivalent under substitution

