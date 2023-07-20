import pytest

from pyetr import parse_string_to_view


class TestFunction:
    def test_parse(self):
        input_string = "∃x ∀y ∃z ∃w ((P(Mary(), x) ∨ P(f_Ace(y), x)) ∨ ((P(z, *f_King(y))) ∨ (P(John(), x) ∨ (P(w, f_Queen(z)) ∨ P(w, f_Jack(y))))))"
        parse_string_to_view(input_string)
