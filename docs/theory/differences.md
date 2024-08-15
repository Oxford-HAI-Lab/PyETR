# Differences with *Reason & Inquiry*

On this page we list the most significant differences between the Chapter 6 system of *Reason & Inquiry* and the system implemented by PyETR.

## Notation

There are a few superficial notational differences worth summarizing.

+ Dependency relations in PyETR are mainly notated with quantifier strings, whereas the notation in R&I is more analogous to the `.base` representation of a view.
+ Issues in PyETR are notated with an asterisk `*`, instead of a circumflex as in R&I.
+ Names of constants in PyETR normally need to be input with empty brackets, e.g. `John()` and rather than `John`. Similarly, primitive propositions (nullary predicates) need empty brackets too, e.g. `IsRaining()` rather than `IsRaining`.
+ The special $=$ binary predicate symbol from R&I Chapter 4 onwards is notated with a double equal sign `==`. It appears as prefix, just like any other predicate, e.g. `==(Clark(),Superman())`.
+ The notation for multisets is a bit different, see [View construction]() for weights and just below for $\sigma$.
+ The special $\overline\times$ binary function symbol from R&I Chapter 5 onwards is notated with a double asterisk `**` in PyETR. It can be used either prefix or infix, e.g. both `**(2,x)` and `2 ** x` are valid and denote the same term. See also [Collapsing functions](#collapsing-functions).
+ The special $\sigma$ function symbol from R&I Chapter 5 onwards is notated either `++` (for convenient typing) or `σ`. It is used as a prefix on a comma-separated list of arguments inside round brackets, e.g. `++(1,1,x)`. Any number of items can appear in the argument list, which is interpreted as a multiset. See also [Collapsing functions](#collapsing-functions).
+ Real numbers were introduced as terms in R&I Chapter 5. In PyETR, terms that should be real numbers are inferred automatically from their name TODO.
+ TODO Do atoms are notated with a comma-separated list.

## Commitments

PyETR does not currently work with any notion of commitment.
Some of the operations and procedures in R&I were directed by a set of *commitments*, i.e. a background set of views held like beliefs, in PyETR we currently rely on the users to implement their own 'set of commitments'.
For most purposes this is not an issue, and it has almost no effect on the case studies.

It does have a small significance for novelization, which is performed at a more local level than was envisaged in R&I.
For example, in R&I, the second argument of an update was expected to be use arbitrary objects which are novel for the entire set of arbitrary objects seen so far, whereas in PyETR [Update]() is hard-coded to perform novelization by itself, and only relative to its first argument.
The PyETR behaviour should be more convenient.

## Collapsing functions

In R&I all function symbols were considered to be completely static.
While certain operations formed new term expressions out of binary multiplication $\overline\times$ and multiset-sum $\sigma$, these expressions were considered to be left unevaluated.
At the points where a final value was required, it was assumed that some procedure was given for evaluating the term, with the exact nature left open.

In PyETR, functional terms can be more dynamic. Two built-in function symbols, `**` and `++`/`σ`, will attempt to simplify themselves as soon as they are instantiated.
For example, when parsing, the term `2 ** 3` is automatically replaced with `6` and the term `++(1,1,3)` is automatically replaced with `5`.

The simplification for `**` and `++` only happens when both/all arguments are real numbers.
However, it does not only happen at parse time.
Suppose a view contains a term such as `x ** 3` where `x` is an arbitrary object.
Then, if in the process of computing an operation a real number term is substituted for `x`, the output view will have the corresponding substitution instances of `x ** 3` simplified already.

The advantage of the approach taken in PyETR is that operations such as [Answer](../view_methods.md#answer) can operate without any intervention to simplify arithmetic expressions.
The main caveat is that sometimes issue items can unexpectedly disappear.
For example, the view `{ A(2 ** (3*)) }` is parsed equally to `{ A(6) }`, despite the attempt to include a non-trivial issue structure in the first view.
The reason is that, after simplifying `2 ** 3` to `6`, there is no longer identifiably an atom `A(2 ** ?)` with `3` in `?`-position.
This does not affect any of the case studies from R&I.

## Do atoms

In R&I Chapter 6, the interaction of do atoms and issue structures was left imprecise.
In PyETR, the issue context of a term only extends to the first atom containing it, and does not include a `do`.
For example, consider parsing the string `∀x { do( A(x*) B() ) }`.
```
>>> from pyetr import View
>>> v = View.from_str("∀x { do(A(x*),B()) }")
>>> print(v.base)
{do(B(),A(x))}^{0} issues={(x,A(?))} U={x} E={}
```
Note that resulting issue structure contains `(x,A(?))`, rather than `(x,do(A(?)B()))`.
