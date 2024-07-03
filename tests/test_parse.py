import pytest

from pyetr import View
from pyetr.func_library import log, power
from pyetr.parsing.common import ParsingError


class TestFunction:
    def test_parse(self):
        input_string = "(Jack(Card()) ∨ Ace(Card()))"
        output_string = View.from_fol(input_string).to_fol()
        alt_string = "(Ace(Card()) ∨ Jack(Card()))"
        assert output_string == input_string or output_string == alt_string

    def test_detailed(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = View.from_fol(input_string)
        assert output_view.detailed

    def test_repr(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = View.from_fol(input_string)
        assert repr(output_view)

    def test_custom_func_parse(self):
        v = View.from_str(
            "Ax {power(++(1, log(++(1, x))), -1)=+ 0} ^ {D(x*)}",
            custom_functions=[power, log],
        )

        new_view = View.from_json(v.to_json())
        assert new_view == v

    def test_arb_object_not_used(self):
        with pytest.raises(
            ValueError, match="not the same as those in stage/supposition"
        ):
            View.from_str("Ax Ay {f(y)}")
        with pytest.raises(ParsingError, match="not found in quantifiers"):
            View.from_fol("Ax Ay f(y)")
        with pytest.raises(
            ValueError, match="not the same as those in stage/supposition"
        ):
            View.from_str("Ax Ay {}")

    def test_arb_object_used_not_quantified(self):
        with pytest.raises(ParsingError, match="not found in quantifiers"):
            View.from_str("{f(y)}")
        with pytest.raises(ParsingError, match="not found in quantifiers"):
            View.from_fol("f(y)")

    def test_invalid_view(self):
        with pytest.raises(ParsingError, match=""):
            View.from_str("{")
        with pytest.raises(ParsingError, match="Expected end of text"):
            View.from_fol("f(")
