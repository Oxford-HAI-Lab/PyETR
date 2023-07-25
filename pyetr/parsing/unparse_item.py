from pyetr.parsing.parse_string import Item


def unparse_items(items: list[Item]) -> str:
    return " ".join([item.to_string() for item in items])
