import pytest

from pyetr.parsing.fol_parser import parse_string_to_view, parse_view_to_string


class TestFunction:
    def test_parse(self):
        input_string = "(Jack(Card()) ∨ Ace(Card()))"
        output_string = parse_view_to_string(parse_string_to_view(input_string))
        alt_string = "(Ace(Card()) ∨ Jack(Card()))"
        assert output_string == input_string or output_string == alt_string

    def test_detailed(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = parse_string_to_view(input_string)
        assert output_view.detailed

    def test_repr(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = parse_string_to_view(input_string)
        assert repr(output_view)
