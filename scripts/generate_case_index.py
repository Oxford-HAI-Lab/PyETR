import inspect

import pyetr.cases
from pyetr.cases import BaseExample


def get_line_no(item):
    if item:
        # Get the source file and line number
        _, start_line_number = inspect.getsourcelines(item)
        url_prefix = (
            "https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L"
        )
        return f"\n[Link to code]({url_prefix}{start_line_number})\n\n"
    else:
        return ""


def main():
    out = []
    for name, case in vars(pyetr.cases).items():
        if (
            isinstance(case, type)
            and issubclass(case, BaseExample)
            and case != BaseExample
        ):
            out.append(name + get_line_no(case) + "\n```" + repr(case) + "```")

    with open("./docs/case_index.md", "w+") as f:
        intro = "# Case Index\n\nBelow you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.\n\n## "
        full_page = intro + "\n\n## ".join(out)
        f.write(full_page)
