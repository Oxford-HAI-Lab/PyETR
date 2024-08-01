# Direct Decision

We'll be using example 90 (part i) from page 249 of the book.

    Example 90, p249, p273

    Imagine that you have been saving some extra money on the side to make some purchases,
    and on your most recent visit to the video store you come across a special sale of a new
    video. This video is one with your favourite actor or actress, and your favourite type of
    movie (such as a comedy, drama, thriller etc.). This particular video that you are considering
    is one you have been thinking about buying a long time. It is a available at a special sale price
    of $14.99. What would you do in this situation?


Let's go through what this case does if we were to do the operation manually.

## Step 1: Import package
```python
from pyetr import View, default_inference_procedure

v = View.from_str("{do(Buy(Video()*)),~do(Buy(Video()))}")
cv = View.from_str("Ax {Fun()}^{do(Buy(x*))}")
pr = View.from_str("{1=+ 0} ^ {Fun()}")

result = default_decision(dq=v, cv=[cv], pr=[pr], verbose=verbose)


if not result.is_equivalent_under_arb_sub(cls.c):
    raise RuntimeError(f"Expected: {cls.c} but received {result}")

c = View.from_str("{do(Buy(Video()*))}")


```
Import the parsing object