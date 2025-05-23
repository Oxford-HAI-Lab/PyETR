import inspect
from typing import get_overloads

from pyetr.view import View

from .common import get_line_no

relevant_methods: dict[str, list[str]] = {
    "## View Operations": [
        "product",
        "sum",
        "update",
        "answer",
        "negation",
        "merge",
        "division",
        "factor",
        "depose",
        "inquire",
        "suppose",
        "query",
        "which",
        "universal_product",
        "atomic_answer",
        "equilibrium_answer",
        "existential_sum",
    ],
    "## Parsing": [
        "from_str",
        "to_str",
        "from_fol",
        "to_fol",
        "from_json",
        "to_json",
        "from_smt",
        "to_smt",
        "from_smt_lib",
        "to_smt_lib",
        "to_english",
    ],
    "## Other": ["replace"],
}


def main():
    out = []
    for section, section_items in relevant_methods.items():
        out.append(f"{section}\n")
        for name in section_items:
            assert name in dir(View)
            method = getattr(View, name)
            overloads = get_overloads(method)
            if overloads:
                for i, overload in enumerate(overloads):
                    doc = inspect.getdoc(overload)
                    if doc is not None:
                        main_str = (
                            "### `"
                            + name
                            + f" (overload{str(i+1)})"
                            + "`\n"
                            + get_line_no(overload, "view")
                            + "```\n"
                            + doc
                            + "\n```"
                        )
                        out.append(main_str)
            else:
                doc = inspect.getdoc(method)
                if doc is not None:
                    main_str = (
                        "### `"
                        + name
                        + "`\n"
                        + get_line_no(method, "view")
                        + "```\n"
                        + doc
                        + "\n```"
                    )
                    out.append(main_str)

    with open("./docs/reference/view_methods.md", "w+") as f:
        intro = "# View Methods Index\n\nBelow you'll find all of the methods of View, including associated operations and ways of creating them.\n"
        full_page = intro + "\n\n".join(out)
        f.write(full_page)
