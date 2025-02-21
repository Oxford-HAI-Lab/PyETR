import pytest

from pyetr import ArbitraryObject, Function, View
from pyetr.atoms.predicate import Predicate


class TestReplace:
    def test_string_simple_func(self):
        v = View.from_str("{Buy()}")
        replaced_view = v.replace("Buy", "Sell")
        sample_view = View.from_str("{Sell()}")
        assert sample_view == replaced_view

    def test_string_simple_arb(self):
        v = View.from_str("Ax {f(x)}")
        replaced_view = v.replace("x", "y")
        sample_view = View.from_str("Ay {f(y)}")
        assert sample_view == replaced_view

    def test_strings_multiple(self):
        v = View.from_str("ABuy {Buy=* do(Buy(Buy*))}")
        replaced_view = v.replace("Buy", "Sell")
        sample_view = View.from_str("ASell {Sell=* do(Sell(Sell*))}")
        assert sample_view == replaced_view

    def test_arbs_multiple(self):
        v = View.from_str("ABuy {Buy(Buy*)=* do(Buy(Buy(Buy*)))}")
        search = ArbitraryObject("Buy")
        replacement = ArbitraryObject("Sell")
        replaced_view = v.replace(search, replacement)
        sample_view = View.from_str("ASell {Buy(Sell*)=* do(Buy(Buy(Sell*)))}")
        assert sample_view == replaced_view

    def test_func_multiple(self):
        v = View.from_str("ABuy {Buy(Buy*)=* do(Buy(Buy(Buy*)))}")
        search = Function("Buy", 1)
        replacement = Function("Sell", 1)
        replaced_view = v.replace(search, replacement)
        sample_view = View.from_str("ABuy {Sell(Buy*)=* do(Buy(Sell(Buy*)))}")
        assert sample_view == replaced_view

    def test_func_non_match_arity(self):
        v = View.from_str("ABuy {Buy(Buy*)=* do(Buy(Buy(Buy*)))}")
        search = Function("Buy", 1)
        replacement = Function("Sell", 0)
        with pytest.raises(
            ValueError,
            match=r"Original Function\(Buy, 1\) and replacement Function\(Sell, 0\) must match arity",
        ):
            v.replace(search, replacement)

    def test_predicate_multiple(self):
        v = View.from_str("ABuy {Buy(Buy*)=* do(Buy(Buy(Buy*)))}")
        search = Predicate("Buy", 1)
        replacement = Predicate("Sell", 1)
        replaced_view = v.replace(search, replacement)
        sample_view = View.from_str("ABuy {Buy(Buy*)=* do(Sell(Buy(Buy*)))}")
        assert sample_view == replaced_view

    def test_predicate_non_match_arity(self):
        v = View.from_str("ABuy {Buy(Buy*)=* do(Buy(Buy(Buy*)))}")
        search = Predicate("Buy", 1)
        replacement = Predicate("Sell", 0)
        with pytest.raises(
            ValueError,
            match=r"Original <Predicate name=Buy arity=1> and replacement <Predicate name=Sell arity=0> must match arity",
        ):
            v.replace(search, replacement)
