import pytest

from pyetr import ArbitraryObject, Function, FunctionalTerm


class TestFunction:
    def test_invalid_arity(self):
        with pytest.raises(ValueError, match="arity must not be less than 0"):
            Function("bad_func", -1)

    def test_valid(self):
        test = Function("good_func", 1)
        assert test.detailed == "Function(good_func, 1)"

    def test_same_name_different_arity(self):
        func1 = Function(name="gentoo", arity=0)
        func2 = Function(name="gentoo", arity=1)

        assert not func1.__eq__(func2)

    def test_eq_diff_obj(self):
        func1 = Function(name="gentoo", arity=0)
        arb = ArbitraryObject(name="thing")
        assert not func1 == arb

    def test_repr(self):
        func = Function(name="gentoo", arity=0)
        assert repr(func) == "Function(gentoo, 0)"


class TestArbitraryObject:
    def test_valid_exi(self):
        test = ArbitraryObject("x1")
        assert test.detailed == "<ArbitraryObject name=x1>"

    def test_valid_uni(self):
        test = ArbitraryObject(
            "x1",
        )
        assert test.detailed == "<ArbitraryObject name=x1>"

    def test_repr(self):
        func = ArbitraryObject(name="gentoo")
        assert repr(func) == "gentoo"

    def test_eq_diff_obj(self):
        func1 = Function(name="gentoo", arity=0)
        arb = ArbitraryObject(name="thing")
        assert not arb == func1


class TestFunctionalTerm:
    def test_valid(self, func: Function, arb_obj: ArbitraryObject):
        t = FunctionalTerm(func, [arb_obj])
        assert (
            t.detailed
            == "<FunctionalTerm f=Function(func, 1) t=(<ArbitraryObject name=x1>)>"
        )
