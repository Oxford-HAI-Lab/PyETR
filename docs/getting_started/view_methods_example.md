# View methods example

First let's take two views:

* View 1: {t()=+ A()}

* View 2: {u()=* A()}

Suppose we would like to update View 1 with View 2. First we create Views from each string:

```py
from pyetr import View

view1 = View.from_str("{t()=+ A()}")
view2 = View.from_str("{u()=* A()}")
```

Now we can use the update method from view1 to update with view2:

```python
updated_view = view1.update(view2)
print(updated_view.to_str()) # {u()=* t()=+ A()}
```

## Full example

```python
from pyetr import View

view1 = View.from_str("{t()=+ A()}")
view2 = View.from_str("{u()=* A()}")

updated_view = view1.update(view2)
print(updated_view.to_str()) # {u()=* t()=+ A()}
```