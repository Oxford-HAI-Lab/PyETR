# Custom Function Behaviour

As discussed [here](./getting_started/view_construction.md#numeric-functions) it's possible in PyETR to define and use numerical functions that combine real number terms in a variety of ways. In this section we'll discuss an advanced variant of this, wherein users may define their own custom functions.

## A 3 Argument Function

Below is a demonstration of a simple custom function, applied to three numeric arguments:
```py
from pyetr import View

def someOp(x: float, y: float, z: float) -> float:
    return (x * y) // z

v1 = View.from_str("{A(someOp(3,4,5))}", custom_functions=[someOp])
print(v1) # {A(2.0)}
```
Here we see the above operation has been applied to the terms given.

## When resolution occurs

If an operation leads to a substitution of one term for a numeric term, this will also lead to a numeric calculation. In the below example, we see how the arbitrary object `x` in `v2` in replaced by the `5` from `v1`, and this in turn causes the function to be calculated:

```py
from pyetr import View
from pyetr.inference import default_inference_procedure

def someOp(x: float, y: float, z: float) -> float:
    return (x * y) // z

v1 = View.from_str("{A(5*)}", custom_functions=[someOp])
v2 = View.from_str("∀x {B(someOp(3,4,x))}^{A(x*)}", custom_functions=[someOp])

print(v1) # {A(5.0*)}
print(v2) # ∀x {B(someOp(3.0,4.0,x))}^{A(x*)}
print(default_inference_procedure((v1,v2))) # {B(2.0)}
```

## Multiset functions

You may have noticed that one of the predefined functions, Summation, does not in fact receive a fixed number of arguments as I have described above. This is because there exists another type of function, that receives a [Multiset](./glossary.md#multiset) of items instead of a fixed arity tuple.

To do this, we must use the "Var Positional" or `*args` kind of function argument. In the below example we create the operation "product", that as with Summation receives an unlimited number of arguments:

```py
from pyetr import View
from pyetr.inference import default_inference_procedure

def product(*x: float) -> float:
    v: float = 1
    for i in x:
        v *= i
    return v

v1 = View.from_str("{A(5*)}", custom_functions=[product])
v2 = View.from_str("∀x {B(product(3,4,x))}^{A(x*)}", custom_functions=[product])
print(v1) # {A(5.0*)}
print(v2) # ∀x {B(product(3.0,4.0,x))}^{A(x*)}
print(default_inference_procedure((v1,v2))) # {B(60.0)}
```

## Alternative Syntax & Name Overrides

The above syntax assumes that the name of the function matches the name used in the string. It's possible that you may wish to use a different name in the view string, than in the function itself. For this we present an alternative syntax, that creates the Function class more directly. In the below example, the function name contains an underscore (a disallowed character in the view string), and the desired name of the function in the view string is also quite short:

```py
from pyetr import View, Function

def some_op(x: float, y: float, z: float) -> float:
    return (x * y) // z

v1 = View.from_str("{A(f(3,4,5))}", custom_functions=[Function.numeric(some_op, name_override='f')])
print(v1) # {A(2.0)}
```

## Overlapping Names (Danger!)

This section is more of a health hazard - the custom function syntax allows for many input types, and where possible we've tried to add errors where inconsistent usage occurs, but it occurred to me there are still some things to be aware of.

Consider the below example:

```py
from pyetr import View, Function

def some_op(x: float, y: float, z: float) -> float:
    return (x * y) // z

v1 = View.from_str("∀x {A(f(3,4,x))}", custom_functions=[Function.numeric(some_op, name_override='f')])
print(v1) # ∀x {A(f(3.0,4.0,x))}

def some_new_op(x: float, y: float) -> float:
    return x * y

v2 = View.from_str("∀x {A(f(3,x))}", custom_functions=[Function.numeric(some_new_op, name_override='f')])
print(v2) # ∀x {A(f(3.0,x))
```

So far so good right? We have two independent views that aren't interacting with different arity functions.

!!! danger
    Do not do this. It's not funny and it's not clever.

As far as the package is concerned it will accept this as the two definitions are mutually exclusive, but this is not recommended as it's extremely confusing readability wise, particularly if these views are later combined:
```py
print(v1.update(v2)) # ∀x ∀a {A(f(3.0,a))A(f(3.0,4.0,x))}
```

### Well, but they aren't exactly overlapping definitions right?

Sure, in the above case the definitions don't overlap as the functions have different arities. However, if we instead consider a case where they have the same arity:

```py
from pyetr import View, Function

def some_op(x: float, y: float) -> float:
    return x * y

v1 = View.from_str("∀x {A(f(3,x))}", custom_functions=[Function.numeric(some_op, name_override='f')])
print(v1) # ∀x {A(f(3.0,4.0,x))}

def some_new_op(x: float, y: float) -> float:
    return x // y

v2 = View.from_str("∀x {A(f(3,x))}", custom_functions=[Function.numeric(some_new_op, name_override='f')])
print(v2) # ∀x {A(f(3.0,x))
```

And now if we combine the two:
```py
print(v1.update(v2)) # ∀x ∀a {A(f(3.0,x))A(f(3.0,a))}
```
We now have no idea which f corresponds to which function - simply put in general it's really worth using different names.

!!! Note
    These kind of overlaps can also cause issues if one definition of the function uses a multiset function.
