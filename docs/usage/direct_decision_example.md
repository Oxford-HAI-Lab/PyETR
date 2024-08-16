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

## Step 1: Import package and operation

```python
from pyetr import View
from pyetr.inference import default_decision
```

## Step 2: Define the views for the operation

First we must define the view representing the decision to be made, in this case this view has two states, buying the video or not buying the video:
```python
v = View.from_str("{do(Buy(Video()*)),~do(Buy(Video()))}")
```
Next we define the view representing the consequence of making the decision, in this case "For all x, fun is the result if buy x":
```python
cv = View.from_str("Ax {Fun()}^{do(Buy(x*))}")
```
The last view to define represents the priority views. This view simply applies an additive weight to "Fun", such that "Fun" becomes a priority:
```python
pr = View.from_str("{1=+ 0} ^ {Fun()}")
```

## Step 3: Calculate the decision
Finally, we put all of these views into the decision calculation:
```python
result = default_decision(dq=v, cv=[cv], pr=[pr])
print(result) # {do(Buy(Video()*))}
```

## Full Example
```python
from pyetr import View
from pyetr.inference import default_decision

v = View.from_str("{do(Buy(Video()*)),~do(Buy(Video()))}")
cv = View.from_str("Ax {Fun()}^{do(Buy(x*))}")
pr = View.from_str("{1=+ 0} ^ {Fun()}")

result = default_decision(dq=v, cv=[cv], pr=[pr])
print(result) # {do(Buy(Video()*))}
```
