# View construction

If you wish to create your own views, you'll need to be able to generate a string that specifies the view.

The notation we've used here tries to follow very closely to the notation used by the book.

Let's start simply:

```
{Fred()}
```

This view is simply a Stage that contains the constant "Fred".

Now let's add a supposition:

```
{Fred()} ^ {John()}
```
This specifies a view with a stage Fred() and supposition John().

