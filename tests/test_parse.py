from pyetr.func_library import log, power
from pyetr.parsing.fol_parser import fol_to_view, view_to_fol
from pyetr.parsing.view_parser import ViewParser


class TestFunction:
    def test_parse(self):
        input_string = "(Jack(Card()) ∨ Ace(Card()))"
        output_string = view_to_fol(fol_to_view(input_string))
        alt_string = "(Ace(Card()) ∨ Jack(Card()))"
        assert output_string == input_string or output_string == alt_string

    def test_detailed(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = fol_to_view(input_string)
        assert output_view.detailed

    def test_repr(self):
        input_string = "∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"
        output_view = fol_to_view(input_string)
        assert repr(output_view)

    def test_custom_func_parse(self):
        vp = ViewParser()
        v = vp.from_str(
            "Ax {power(++(1, log(++(1, x))), -1)=+ 0} ^ {D(x*)}",
            custom_functions=[power, log],
        )

        new_view = vp.from_json(vp.to_json(v))
        assert new_view == v
