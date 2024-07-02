# from typing import Any

# from pyetr.atoms.terms.function import Function, NumFunc
# from pyetr.parsing.fol_parser import fol_to_view, view_to_fol
# from pyetr.view import View

# from .data_parser import json_to_view, view_to_json
# from .string_parser import string_to_view, view_to_string


# class ViewParser:
#     """
#     Tool used to easily parse views between different forms
#     """

#     @classmethod
#     def from_json(cls, s: str) -> View:
#         """
#         Parses from json form to View form

#         Args:
#             s (str): The json string

#         Returns:
#             View: The parsed view
#         """
#         return json_to_view(s)

#     @classmethod
#     def to_json(cls, v: View) -> str:
#         """
#         Parses from View form to json form

#         Args:
#             v (View): The input view

#         Returns:
#             str: The output json
#         """
#         return view_to_json(v)

#     @classmethod
#     def from_str(
#         cls, s: str, custom_functions: list[NumFunc | Function] | None = None
#     ) -> View:
#         """
#         Parses from view string form to view form.

#         Args:
#             s (str): view string
#             custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
#                 string. It assumes the name of the function is that used in the string. Useful
#                 for using func callers. Defaults to None.

#         Returns:
#             View: The output view
#         """
#         return string_to_view(s, custom_functions)

#     @classmethod
#     def to_str(cls, v: View, **string_conversion_args: Any) -> str:
#         """
#         Parses from View form to view string form

#         Args:
#             v (View): The view to convert to string

#         Returns:
#             str: The view string
#         """
#         return view_to_string(v, **string_conversion_args)

#     @classmethod
#     def from_fol(
#         cls, s: str, custom_functions: list[NumFunc | Function] | None = None
#     ) -> View:
#         """
#         Parses from first order logic string form to View form.
#         Args:
#             s (str): A first order logic string
#             custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
#                 string. It assumes the name of the function is that used in the string. Useful
#                 for using func callers. Defaults to None.
#         Returns:
#             View: The parsed view
#         """
#         return fol_to_view(s, custom_functions=custom_functions)

#     @classmethod
#     def to_fol(cls, v: View) -> str:
#         """
#         Parses from View form to first order logic string form.

#         Args:
#             v (View): The View object

#         Returns:
#             str: The first order logic string form.
#         """
#         return view_to_fol(v)
