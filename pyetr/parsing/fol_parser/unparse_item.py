from .parse_string import Item


def unparse_items(items: list[Item]) -> str:
    """
    Unparse the parser object representation back to a string

    Args:
        items (list[Item]): The parser object representation

    Returns:
        str: The first order logic string.
    """
    return " ".join([item.to_string() for item in items])
