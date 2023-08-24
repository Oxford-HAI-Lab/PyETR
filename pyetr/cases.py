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
    def test(cls, verbose: bool = False):
        raise NotImplementedError


class BaseTest:
    v: tuple[View, ...]
    c: View


class DefaultInference(BaseTest):
    @classmethod
    def test(cls, verbose: bool = False):
        result = default_inference_procedure(cls.v, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class BasicStep(BaseTest):
    @classmethod
    def test(cls, verbose: bool = False):
        result = basic_step(cls.v, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Factor(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].factor(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e1(DefaultInference, BaseExample):
    """
    Example 1 (p. 61):

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else
    Mark is standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire.
    C Jane is looking at the TV.
    """

    v: tuple[View, View] = (
        ps(
            "(KneelingByTheFire(Jane()) ∧ LookingAtTV(Jane())) ∨ (StandingAtTheWindow(Mark()) ∧ PeeringIntoTheGarden(Mark()))"
        ),
        ps("KneelingByTheFire(Jane())"),
    )
    c: View = ps("LookingAtTV(Jane())")


class e2(DefaultInference, BaseExample):
    """
    Example 2 (p. 62):

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    """

    v: tuple[View, View] = (
        ps("(A(x()) ∧ Q(y())) ∨ (K(z()) ∧ T(w()))"),
        ps("K(x())"),
    )
    c: View = ps("T(x())")


class e3(DefaultInference, BaseExample):
    """
    Example 3 (p.63):

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("(Ace(a()) ∧ King(k())) ∨ (Queen(q()) ∧ Jack(j()))"),
        ps("~Ace(a())"),
    )
    c: View = ps("Queen(q()) ∧ Jack(j())")


class e10(DefaultInference, BaseExample):
    """
    Example 10 (p.76)

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a ten.
    """

    v: tuple[View, View] = (
        ps("K(x())"),
        ps("(A(x()) ∧ Q(y())) ∨ (K(z()) ∧ T(w()))"),
    )
    c: View = ps("⊤")


class e11(DefaultInference, BaseExample):
    """
    Example 11 (p. 77)

    P1 Either John smokes or Mary smokes.
    P2 Supposing John smokes, John drinks.
    P3 Supposing Mary smokes, Mary eats.
    C Either John smokes and drinks or Mary smokes and drinks.
    """

    v: tuple[View, View, View] = (
        ps("Smokes(j()) ∨ Smokes(m())"),
        ps("Smokes(j()) → Drinks(j())"),
        ps("Smokes(m()) → Eats(m())"),
    )
    c: View = ps("(Smokes(j()) ∧ Drinks(j())) ∨ (Smokes(m()) ∧ Drinks(m()))")


# class e12i(NegationTest, BaseExample):
#     """
#     Example 12i (p. 78)

#     ItisnotthecasethatPorQorR
#     """
#     v: tuple[View] = (
#         ps("P(p()) ∨ Q(q()) ∨ R(r())"),
#     )
#     c: View = ps("~P(p()) ∧ ~Q(q()) ∧ ~R(r())")

# class e12ii(NegationTest, BaseExample):
#     """
#     Example 12ii (p. 78)

#     ItisnotthecasethatPandQandR
#     """
#     v: tuple[View] = (
#         ps("P(p()) ∧ Q(q()) ∧ R(r())"),
#     )
#     c: View = ps("~P(p()) ∧ ~Q(q()) ∧ ~R(r())")

# class e12iii(NegationTest, BaseExample):
#     """
#     Example 12iii (p. 79)

#     It is not the case that, supposing S, ((P and Q) or R)
#     """
#     v: tuple[View] = (
#         ps("S(s()) → ((P(p()) ∧ Q(q())) ∨ R(r()))"),
#     )
#     c: View = ps("(S(s()) ∧ ~P(p()) ∧ ~R(r())) ∨ (S(s()) ∧ ~Q(q()) ∧ ~R(r()))")


class e13(DefaultInference, BaseExample):
    """
    Example 13 (p. 80)

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("(IsAce(a()) ∧ IsKing(k())) ∨ (IsQueen(q()) ∧ IsJack(j()))"),
        ps("~IsAce(a())"),
    )
    c: View = ps("IsQueen(q()) ∧ IsJack(j())")


class e14_1(Factor, BaseExample):
    """
    Example 14-1(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("(P(p()) ∧ Q(q())) ∨ (P(p()) ∧ R(r()))"),
        ps("P(p())"),
    )
    c: View = ps("Q(q()) ∨ R(r())")


class e14_2(Factor, BaseExample):
    """
    Example 14-2(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps(
            "(P(p()) ∧ Q(q()) ∧ S(s())) ∨ (P(p()) ∧ R(r()) ∧ S(s())) ∨ (P(p()) ∧ R(r()))"
        ),
        ps("(S(s())) → (P(p()))"),
    )
    c: View = ps("(Q(q()) ∧ S(s())) ∨ (R(r()) ∧ S(s())) ∨ (P(p()) ∧ R(r()))")


class e14_3(Factor, BaseExample):
    """
    Example 14-2(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps(
            "(P(p()) ∧ Q(q()) ∧ S(s())) ∨ (P(p()) ∧ R(r()) ∧ S(s())) ∨ (P(p()) ∧ R(r()))"
        ),
        ps("(S(s())) → (P(p()))"),
    )
    c: View = ps("(Q(q()) ∧ S(s())) ∨ (R(r()) ∧ S(s())) ∨ (P(p()) ∧ R(r()))")


class e47(DefaultInference, BaseExample):
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


class e48(DefaultInference, BaseExample):
    """
    P1 Some dictyoglomus is thermophobic.
    P2 Turgidum is not a dictyoglomus.
    C Turgidum is not a dictyoglomus.
    """

    v: tuple[View, View] = (
        ps("∃x D(x*) ∧ T(x)"),
        ps("~D(Turgidum()*)"),
    )
    c: View = ps("~D(Turgidum())")


class e51(BasicStep, BaseExample):
    """
    P1: Every archaeon has a nucleus
    P2: Halobacterium is an archeon

    C: Halobacterium is an archaeon and has a nucleus
    """

    v: tuple[View, View] = (
        ps("∀x (IsArcheon(x*) → IsArcheon(x) ∧ HasNucleus(x))"),
        ps("IsArcheon(Halobacterium()*)"),
    )
    c: View = ps("IsArcheon(Halobacterium()*) ∧ HasNucleus(Halobacterium())")


class e56_default_inference(DefaultInference, BaseExample):
    """
    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    """

    v: tuple[View, View] = (
        ps("∀x ∃y Professor(x) → Professor(x) ∧ Student(y*) ∧ Teaches(x, y)"),
        ps("∀z ∃w Student(z*) → Student(z) ∧ Book(w) ∧ Reads(z, w)"),
    )

    c: View = ps("∃y ∃b ⊤ ∨ Reads(y,b) ∧ Book(b)")


class e56_basic_step(BasicStep, e56_default_inference):
    c: View = ps(
        "∀a ∃b ∃c Professor(a) → Professor(a) ∧ Student(b*) ∧ Teaches(a, b) ∧ Reads(b, c) ∧ Book(c)"
    ).depose()


# class e15(BaseExample):
#     """
#     P1: There is an ace and a jack and a queen, or else there is an eight
#     and a ten and a four or else there is an ace.
#     P2: There is an ace and a jack, and there is an ace and a ten.
#     P3: There is not a queen.

#     C: There is a four
#     """

#     v: tuple[View, View, View] = (
#         ps(
#             "∃x1 ∃x2 ∃x3 ∃x4 ∃x5 ∃x6 ∃x7 (Ace() ∧ Jack(x2) ∧ Queen(x3)) ∨ (Eight(x4) ∧ Ten(x5) ∧ Four(x6)) ∨ Ace(x7)"
#         ),
#         ps("∃y1 ∃y2 ∃y3 ∃y4 (Ace() ∧ Jack(y2)) ∨ (Ace(y3) ∧ Ten(y4))"),
#         ps("∀z ~Queen(z)"),
#     )
#     c: View = ps("∃w Four(w)")

#     @classmethod
#     def test(cls):
#         result = default_inference_procedure(cls.v)
#         assert result.is_equivalent_under_arb_sub(cls.c)


class UniProduct(BaseExample):
    v = (ps("∀x ∃a (P(x*) ∧ E(x,a)) ∨ ~P(x)"), ps("P(j()*)"))
    c = ps("∃a (P(j()*) ∧ E(j(),a)) ∨ ~P(j())")

    @classmethod
    def test(cls):
        result = cls.v[0].universal_product(cls.v[1])
        assert result.is_equivalent_under_arb_sub(cls.c)
