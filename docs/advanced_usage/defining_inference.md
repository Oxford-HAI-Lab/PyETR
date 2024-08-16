# Custom inference operations

PyETR comes packaged with several inference procedures, but in this tutorial we'll demonstrate how to make your own. We can use python functions combined with the methods it provides to construct new inference procedures.

Let's suppose we have an operation that takes two views and does update, suppose, query:

```py
from pyetr import View

def new_inference(v1: View, v2: View):
    return v1.update(v2).suppose(v2).query(v2)
```

We can easily chain these operations together. To add verbose mode:

```py
from pyetr import View

def new_inference(v1: View, v2: View, verbose: bool = False):
    return v1.update(v2, verbose=verbose).suppose(v2, verbose=verbose).query(v2, verbose=verbose)
```

Now each operation follows the verbosity of the input boolean.

## A more complex case

Suppose we have a slightly more complex operation, where the first view in a tuple is to be updated and supposed by each following view:

Here, again we can use the python language feature of for loops to iteratively apply these operations:

```py
from pyetr import View

def complex_inference(views: list[View]):
    new_view = views[0]
    if len(views) == 1:
        return new_view
    for v in views[1:]:
        new_view = new_view.update(v).suppose(v)
    return new_view

v0 = View.from_str("{X()}")
v1 = View.from_str("{Y()}")
v2 = View.from_str("{Z()}")
v3 = complex_inference([v0,v1,v2])
print(v3.to_str()) # {X()Z()Y()}^{Z()Y()}
```

Python has the flexibility to express any combination of operations as desired, but hopefully this gives a good basis to begin learning more advanced language features.
