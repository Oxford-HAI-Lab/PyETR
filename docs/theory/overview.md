# Overview

On this page we summarize the main points of the *Erotetic Theory of Reasoning* (ETR) as implemented in PyETR.

## Views

ETR is centred around the manipulation of objects called *views*.
Views are what a reasoner works with: the current focus of attention is a view, incoming information arrives packaged as a view or sequence of views, and latent beliefs are a collection of views.

Every view has an underlying truth-conditional content, equivalent to some sentence of first-order logic.
However, a view is more than this, because logically equivalent but distinct views are treated differently in the reasoning procedure hypothesized in ETR.
The extra content can be seen as 'inquisitiveness' about certain topics.

The central hypothesis of ETR is that the goal of reasoning is to resolve inquisitiveness.
Moreover, it is hypothesized that failures of reasoning, relative to formal standards of rationality, arise from this tendency and that failure can be averted by explicitly enforcing a certain amount of inquisitiveness.

## Looking at a view

For concreteness, let us study a view from [Example 56](../reference/case_index.md#e56_default_inference). Once you have set up PyETR you can inspect the provided examples as follows.
```python
from pyetr.cases import e56_default_inference

v = e56_default_inference.v[1]
print(v) # ∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
```
Lines beginning `>>>` are user input and other lines are Python output.
Here we have imported one of the views from Example 56 of R&I and given it the name `v`.
Then asking Python for `v` causes a string representation of `v` to be printed.

!!! warning
    There are several formats that can be used for 'printing' views in PyETR. The default one is chosen for convenience of reading and writing, rather than a perfect match to the notation used in R&I.

!!! info
    Instead of importing the example, you could copy and paste any string given as an output like this
    ```python
    from pyetr import View

    v = View.from_str("∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}")
    print(v) # ∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
    ```

Asking Python to print `v` is equivalent to the following
```python
print(v.to_str()) # ∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
```
Aside from `to_str()`, another way to render a view is `base`.
```python
print(v.base) # {Student(z)Reads(z,w)Book(w)}^{Student(z)} issues={(z,Student(?))} U={z} E={w} deps=z{w}
```
This is provided to give a close match to the notation and theoretical structure of views provided in R&I. It should not be necessary to use `base` to follow calculations, as all relevant information is encoded in the `to_str()` representation, but it may be helpful for learning to connect the concrete `to_str()` syntax with the abstract structures of R&I.

## Anatomy of a view

A view consists of four main parts.

- Stage
- Supposition
- Dependency Relation
- Issue Structure

Let's see how these appear in the Python printout for our running example.

In `v.to_str()`, the stage and the supposition appear with the issue structure mixed in as
```
{Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
```
where the `^` separates the stage on the left from the supposition on the right.
(In R&I, the supposition is written as a superscript).
The asterisks encode the issue structure and are not technically part of the stage or structure.
This is made more clear with `v.base` where
```
{Student(z)Reads(z,w)Book(w)}^{Student(z)} issues={(z,Student(?))}
```
shows the stage and supposition in the same format but without asterisks, and the issue structure given separately.
The issue structure tells us that `z` is at issue for being a `Student`.

!!! info
    For this view, the issue structure contains only a single item, which is clear from `v.base` but less so from `v.to_str()`.
    This is because issues are not local to particular positions in the stage or supposition, but apply globally to a view.
    We will discuss this further in [TODO].
    This is one advantage to the more verbose `base` representation.

Finally, in `v.to_str()` the dependency relation is determined by the prefix
```
∀z ∃w
```
while for `v.base` it is determined by the suffix:
```
U={z} E={w} deps=z{w}
```

The `v.base` form tells us explicitly that the view contains the arbitrary objects `z` and `w`, with `z` being universal and `w` being existential.
In ETR, existential objects can depend on universals, and so the `deps` part tells us that the set of existentials depending on `z` is just the set `w`, i.e. that the only dependency is that of `w` on `z`.

The `to_str()` representation contains the same information in a condensed form.
We can see the ∀ (for all) and ∃ (there exists) quantifier symbols attached to each arbitrary object tell us whether they are universal or existential respectively.
The dependencies are encoded in the order that the variables are listed: because the existential `w` is to the right of the universal `z`, `w` must depend on `z`.

!!! info
    The dependency relations of ETR are in one-to-one correspondence with strings of first-order quantifiers *up to reordering of similar quantifiers*.
    This justifies the use of the quantifier string as a convenient notation for dependency relations.
    The key caveat is that in a chain of quantifiers of the same type, e.g. `∃a ∃b ∃c`, there is no significance at all to the ordering of `a`, `b`, and `c`: effectively an order is just chosen arbitrarily in order to print out a string.
    Another way to say this is that in first-order logic, permuting such strings of quantifiers preserves logical equivalence, but in ETR it actually preserves the equality class of the view.

## States and weights

In the example above, the stage appeared as sequence of three 'atoms': `Student(z)`, `Reads(z,w)`, `Book(w)`.
Intuitively, this is a conjunction ('and') of the three atomic propositions.
Really, a stage is a comma-separated set of *states*, each of which is a set of *atoms*.
Each state is intuitively a conjunction of its constituent atoms, and the stage is intuitively a disjunction ('or') of its constituent states.
The order of atoms within a state, and the order of states within the stage, have no significance.
Furthermore, each state in the stage can carry an optional 'multiplicative' weight and/or 'additive weight'.

Let us consider another example from [Example 69](../reference/case_index.md#e69_part1).
```python
from pyetr.cases import e69_part1

v2 = e69_part1.v[1]
print(v2) # {0.000001=* ~Guilty(Suspect())Match(Suspect()),~Guilty(Suspect())~Match(Suspect())}^{~Guilty(Suspect())}
```
Here the stage consists of two states (because there is one comma).
Each state consists of two atoms, but the first (in the arbitrary printed order) state has a multiplicative weight of `0.000001`, as indicated by the `0.000001=*` prefix.

The supposition of a view is also set of states, but states in a supposition do not carry weights.
Most commonly, the supposition consists of a single empty state, in which case we omit the supposition in notation.
Next most typically the supposition is a single state with a single atom, occasionally it is a single state with more than one atom, and only very rarely will it have a different number of states.

## Operations and inference procedures

Once we have a view, reasoning consists in changes to that view, possibly in light of new information.
In ETR, changes to the current view are effected by a basic set of *operations*, each of which acts on the current view in light of a second view.
The second view is sometimes either new or recalled information, though often it does not stand for its logical content.

View operations can be referenced in their own [index](../reference/view_methods.md).
As an example, perhaps the most useful operation is [update](../reference/view_methods.md#update), used as follows.
```python
from pyetr import View

v1 = View.from_str("{Man(Socrates()*)}")
v2 = View.from_str("Ax {Mortal(x)}^{Man(x*)}")
v1.update(v2) # {Mortal(Socrates())Man(Socrates()*)}
```

In ETR, the capacity for reasoning is constrained by the limited set of view operations, and the process of reasoning consists in following procedures that chain together these basic operations rather than apply single basic operations.
A few built-in inference procedures are listed in an [index](../reference/inference_index.md).
For example, the default inference procedure for "what if anything follows?" questions can be used as follows.
```python
from pyetr import View
from pyetr.inference import default_inference_procedure

v1 = View.from_str("{Man(Socrates()*)}")
v2 = View.from_str("Ax {Mortal(x)}^{Man(x*)}")
print(default_inference_procedure([v1,v2])) # {Mortal(Socrates())}
```
The `default_inference_procedure` internally uses the `update` operation, but chains it with other operations to produce a conclusion with only novel contents.
