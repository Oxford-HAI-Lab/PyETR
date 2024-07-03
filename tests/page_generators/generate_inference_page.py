import pyetr.inference

out = []
for name, func in vars(pyetr.inference).items():
    if name in pyetr.inference.__all__:
        if func.__doc__ is not None:
            new_doc = func.__doc__
        else:
            new_doc = ""
        out.append("`" + name + "`" + "\n```\n" + new_doc + "\n```")

with open("../../docs/inference_index.md", "w+") as f:
    intro = "# Inference Index\n\nBelow you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.\n\n## "
    full_page = intro + "\n\n## ".join(out)
    f.write(full_page)
