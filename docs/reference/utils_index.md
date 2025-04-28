# Utilities Index

Below you'll find all of the utilities in pyetr.utils. You can use this page as an index of the available utilities.

## `views_to_smt_lib`
[Link to code](https://github.com/Oxford-HAI-Lab/PyETR/blob/master/pyetr/utils.py#L103)


```
Convert multiple views into a single smt lib string.

Args:
    views (list[View]): A list of views to convert.
    env (typing.Optional[Environment], optional): The pysmt environment to embed
        parsed variables. If None will use a fresh environment to avoid clashes.
        Defaults to None.

Returns:
    str: The smt lib string containing multiple views.
```

## `smt_lib_to_views`
[Link to code](https://github.com/Oxford-HAI-Lab/PyETR/blob/master/pyetr/utils.py#L12)


```
Convert one smt lib string containing multiple Views into a series of Views.

Args:
    smt_lib (str): The smt lib string
    custom_functions (Optional[list[NumFunc  |  Function]], optional): Custom functions used in the
        string. It assumes the name of the function is that used in the string. Useful
        for using func callers. Defaults to None.

Returns:
    list[View]: The list of views found in the smt lib string.
```