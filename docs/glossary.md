# Glossary of operations and terms

## Multiset

A multiset is a collection of objects which is *unordered* and *possibly has repeats*, cf. [Set](#set)
In ETR multisets are represented as comma-separated lists between double-angle brackets, thus

\[
    \llangle 1,1,2 \rrangle = \llangle 1,2,1 \rrangle = \llangle 2,1,1 \rrangle
\]

are three ways of writing the same thing: the multiset containing two copies of the number $1$ and one copy of the number $2$.

In ETR, multisets are always finite and can be empty.

## Set

A set is a collection of objects which is *unordered* and *without repeats*, cf [Multiset](#multiset).
As is standard, sets are represented as comma-separated lists between curly brackets, thus

\[
    \{1,2\} = \{2,1\} = \{1,1,2\}
\]

are three (of many possible) ways of writing the same thing: the set whose members are $1$ and $2$ only (note that repeating a member in the description has no effect). However, note that a [State] is by definition a kind of set, but when a set is considered as a state we use a different notation (see that entry).

In PyETR, all sets are finite, so we usually write 'set' when we really mean 'finite set'. In ETR, all sets involved in the construction of a [View] are finite, but note that some entities, such as "the set of all views", are infinite sets.

## Stage

The main component of a view is the stage.
The stage is a set of [States]

## Update

Update is a view operation, the workhorse of reasoning. Written 

First View: Currently active point of view
Second View: Treated as a fact
Conclusion: New active point of view

Take a starting view, and when provided a new perspective produces a third view. (more details, reference glossary)

## View

A view is the basic object manipulated during reasoning. The current focus of a reasoner is taken to be a view. Incoming information arrives as a sequence of views, and latent beliefs are a collection of views. The different view operations correspond to different ways of evolving the current view in light of either new information or selected latent beliefs.

Views are built up from a [Stage], a [Supposition], a [Dependency Relation], and an [Issue Structure].

## Default Reasoning Procedure

The current expected way that a person processes a series of views

All operations take an initial view, and take on board a second view through the lens of the first, to produce a third view.



## Inquire

To pose a question on a starting view, where the question is represented as another view.

## Query

## Merge

Combine two views.

## Factor

