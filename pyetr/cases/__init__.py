__all__ = ["BaseExample"]
from abc import ABCMeta, abstractmethod
from typing import cast

from pyetr.inference import basic_step, default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View


class BaseExample(metaclass=ABCMeta):
    v: tuple[View, ...]
    c: View

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "v"):
            raise TypeError("Example must have attribute v")
        if not hasattr(cls, "c"):
            raise TypeError("Example must have attribute c")
        v = getattr(cls, "v")
        assert isinstance(v, tuple)
        for i in v:
            assert isinstance(i, View)
        v = cast(tuple[View, ...], v)
        c = getattr(cls, "c")
        assert isinstance(c, View)

    @classmethod
    @abstractmethod
    def test(cls):
        raise NotImplementedError


class e1(BaseExample):
    """
    P1: Every archaeon has a nucleus; ∀x (IsArcheon(x) → HasNucleus(x))
    P2: Halobacterium is an archeon; IsArcheon(Halobacterium())

    C: Halobacterium is an archaeon and has a nucleus; IsArcheon(Halobacterium()) ∧ HasNucleus(Halobacterium())
    """

    v: tuple[View, View] = (
        ps("∀x (IsArcheon(x*) → IsArcheon(x) ∧ HasNucleus(x))"),
        ps("IsArcheon(Halobacterium()*)"),
    )
    c: View = ps("IsArcheon(Halobacterium()*) ∧ HasNucleus(Halobacterium())")

    @classmethod
    def test(cls):
        result = basic_step(cls.v)
        print("result", result)

        assert result.is_equivalent_under_arb_sub(cls.c)


class e47(BaseExample):
    """
    P1: Some thermotogum stains gram-negative
    P2: Maritima is a thermotogum

    C: Maritima stains gram negative
    """

    v: tuple[View, View] = (
        ps("∃x Thermotogum(x*) ∧ StainsGramNegative(x)"),
        ps("Thermotogum(Maritima()*)"),
    )
    c: View = ps("StainsGramNegative(Maritima())")

    @classmethod
    def test(cls):
        result = default_inference_procedure(cls.v)
        assert result.is_equivalent_under_arb_sub(cls.c)


class e56_basic_step(BaseExample):
    """
    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    """

    v: tuple[View, View] = (
        ps("∀x ∃y Professor(x) → Professor(x) ∧ Student(y*) ∧ Teaches(x, y)"),
        ps("∀z ∃w Student(z*) → Student(z) ∧ Book(w) ∧ Reads(z, w)"),
    )
    c: View = ps(
        "∀a ∃b ∃c Professor(a) → Professor(a) ∧ Student(b*) ∧ Teaches(a, b) ∧ Reads(b, c) ∧ Book(c)"
    ).depose()

    @classmethod
    def test(cls):
        result = basic_step(cls.v)
        assert result.is_equivalent_under_arb_sub(cls.c)


class e56_default_inference(e56_basic_step):
    c: View = ps("∃y ∃b ⊤ ∨ Reads(y,b) ∧ Book(b)")

    @classmethod
    def test(cls):
        result = default_inference_procedure(cls.v)
        assert result.is_equivalent_under_arb_sub(cls.c)


class e15(BaseExample):
    """
    P1: There is an ace and a jack and a queen, or else there is an eight
    and a ten and a four or else there is an ace.
    P2: There is an ace and a jack, and there is an ace and a ten.
    P3: There is not a queen.

    C: There is a four
    """

    v: tuple[View, View, View] = (
        ps(
            "∃x1 ∃x2 ∃x3 ∃x4 ∃x5 ∃x6 ∃x7 (Ace() ∧ Jack(x2) ∧ Queen(x3)) ∨ (Eight(x4) ∧ Ten(x5) ∧ Four(x6)) ∨ Ace(x7)"
        ),
        ps("∃y1 ∃y2 ∃y3 ∃y4 (Ace() ∧ Jack(y2)) ∨ (Ace(y3) ∧ Ten(y4))"),
        ps("∀z ~Queen(z)"),
    )
    c: View = ps("∃w Four(w)")

    @classmethod
    def test(cls):
        result = default_inference_procedure(cls.v)
        assert result.is_equivalent_under_arb_sub(cls.c)


class UniProduct(BaseExample):
    v = (ps("∀x ∃a (P(x*) ∧ E(x,a)) ∨ ~P(x)"), ps("P(j()*)"))
    c = ps("∃a (P(j()*) ∧ E(j(),a)) ∨ ~P(j())")

    @classmethod
    def test(cls):
        result = cls.v[0].universal_product(cls.v[1])
        assert result.is_equivalent_under_arb_sub(cls.c)
