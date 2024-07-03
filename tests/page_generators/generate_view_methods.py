from pyetr.view import View

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
    "## Parsing": ["from_str", "to_str", "from_fol", "to_fol", "from_json", "to_json"],
}

out = []
for section, section_items in relevant_methods.items():
    out.append(f"{section}\n")
    for name in section_items:
        assert name in dir(View)
        method = getattr(View, name)
        out.append("### `" + name + "`\n```\n" + method.__doc__ + "\n```")


with open("../../docs/view_methods.md", "w+") as f:
    intro = "# View Methods Index\n\nBelow you'll find all of the methods of View, including associated operations and ways of creating them.\n"
    full_page = intro + "\n\n".join(out)
    f.write(full_page)
