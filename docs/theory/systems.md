# Systems from *Reason & Inquiry*

On this page we recap the structure of the book *Reason & Inquiry* and explain how to relate its contents to PyETR.

## Four versions of the ETR system

*Reason & Inquiry* introduces four versions of ETR where the possible contents of views increase in sophistication.
We can label them by the number of the chapter that introduces each one and here we briefly summarize the characteristic features that each introduces.

- **Chapter 2:** views can express sentences of propositional logic.
- **Chapter 4:** adds terms and arbitrary objects; now views can express sentences of first-order logic.
- **Chapter 5:** states are now weighted, hence views can express reasoning under uncertainty.
- **Chapter 6:** states now have two weights (multiplicative and additive) each and can contain do-atoms, hence views can express decision-making (under uncertainty).

The richer view contents means that subsequent systems redefine named operations defined in earlier systems.
They also add new operations.

PyETR implements the Chapter 6 system, [with a few modifications](./differences.md). Since all of the other systems can be translated into the Chapter 6 one, this allows us to use PyETR to study examples written for any of the systems in R&I. In practice, this means there is occasionally a little notational overhead, most notable in [View Construction](../usage/view_construction.md).

## Translations between systems

Views in more primitive systems can be translated into the later systems.

- **Chapter 2 -> Chapter 4:** Treat Chapter 2 atoms as Chapter 4 atoms formed from nullary predicates, and leave the dependency relation and issue structure empty.

- **Chapter 4 -> Chapter 5:** Give each state in the stage the empty multiset $\llangle \rrangle$ as its weight.

- **Chapter 5 -> Chapter 6:** The existing weight of a state becomes its multiplicative weight and its additive weight becomes the empty multiset $\llangle \rrangle$.

These 'upwards' translations are designed to commute with view operations. Concretely, if we write the translation from Chapter $m$ views to Chapter $n$ views as $\uparrow_m^n$, then for any operation $O$ defined in Chapter $m$, firstly Chapter $n$ has an operation with the same name for example, and secondly if $G$ & $D$ are Chapter $m$ views then the following equation holds.

$$
\uparrow_m^n(G[D]^O) = (\uparrow_m^n G)[\uparrow_m^n D]^O
$$

See Theorem B.44 in R&I for the case of $\uparrow_4^5$.

It sometimes seems reasonable to consider 'downwards' translations as well. The step from 5 to 4 works well: we simply drop the weights from the states. We can go from 6 to 5 by forgetting the additive weights and possibly removing any do-atoms. There does not seem to be any feasible way to go from 4 to 2 that preserves a reasonable amount of content. Moreover, downwards translates should not be expected to commute with reasoning operations, see Theorem B.45 in R&I.

