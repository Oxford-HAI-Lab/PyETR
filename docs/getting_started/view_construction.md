# View construction

The basic way to create your own views is to specify them via a string representation which closely follows the notation used in *Reason & Inquiry*.
The same string representation is used for printing views as the results of calculations. [N.B. This isn't quite true, maybe we can make it true? Difference between `to_str` and `__str__`?]

For convenience, you only need to include in the string those parts of the view that are non-trivial or have non-default values.
Recall that *Reason & Inquiry* builds up to the full theory of views through iterative enrichments of the possible view contents.
Thus, by only relying on restricted kinds of content one can use PyETR for computations with any of the restricted theories of views in the earlier chapters of the book, even though PyETR is technically a single implementation of the full theory.
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
Observe that the basic method for creating a view from a string representation is the `from_str` method of the `View` class.
To turn a view object into a string, use `to_str` of that view object.

This string representation completely determines the view object, but for troubleshooting and debugging each view has a `detailed` property which explicitly states the entire contents.
We can see in the above that while `p1.to_str()` only presents the `stage` of `p1`, in fact `p1` has a supposition (with default value `{{}}`) as well as a dependency relation, issue structure, and a collection of weights (all empty by default).

## Stages, states, and simple atoms

Let us break down the following representation of view found in [Example 8](/case_index/#e8).
```
{k()t(),a()q()}
```

At the core of any view is a set of states.
In *Reason & Inquiry*, this is the element of a view typically denoted by &Gamma; (upper-case gamma).
In the code base for PyETR, this is called the `stage`.
A string representing a view must specify a stage between `{` and `}` as a comma-separated list of states.
Thus in the example above, the view specifies a stage with two states: `k()t()` and `a()q()`.

A state is a set of atoms.
It is specified in PyETR as a list of atoms *without any delimiters*.
Thus the two states in the example each consist of two atoms, one has `k()` and `t()` and the other has `a()` and `q()`.
All atoms in PyETR consist of a string of ordinary characters followed by (possibly empty) matching parentheses, thus the parsing of a string representing a state into a list of strings representing atoms is unambiguous, despite the lack of delimiters.

!!! info
    The empty state is written `0`.

Atoms written with an empty pair of parentheses correspond to the atoms in Chapter 2 of *Reason & Inquiry*, which act a like the literals of propositional logic.
In the book, the view from the example is written more like this:
```
{kt, aq}
```
For technical reasons we do not adopt this notation in PyETR.
Thus, when working in the propositional fragment of ETR, it is necessary to insert the empty parentheses as a suffix to the name of atoms.
This is mildly more cluttered than the notation used in Chapters 2 and 3 of *Reason & Inquiry*, but, on the other hand, the presence of parentheses assists in using names for atoms that are longer than a single character.

!!! info
    Note that the ordering of states in the stage, and of atoms within each state, are immaterial to the denoted view.
    Thus the view above could equally well be denoted as follows.
    ```
    {q()a(),t()k()}
    ```
    Indeed,
    ```py
    View.from_str("{k()t(),a()q()}") == View.from_str("{q()a(),t()k()}")
    ```
    will return `True`.

!!! warning
    Since the order is not meant to matter, the result of `to_str()` need not exactly match the input to `View.from_str`.
    The representation of View objects internal to PyETR and Python does require an arbitrary order to be imposed, but this can be quite unpredictable and might depend on your computing setup.
    For example, despite the equality above, you may find that
    ```py
    View.from_str("{k()t(),a()q()}").to_str() == View.from_str("{q()a(),t()k()}").to_str()
    ```
    returns `False`!
    PyETR overloads Python's equality test to give a more correct equality test for View objects.
    See TODO for further discussion of equality testing.

## Negation

An atom is made negative by prepending a tilde `~` to it.
This corresponds to the notation in *Reason & Inquiry* where the negative counterpart of a positive atom was denoted by the same letter with an overline.

For example, consider [Example 22](/case_index/#e22).
Starting with the view denoted
```
{a()c()b()}
```
which has a single state containing the three atoms `a()`, `b()`, and `c()`, its negation is computed to be the view denoted
```
{~c(),~b(),~a()}
```
which has three states, each containing a singleton negative atom.

## Suppositions

Suppositions are optional and are denoted with a `^` after the stage, using the same syntax for a set of states as for stages.
In *Reason & Inquiry*, suppositions were typically denoted by &Theta; (upper-case theta) and placed in superscript position following the stage.

For example, consider [Example 28](/case_index/#28).
There is a view denoted
```
{Tiger()Orange()}^{Tiger()}
```
Here, the stage is `{Tiger()Orange()}` consisting of one state with two atoms (`Tiger()` and `Orange()`).
The supposition is `{Tiger()}`, which consists of one state with one atom (just `Tiger()`).

!!! info
    Omitting the supposition is equivalent to a supposition of `{0}`.
    That is, unless otherwise specified, a view has as its supposition the singleton set consisting of the empty state.

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