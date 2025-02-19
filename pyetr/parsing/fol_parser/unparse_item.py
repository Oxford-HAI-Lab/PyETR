from typing import Unpack

from pyetr.parsing.common import StringConversion

from ..fol_items import Item


def unparse_items(
    items: list[Item], **string_conversion_kwargs: Unpack[StringConversion]
) -> str:
    """
    Unparse the parser object representation back to a string

    Args:
        items (list[Item]): The parser object representation

    Returns:
        str: The first order logic string.
    """
    return " ".join([item.to_string(**string_conversion_kwargs) for item in items])
