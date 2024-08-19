# View construction

This page is a comprehensive guide to building your own views via the `View.from_str()` method.

It will also serve to make more precise the [anatomy of a view](../getting_started/overview.md#anatomy-of-a-view) summarized earlier.

The `View.from_str()` is the basic way that views are created in the [case studies](../reference/case_index.md) and how we expect most users will input their own views.
The syntax required broadly follows the notation used in *Reason & Inquiry*.
The same syntax is the default format for printing views (the other formats were mentioned in the [overview](../getting_started/overview.md)).

You can explicitly convert to this string format with `.to_str()`.

!!! info
    Since views are completely determined by the string representation, the following boolean test should always return `True` for any view `v`.
    ```
    v == View.from_str(v.to_str())
    ```
    See [here](../advanced_usage/view_equality_and_equivalence.md) for details about equality. However, you should not expect
    ```
    View.from_str("...").to_str()
    ```
    to return an equal string.
    One reason is because printing to a string requires us to impose a linear order on the unordered components of a view.
    Another reason is that there are multiple ways to notate some features.
    Typically, where there is a 'pretty' notation used for printing that is less convenient to type, an alternative notation is provided.
    For example, `∀` is used in printing but for convenience `A` can be typed instead, see [Dependency relations](#dependency-relations).



For convenience, you only need to include in the string those parts of the view that are non-trivial or have non-default values.
This helps when using PyETR for the earlier [systems](../theory/systems.md) of *R&I*, even though PyETR implements the full Chapter 6 system, as you will never have views cluttered with default values for the irrelevant components.
There are a few notational caveats which will become apparent below (also summarized in [Differences with R&I](../theory/differences.md)).

## Basic example

As an example, consider running the following code.
This code might also be useful as a template for testing out features detailed below.
```py
from pyetr import View

p1 = View.from_str("{GrassWet()}")
print("The view is " + p1.to_str())
print("Slightly elaborated: " + p1.base)
print("\nIn detail:")
print(p1.detailed)
print("\nNB 'to_str()' is implicit if we print a view by itself:")
print(p1)
```
The output should be
```
The view is {GrassWet()}
Slightly elaborated: {GrassWet()}^{0}

In detail:
<View
  stage={{<PredicateAtom predicate=<Predicate name=GrassWet arity=0> terms=()>}}
  supposition={{}}
  dep_rel=<DependencyRelation deps=[] unis=frozenset() exis=frozenset()>
  issue_structure={}
  weights=<Weights {<PredicateAtom predicate=<Predicate name=GrassWet arity=0> terms=()>}: <Weight multi=<Multiset items=[]> add=<Multiset items=[]>>>
>

NB 'to_str()' is implicit if we print a view by itself:
{GrassWet()}
```
Observe that the basic method for creating a view from a string representation is the `from_str` method of the `View` class.
To turn a view object into a string, use `to_str` of that view object.

This string representation completely determines the view object, but for troubleshooting and debugging each view has a `detailed` property which explicitly states the entire contents.
We can see in the above that while `p1.to_str()` only presents the `stage` of `p1`, in fact `p1` has a supposition (with default value `{{}}`) as well as a dependency relation, issue structure, and a collection of weights (all empty by default).
The `base` property is provided in case it is useful for troubleshooting and also for its slightly closer connection with the notation used in *R&I*.

**Unless specified otherwise, we'll be using the `to_str()` representation as the default.**

## Stages and states

Let us break down the following representation of view found in [Example 8](../reference/case_index.md#e8).
```
{k()t(),a()q()}
```

At the core of any view is a set of states.
In *Reason & Inquiry*, this is the element of a view typically denoted by Γ (upper-case gamma).
In the code base for PyETR, this is called the `stage`.
A string representing a view must specify a stage between `{` and `}` as a comma-separated list of states.
Thus in the example above, the view specifies a stage with two states: `k()t()` and `a()q()`.

A state is a set of atoms.
It is specified in PyETR as a list of atoms *without any delimiters*.
Thus the two states in the example each consist of two atoms, one has `k()` and `t()` and the other has `a()` and `q()`.
We will describe [atoms](#atoms) below, but for now note that all atoms in PyETR consist of a string of ordinary characters followed by (possibly empty) matching parentheses.
Thus the parsing of a string representing a state into a list of strings representing atoms is unambiguous, despite the lack of delimiters.

!!! info
    The empty state is written `0`.



## Negation

An atom is made negative by prepending a tilde `~` to it.
This corresponds to the notation in *Reason & Inquiry* where the negative counterpart of a positive atom was denoted by the same letter with an overline.

For example, consider [Example 22](../reference/case_index.md#e22).
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
In *Reason & Inquiry*, suppositions were typically denoted by Θ (upper-case theta) and placed in superscript position following the stage.

For example, consider [Example 28](../reference/case_index.md#e28).
There is a view denoted
```
{Tiger()Orange()}^{Tiger()}
```
Here, the stage is `{Tiger()Orange()}` consisting of one state with two atoms (`Tiger()` and `Orange()`).
The supposition is `{Tiger()}`, which consists of one state with one atom (just `Tiger()`).

!!! info
    Omitting the supposition is equivalent to a supposition of `{0}`.
    That is, unless otherwise specified, a view has as its supposition the singleton set consisting of the empty state.

## Atoms

Atoms are formed by applying a predicate to a (possibly empty) list of terms.
Consider this view from [Example 50](../reference/case_index.md#e50_part1).
```
{L(j(),s())L(s(),g())}
```
This stage has a single state containing two atoms.
For both atoms, `L` is read as a predicate applied to two terms, given as a comma-separated list inside the brackets following the name of the predicate.
The `j()`, `s()`, and `g()` are examples of terms, we will see more examples as we continue.


Atoms and terms can look similar.
In the above, the parser infers that `j()` is a term rather than an atom because it appears inside the brackets associated to an atom.
Any item at the top-level of a state must be an atom.


!!! warning
    `do` is a reserved name and should not be used for predicates.
    See [Do atoms](#do-atoms).

### Equality Atoms
In *Reason & Inquiry*, there is a privileged binary equality predicate which gets special treatment by some operations.

We'll use one of the views from [Example 88](../reference/case_index.md#e88) to demonstrate:
```
{==(Clark(), Superman())}
```
The above statement is the same as "Clark is superman", we see the equates the ideas of Clark and Superman. It's defined in the usual way for a function, using `==` as the function name.


### Propositional Atoms
As in the example from [Stages and states](#stages-and-states), in *Reason & Inquiry*, the view from the example is written something like this:
```
{kt, aq}
```
For technical reasons we do not adopt this notation in PyETR.
Thus, when working in the propositional fragment of ETR, it is necessary to insert the empty parentheses as a suffix to the name of atoms.
This is mildly more cluttered than the notation used in Chapters 2 and 3 of *Reason & Inquiry*, but, on the other hand, the presence of parentheses assists in using names for atoms that are longer than a single character.

This is why examples such as [Example 8](../reference/case_index.md#e8) have extra parentheses in PyETR relative to *Reason & Inquiry*.


## Terms

A representation of a term takes one of three possible forms.

#### Functional terms

This is a string of ordinary characters followed by parentheses containing a (possibly empty) comma-separated list of other term-representing strings.

A function taking a empty list of arguments is essentially the same as a constant.
Thus these functional terms are used to stand for the names of individuals, as in `Clark()` and `Superman()` above, as well as `j()`, `s()`, and `g()` ('John', 'Sally', and 'George').

Compound terms where functions take one or more arguments most often appear in mathematical expressions.
For example, in [Example 93](e93_grp1) the follow term appears, which is formed by applying the function `power` to a list of two other terms.
```
power(σ(1.0,log(σ(1.0,x))),-1.0)
```

!!! warning
    In PyETR, there are a few reserved function names, see [Special functions](#special-functions).
    Moreover, the behaviour of `σ` mildly differs from *Reason & Inquiry*, see [Collapsing functions](../theory/differences.md#collapsing-functions).

#### Real numbers


Integers and decimals such as `1`, `1.0`, `-1.0`. These are constants (0 arity functional terms), but notably do not use the open-close bracket syntax. See [here](../advanced_usage/func_callers.md) for details of how they interact with numeric functions.


#### Arbitrary objects

In PyETR, a string of ordinary characters *not* followed by parentheses is an arbitrary object.
These can only appear if there is a suitable [dependency relation](#dependency-relations).

!!! warning
    Names can be reused between functional terms and arbitrary objects, e.g. `x()` and `x` are completely independent terms.
    Moreover, functions can appear several times with different arities, and are considered to be different functions (and thus form necessarily different terms).

## Issue structures

Issue structures are specified inserting asterisks immediately after a term which is at issue for its environment.
This applies to terms appearing in states of the stage or supposition, (but not in [weights](#weights))
For example, in [Example 47](../reference/case_index.md#e47), the view
```
{Thermotogum(Maritima()*)}
```
has the (functional) term `Maritima()` at issue for the context `Thermotogum(?)`.

!!! info
    The issue structures in PyETR follow exactly the description given in Definition 4.7/A.29 in *Reason & Inquiry* and the informal use of the circumflex in the book agrees with the asterisk here. For more information about issue structures we recommend taking a look at this.

    See [Differences with R&I](../theory/differences.md#do-atoms-and-issue-structures), for a discussion on how [Do atoms](#do-atoms) interact with issues.

### Issue Contexts
For users unfamiliar with issue structures from *R&I*, the following is a likely source of initial confusion.
The following strings all represent the same view.
```
{A(a()*),A(a())B(b())}
{A(a()),A(a()*)B(b())}
{A(a()*),A(a()*)B(b())}
```
Converting any of them to string with `to_str()` will give the representation with two asterisks (i.e. the third one up to reordering).

This is expected behaviour.
The reason is that any of these asterisks informs PyETR that `a()` is at issue for the environment `A(?)`, and being at issue is a global property of the view *not* of the individual instances of `A(a())`.
Thus it is not meaningful for some 'instances' of `A(a())` to have `a()` at issue and not others.
When converting to string, all instances of `A(a())` are decorated with an asterisk as a canonical choice.

This may be clearest if you print this in `v.base` mode like so:
```py
from pyetr import View

print(View.from_str("{A(a()*),A(a())B(b())}").base) # {A(a),B(b)A(a)}^{0} issues={(a,A(?))}
print(View.from_str("{A(a()),A(a()*)B(b())}").base) # {A(a),A(a)B(b)}^{0} issues={(a,A(?))}
print(View.from_str("{A(a()*),A(a()*)B(b())}").base) # {A(a),A(a)B(b)}^{0} issues={(a,A(?))}
```

## Dependency relations

Dependency relations are specified by giving an equivalent string of quantifiers from first-order logic.
For example, consider the following view from [Example 56](../reference/case_index.md#e56_default_inference).
```
∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
```
Here, `z` and `w` are arbitrary objects.
The prefix `∀z ∃w` specifies that `z` is a universal arbitrary object and that `w` is an existential arbitrary object, and moreover that `w` has a dependence on `z`.
Alternatively, a prefix of `∃w ∀z` would import a lack of dependence of `w` on `z`.


!!! warning
    The set of arbitrary objects that appear in the quantifier string must precisely match the set of arbitrary objects that appear in either the stage or supposition of the view.
    This is just as in *Reason & Inquiry*.
    If it is not the case, an error will be raised.


### Alternative syntax

For convenience when typing, one can use `A` and `E` as synonyms for `∀` and `∃` respectively.
So the above is equivalent to the following.
```
Az Ew {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
```


### Equality of dependency relations

The quantifier string corresponding to a dependency relation is unique up to reordering of within homogeneous quantifier blocks.
Thus the following prints `True`.
```py
p1 = View.from_str("∀x ∀y {A(x),B(y)}")
p2 = View.from_str("∀y ∀x {A(x),B(y)}")
print(p1 == p2)
```

## Weights

Weights are an optional prefix to each state in the stage.
For example, consider the following view appearing in [Example 65](../reference/case_index.md#e65).
```
∀x {0.3=* P(x*)C(x),P(x*)~C(x)}^{P(x*)},
```
This a view with two states where the state `P(x)C(x)` is assigned a multiplicative weight `0.3`.

Each state has a *multiplicative* and an *additive* weight, introduced with `=*` and `=+` respectively.
Both are optional.
The `=*` should not be confused with the `*` for introducing items to the issue structure.


!!! abstract "Note for readers of *Reason and Inquiry*"

    Note that the `base` representation of this view uses a notation for weights which is more familiar from *R&I*.
    ```
    {⟪1.0,1.0,2.25⟫×.⟪7.0⟫+.A(),⟪1.0⟫+.B(),C()}^{0}
    ```
    PyETR implements the double-weighted states of Chapter 6 of *Reason & Inquiry*.
    To work with the single-weighted states of Chapter 5, only use the multiplicative weight `=*` and leave the additive weight `=+` empty.

    Definition 5.4 of *Reason & Inquiry* introduces a special binary function symbol for multiplication, used when combining two multiplicatively-weighted states.
    See [XBar](#xbar) for how to input it, and see [Collapsing functions](../theory/differences.md#collapsing-functions).


### Multiset Weights

Each weight is a multiset of terms, written as a list with the pipe `|` as delimiter.
(A multiset is a set allowing repeated elements).
For example,
```
{ 1.0|1.0|2.25=* 7.0=+ A(), 1=+ B(), C() }
```
represents a view where the state `A()` has for its multiplicative weight a multiset of size 3 and for its additive weight a multiset of size 1.
The multiplicative weight of `B()`, and both weights of `C()`, are the empty multiset, the unique multiset of size 0.
The example could also be written with explicit empty multisets as follows.
```
{ 1.0|1.0|2.25=* 7.0=+ A(), =* 1=+ B(), =* =+ C() }
```

### Ordering
Following the conventions of *Reason & Inquiry*, the multiplicative weight is always given first.
For example,
```
{ 1.0=* 3.1=+ A()B() }
```
is valid but
```
{ 3.1=+ 1.0=* A()B() }
```
will raise an error.


## Do atoms

Further to the predicate atoms discussed above at [Atoms](#atoms), do atoms are formed by using `do` like a predicate.

For example, the following appears in [Example 90](../reference/case_index.md#e90_conda).
```
{do(Buy(Video()*)),~do(Buy(Video()))}
```

The first state consists of a single atom, a positive do atom whose contents is `Buy(Video())`.

Moreover, `Video()` is at issue for the matter of `do(Buy(?))`.
The second state is a negative `do`-atom, simply the negation of the first.
(Note that `Video()` is not at issue for `~do(Buy(?))`).


The content of a do atom can be any state, even empty (denoted by empty brackets)

For example, the following is a valid view.
```
∀x { do(P(x)Q(x)R()), do(), do(P(x))do(Q(x)) }
```


!!! abstract "Note for readers of *Reason and Inquiry*"
    In *Reason & Inquiry*, 'do' could not appear inside the contents of a do-atom.
    PyETR does not currently enforce this, but behaviour when nested `do`-atoms might be unpredictable.

## Numeric Functions

There are are number of numeric functions available in PyETR. It's also possible to define your own custom functions, but for details of this please see the [advanced section](../advanced_usage/func_callers.md).

## Special Functions

Below are the details for each of the built-in numeric functions, that each have their own syntaxes for view construction.

### Xbar

Xbar is numeric multiplication, receiving 2 arguments. There are a couple of different ways to express this function. It may be represented using `**` or `x̄`; for the purposes of demonstration we'll use `**`.

As demonstrated in [Example 74](../reference/case_index.md#e74), it can be used to simply represent a numeric multiplication like so:

```
{A(4**5)} # Resolving to {A(20.0)}
```
If preferred it can also be written using the prefix notation:
```
{A(**(4,5))} # Resolving to {A(20.0)}
```

It is also used in the Non-Book example [New Example 18](../reference/case_index.md#new_e18):

```
{m()=* A()}
{n()=* B()}

# And the result after an update operation:
{m() ** n()=* A() B()}
```

Here we see that multiplication can also result from internal operations.

### Summation

Summation is numeric summation, receiving a [Multiset](../glossary.md#multiset) of arguments. It may be represented using `++` or `σ`; for the purposes of demonstration we'll use `++`.

This is used internally, and in part of [Example 93](../reference/case_index.md#e93_grp1).

```
Ax {++(1, log(++(1, x)))=+ 0} ^ {S(x*)}
```

Here this is used to represent the term: 1+log(1+x)

The summation may contain zero or more arguments.

## Sample functions

Sample functions can be imported from the func_library namespace. These represent some simple example numeric functions - below is a short example detailing usage with the div function:

```py
from pyetr import View
from pyetr.func_library import div


print(View.from_str("{A(div(100,3))}", custom_functions=[div]))
```
### `div`

A function representing divide (takes 2 arguments, numerator and denominator)

### `power`

A function representing power (takes 2 arguments, base and power)

### `log`

A function representing log base 10 (takes 1 argument)
