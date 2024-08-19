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

The considerations for if two views are equal are quite simple. Broadly speaking, if the book would  view two views strings as identical, so will python equality. Notably this does not allow for different naming schemes etc - for two views to be equal they much express the same concept using the same notation. E.g.

```py
v1 = View.from_str("{A(f())B(f())}")
v2 = View.from_str("{B(f())A(f())}")

print(v1 == v2) # Returns True
```

Since the A and B atoms share the same state, the fact here they are in a different order in v1 vs v2 is irrelevant. Both these strings represent the exact same view. However if instead we try:

```py
v1 = View.from_str("{A(f(), g())}")
v2 = View.from_str("{A(g(), f())}")

print(v1 == v2) # Returns False
```

Since ordering matters inside the atom, these two views are not equal to one another. Wherever a set is used (e.g. States, Stage, Supposition, DoAtoms) ordering is irrelevant, but anywhere a tuple or ordered object is used ordering matters to the equality of two views.

## When are views are equivalent under substitution

The letters used to describe arbitrary objects are in some sense - arbitrary. We've therefore made a bespoke check for, if we were to ignore the different naming conventions of the arbitrary objects, would two views be equal. See the example below:

```py
v1 = View.from_str("∀x {A(x)}")
v2 = View.from_str("∀y {A(y)}")

print(v1 == v2) # Returns False
print(v1.is_equivalent_under_arb_sub(v2)) # Returns True
```
!!! info "Limit of Equivalence Check"
    Due to the fact the comparison must check all permutations for a series of arbitrary objects, there is a certain computation limit. The computational complexity is O((n!)^2*n) where n is average num of existentials and universals, so as you can imagine for a feasible number of arbitrary objects this become impractical. We've set the limit at 9 of each type in each view, which seems to process in a reasonable computation time. Anything higher than this is unlikely to appear in real world scenarios.
