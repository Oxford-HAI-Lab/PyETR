import inspect

import pyetr.inference


def get_line_no(item):
    if item:
        # Get the source file and line number
        _, start_line_number = inspect.getsourcelines(item)
        url_prefix = (
            "https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L"
        )
        return f"\n[Link to code]({url_prefix}{start_line_number})\n\n"
    else:
        return ""


def main():
    out = []
    for name, func in vars(pyetr.inference).items():
        if name in pyetr.inference.__all__:
            if func.__doc__ is not None:
                new_doc = func.__doc__
            else:
                new_doc = ""
            out.append(
                "`" + name + "`" + get_line_no(func) + "\n```\n" + new_doc + "\n```"
            )

    with open("./docs/inference_index.md", "w+") as f:
        intro = "# Inference Index\n\nBelow you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.\n\n## "
        full_page = intro + "\n\n## ".join(out)
        f.write(full_page)
