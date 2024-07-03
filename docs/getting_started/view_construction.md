# View construction

If you wish to create your own views, you'll need to be able to generate a string that specifies the view.

The notation we've used here tries to follow very closely to the notation used by the book.

Let's start simply:

```
{GrassWet()}
```

This view is simply a Stage that contains the constant "GrassWet".

Now let's add a supposition:

```
{GrassWet()} ^ {Raining()}
```
This specifies a view with a stage GrassWet() and supposition Raining().

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