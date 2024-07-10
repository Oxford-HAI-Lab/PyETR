# View construction

The basic way to create your own views is to specify them via a string representation which closely follows the notation used in *Reason & Inquiry*.
The same string representation is used for printing views as the results of calculations. [N.B. This isn't quite true, maybe we can make it true? Difference between `to_str` and `__str__`?]

For convenience, you only need to include in the string those parts of the view that are non-trivial or have non-default values.
Recall that *Reason & Inquiry* builds up to the full theory of views through iterative enrichments of the possible view contents.
Thus, by only relying on restricted kinds of content one can use *PyETR* for computations with any of the restricted theories of views in the earlier chapters of the book, even though *PyETR* is technically a single implementation of the full theory.
There are a few notational caveats which will become apparent below.

As an example, consider running the following code.
This code might also be useful as a template for testing out features detailed below.
```py
from pyetr import View

p1 = View.from_str("{GrassWet()}")
print("The view is " + p1.to_str())
print("\nIn detail:")
print(p1.detailed)
```
The output should be
```
The view is {GrassWet()}

In detail:
<View 
  stage={{<PredicateAtom predicate=<Predicate name=GrassWet arity=0> terms=()>}} 
  supposition={{}} 
  dep_rel=<DependencyRelation deps=[] unis=frozenset() exis=frozenset()> 
  issue_structure={} 
  weights=<Weights {'{<PredicateAtom predicate=<Predicate name=GrassWet arity=0> terms=()>}': '<Weight multi=<Multiset items=[]> add=<Multiset items=[]>>'}> 
>
```
Observe that the basic method for creating a view from a string representation is the `Vfrom_str` method of the `View` class.
To turn a view object into a string, use `to_str` of that view object.

This string representation completely determines the view object, but for troubleshooting and debugging each view has a `detailed` property which explicitly states the entire contents.
We can see in the above that while `p1.to_str()` only presents the `stage` of `p1`, in fact `p1` has a supposition (with default value `{{}}`) as well as a dependency relation, issue structure, and a collection of weights (all empty by default).

The example here made use of the convention in *Reason & Inquiry* that the supposition part of a view consists of a single empty state.
The empty state in string representations is always notated `0`, as in the book, rather than `{}`.
Thus if one changes a line in the code above to
```py
p1 = View.from_str("{GrassWet()}^{0}")
```
we should see exactly the same output.

For a non-trivial supposition
```py
p1 = View.from_str("{GrassWet()}^{Raining()}")
print("The view is " + p1.to_str())
```
yields the following.
```
The view is {GrassWet()}^{Raining()}
```

## Quantifiers

Arbitrary objects are identified with quantifiers. These quantifiers are placed at the start of the expression, and may be:

* For all: A or ∀
* There exists: E or ∃

For instance, if there exists a plant that is wet if it is raining:

```py
{Ex IsWet(x)} ^ {Raining()}
```
or equivalently
```py
{∃x IsWet(x)} ^ {Raining()}
```
### Dependencies

You may be familiar with the concept of dependencies from the book - this translates using the ordering of quantifiers to establish the dependencies, as described in the book.

## Issue Structures

If you wish to notate an issue structure, this done slightly different than in the book, using a quantity referred to as "emphasis". Emphasis is used to make a particular term at issue, and is notated with a *.

For example, let's say the x in IsWet is at issue:

```py
{∃x IsWet(x*)} ^ {Raining()}
```


## Multiplicative Weights

## Additive Weights

## Term

```py
{∃x IsWet(bob(x)*)} ^ {Raining()}
```
## Custom Functions

!!! warning "Caveat for Readers of *Reason & Inquiry*"
    Custom function in the current implementation deviates.

## Special Functions

### Equality

### Xbar

### Summation

## Sample functions

### `div`

### `power`

### `log`