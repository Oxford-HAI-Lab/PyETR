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

## Anatomy of a view

A view consists of four main parts.

- Stage
- Supposition
- Dependency Relation
- Issue Structure

For concreteness, let us study a view from [Example 56](case_index/e56_default_inference). Once you have set up PyETR you can inspect the provided examples as follows.
```
>>> from pyetr.cases import e56_default_inference
>>> v = e56_default_inference.v[1]
>>> print(v)
∀z ∃w {Student(z)Reads(z,w)Book(w)}^{Student(z)} issues=IssueStructure({(z, Student(?))}) deps=z{w}
```
!!! Todo
    The dependency is a bit confusing??

Here we have imported a view `v` from Example 56 of R&I.
The four main parts of the view are present as follows.

```
{Student(z)Reads(z,w)Book(w)}
```
is a rendering of the stage, and we can see it as the main logical content of the view `v`. It asserts a conjunction of atomic propositions corresponding to '`z` is a student', '`w` is a book', and '`z` reads `w`'.
Every view has a stage.

```
^{Student(z)}
```
is a rendering of the supposition, indicated with a `^` on the right of the stage. Suppositions are optional. The presence supposition indicates that belief in the stage is actually conditional on the truth of the supposition, in this case, the supposition indicates that the belief about all `z`'s reading a book is restricted to those `z`'s which are students.

The dependency relation is displayed in the parts
```
∀z ∃w ... deps=z{w}
```
The beginning of the dependency relation tells us which terms appearing in the view are *arbitrary objects*, and further more which are *universal arbitrary objects* (indicated by ∀, analogous to universally quantified bound variables) and which are *existential arbitrary objects* (indicated by ∃, analogous to existentially quantified bound variables). In ETR, existential arbitrary objects can *depend* on universal arbitrary objects. This is indicated by the last part: `z{w}` tells us that the set of existentials depending on the universal `z` consists of just `w`. In the case of the view `v`, the view refers to students universally and asserts the existence of a book that *depends* on that student. This distinguishes it from a view which asserts that there is at least one book that all students read. For convenience, the dependencies are also displayed in the initial part of the printout: by the fact that `∃w` is to the right of `∀z` we see that `w` depends on `z`.

The issue structure is displayed as
```
issues=IssueStructure({(z, Student(?))})
```
Issue structures are optional, and have no effect on the logical reading of a view. This issue structure tells us that "`z` is at issue for being a student". This has significance for several view operations whose implementation is guided by issue structures.


TODO: weights, multiple states, view operations, default reasoning.