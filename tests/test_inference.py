from pyetr import View
from pyetr.inference import (
    classically_valid_does_it_follow,
    classically_valid_inference_procedure,
)


class TestClassicalInferenceProcedure:
    def test_simple_mp(self, verbose: bool = False):
        v = (View.from_str("{p()}"), View.from_str("{q()}^{p()}"))
        c = View.from_str("{q()}")
        result = classically_valid_inference_procedure(v, verbose=verbose)
        assert result.is_equivalent_under_arb_sub(
            c
        ), f"Expected: {c} but received {result}"

    def test_illusory_inference_blocked(self, verbose: bool = False):
        v = (View.from_str("{a()b(), c()d()}"), View.from_str("{a()}"))
        c = View.from_str("{b()}")
        result = classically_valid_inference_procedure(v, verbose=verbose)
        assert not result.is_equivalent_under_arb_sub(c)

    def test_procedure_with_verum(self, verbose: bool = False):
        v = (View.from_str("{0}"), View.from_str("{p()}"))
        c = View.from_str("{0}")
        result = classically_valid_inference_procedure(v, verbose=verbose)
        assert result.is_equivalent_under_arb_sub(
            c
        ), f"Expected: {c} but received {result}"


class TestClassicalInferenceDoesItFollow:
    def test_simple_mp(self, verbose: bool = False):
        v = (View.from_str("{p()}"), View.from_str("{q()}^{p()}"))
        c = View.from_str("{q()}")
        result = classically_valid_does_it_follow(v, c, verbose=verbose)
        assert result

    def test_illusory_inference_blocked(self, verbose: bool = False):
        v = (View.from_str("{a()b(), c()d()}"), View.from_str("{a()}"))
        c = View.from_str("{b()}")
        result = classically_valid_does_it_follow(v, c, verbose=verbose)
        assert not result
