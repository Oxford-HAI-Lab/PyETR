# Getting started with python

For users unfamiliar with Python, there do exist many guides online including [this](https://docs.python.org/3/tutorial/interpreter.html) from the developers of Python. However, as a quick intro we'll show how to get started in a couple of basic ways:

## Running an interactive shell

Let's assume you've already [installed the package and Python](./installation.md). To initiate an interactive shell, you'll need to first open a terminal. Next simply type:

```
python
```
Depending on your exact installation you may need to instead type `python3` or perhaps even `python3.11` or `python3.12`, but for the purposes of this tutorial we'll assume the above.

This opens a shell like so:

```python
>>>
```
You can try something simple like:

```python
>>> print("Hello world!")
```

Or even:

```python
>>> from pyetr import View
```
To test that pyetr has installed correctly. This has full flexibility to allow you can type commands and test features, but a lot of the time you'll find it easier to work inside a script.


## Running a script

First make a file somewhere in your OS:

```
test.py
```

Inside this file, place whatever commands you desire, like:

```python
print("Hello world!")
```

To run the script now just use:

```
python test.py
```
(Assuming you're in the same directory as the file)

That's really all there is to it! However, it may be that you might want some more advanced controls over your files. For this I would recommend using the IDE [VS Code](https://code.visualstudio.com/).

## Setting up an IDE

First you need to download VSCode. This can be done [here](https://code.visualstudio.com/).

Next, open a folder you wish to use for development. 

Make a new file with `File -> New File`, and title this `test.py`.

Now open a terminal with `Terminal -> New Terminal`, and run the script as shown above. Running inside the IDE allows you to add extensions for spellcheck and type completion (I recommend installing Pylance). This will accelerate your development.
