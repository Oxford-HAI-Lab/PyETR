# Overview

On this page we summarize the main points of the *Erotetic Theory of Reasoning* (ETR) as implemented in PyETR.

## Views

ETR is centred around the manipulation of objects called *views*.
Views are what a reasoner works with: the current focus of attention is a view, incoming information arrives packaged as a view or sequence of views, and latent beliefs are a collection of views.

Every view has an underlying truth-conditional content, equivalent to some sentence of first-order logic.
A view is more than this, as logically equivalent but distinct views are treated differently in the reasoning procedure hypothesized in ETR.
The extra content can be seen as 'inquisitiveness' about certain topics.

The central hypothesis of ETR is that the goal of reasoning is to resolve inquisitiveness.
Moreover, it is hypothesized that failures of reasoning, relative to formal standards of rationality, arise from this tendency and that failure can be averted by explicitly enforcing a certain amount of inquisitiveness.
