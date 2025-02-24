__all__ = ["view_to_english"]
import typing
from typing import Unpack

from pyetr.parsing.common import Quantified, StringConversion

from ..fol_items import Item, view_to_items

if typing.TYPE_CHECKING:
    from pyetr.view import View


def unparse_items_to_eng(
    items: list[Item],
    name_mappings: dict[str, str],
    **string_conversion_kwargs: Unpack[StringConversion],
) -> str:
    """
    Unparse the parser object representation back to a string

    Args:
        items (list[Item]): The parser object representation

    Returns:
        str: The english string.
    """
    # First separate quantifieds
    view_item = None
    quantifieds: list[Quantified] = []
    for item in items:
        if isinstance(item, Quantified):
            quantifieds.append(item)
        else:
            assert view_item is None  # There must only be one valid view
            view_item = item
    if view_item is None:
        raise ValueError(f"Main section not found")

    # parse main item

    current_quants: list[str] = []
    last_quantifier = None
    current_string = ""
    for quant in quantifieds:
        if last_quantifier is not None and quant.quantifier != last_quantifier:
            if last_quantifier == "∀":
                current_string += f"for all {', '.join(current_quants)}, "
            else:
                current_string += f"there exists {', '.join(current_quants)} such that "
            current_quants = []
        current_quants.append(
            quant.variable.to_english(name_mappings, **string_conversion_kwargs)
        )
        last_quantifier = quant.quantifier
    if current_quants:
        if last_quantifier == "∀":
            current_string += f"for all {', '.join(current_quants)}, "
        else:
            current_string += f"there exists {', '.join(current_quants)} such that "

    out = view_item.to_english(name_mappings, **string_conversion_kwargs)
    return current_string + out


def view_to_english(
    v: "View",
    name_mappings: dict[str, str],
    **string_conversion_kwargs: Unpack[StringConversion],
) -> str:
    """
    Parses from View form to english string form.

    Args:
        v (View): The View object

    Returns:
        str: The english form.
    """
    return unparse_items_to_eng(
        view_to_items(v), name_mappings, **string_conversion_kwargs
    )
