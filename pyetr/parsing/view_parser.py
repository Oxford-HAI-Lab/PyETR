from pyetr.atoms.terms.function import Function
from pyetr.parsing.fol_parser import fol_to_view, view_to_fol
from pyetr.view import View

from .data_parser import json_to_view, view_to_json
from .string_parser import string_to_view, view_to_string


class ViewParser:
    @staticmethod
    def from_json(s: str) -> View:
        return json_to_view(s)

    @staticmethod
    def to_json(v: View) -> str:
        return view_to_json(v)

    @staticmethod
    def from_str(s: str, custom_functions: list[Function] | None = None) -> View:
        return string_to_view(s, custom_functions)

    @staticmethod
    def to_str(v: View, **string_conversion_args) -> str:
        return view_to_string(v, **string_conversion_args)

    @staticmethod
    def from_fol(s: str) -> View:
        return fol_to_view(s)

    @staticmethod
    def to_fol(v: View) -> str:
        return view_to_fol(v)
