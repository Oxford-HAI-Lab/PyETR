__all__ = ["BaseExample"]
from abc import ABCMeta, abstractmethod
from typing import cast

from pyetr.inference import basic_step, default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View


class BaseExample(metaclass=ABCMeta):
    v: tuple[View, ...]
    c: View | tuple[View, ...]

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
        assert isinstance(c, View) or (
            isinstance(c, tuple) and all(isinstance(x, View) for x in c)
        )

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


class Product(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].product(cls.v[1])
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Sum(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].sum(cls.v[1])
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Factor(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].factor(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Negation(BaseTest):
    v: tuple[View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].negation(verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Query(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].query(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class WHQuery(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].wh_query(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Suppose(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].suppose(cls.v[1], verbose=verbose)
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
        ps("K(z())"),
    )
    c: View = ps("T(w())")


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


# e4 is not a test


class samples:
    gamma = "p1() ∧ q1()"
    delta = "r1() ∧ s1()"
    epsilon = "p2() ∧ q2()"
    theta = "r2() ∧ s2()"


class e5ii(Product, BaseExample):
    v: tuple[View, View] = (
        ps("p1() ∧ q1() ∨ r1() ∧ s1()"),
        ps(f"p2() ∧ q2() ∨ r2() ∧ s2()"),
    )
    c: View = ps(
        "p1() ∧ q1() ∧ p2() ∧ q2() ∨ r1() ∧ s1() ∧ p2() ∧ q2() ∨ p1() ∧ q1() ∧ r2() ∧ s2() ∨ r1() ∧ s1() ∧ r2() ∧ s2()"
    )


class e5iii(Product, BaseExample):
    v: tuple[View, View] = (ps(f"{samples.gamma} ∨ {samples.delta}"), View.get_falsum())
    c: View = View.get_falsum()


class e5iv(Product, BaseExample):
    v: tuple[View, View] = (ps(f"{samples.gamma} ∨ {samples.delta}"), View.get_verum())
    c: View = ps(f"{samples.gamma} ∨ {samples.delta}")


class e5v(Product, BaseExample):
    v: tuple[View, View] = (
        View.get_verum(),
        ps(f"{samples.gamma} ∨ {samples.delta}"),
    )
    c: View = ps(f"{samples.gamma} ∨ {samples.delta}")


class e6(Product, BaseExample):
    """
    Example 6, p72

    There is an Ace and a King = (There is an Ace) x (There is a king)
    """

    v: tuple[View, View] = (ps("a()"), ps("k()"))
    c: View = ps("a() ∧ k()")


class e7(Sum, BaseExample):
    """
    Example 7, p73

    There is an Ace or there is a king = (There is an Ace) + (There is a king)
    """

    v: tuple[View, View] = (ps("a()"), ps("k()"))
    c: View = ps("a() ∨ k()")


class e8(DefaultInference, BaseExample):
    """
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    """

    v: tuple[View, View] = (ps("a() ∧ q() ∨ k() ∧ t()"), ps("k()"))
    c: View = ps("t()")


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


class e11(BasicStep, BaseExample):
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
    c: View = ps("(Smokes(j()) ∧ Drinks(j())) ∨ (Smokes(m()) ∧ Eats(m()))")


class e12i(Negation, BaseExample):
    """
    Example 12i (p. 78)

    ItisnotthecasethatPorQorR
    """

    v: tuple[View] = (ps("P(p()) ∨ Q(q()) ∨ R(r())"),)
    c: View = ps("~P(p()) ∧ ~Q(q()) ∧ ~R(r())")


class e12ii(Negation, BaseExample):
    """
    Example 12ii (p. 78)

    ItisnotthecasethatPandQandR
    """

    v: tuple[View] = (ps("P(p()) ∧ Q(q()) ∧ R(r())"),)
    c: View = ps("~P(p()) ∨ ~Q(q()) ∨ ~R(r())")


class e12iii(Negation, BaseExample):
    """
    Example 12iii (p. 79)

    It is not the case that, supposing S, ((P and Q) or R)
    """

    v: tuple[View] = (ps("S(s()) → ((P(p()) ∧ Q(q())) ∨ R(r()))"),)
    c: View = ps("(S(s()) ∧ ~P(p()) ∧ ~R(r())) ∨ (S(s()) ∧ ~Q(q()) ∧ ~R(r()))")


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
    Example 14-3(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps(
            "(P(p()) ∧ R(r())) ∨ (Q(q()) ∧ S(s())) ∨ (P(p()) ∧ S(s())) ∨ (Q(q()) ∧ R(r()))"
        ),
        ps("P(p()) ∨ Q(q())"),
    )
    c: View = ps("R(r()) ∨ S(s())")


class e14_6(Factor, BaseExample):
    """
    Example 14-6(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("(P(p()) ∧ R(r())) ∨ (Q(q()) ∧ S(s()))"),
        ps("P(p()) ∨ Q(q()) ∨ T(t())"),
    )
    c: View = ps("(P(p()) ∧ R(r())) ∨ (Q(q()) ∧ S(s()))")


class e14_7(Factor, BaseExample):
    """
    Example 14-7(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("(P(p()) ∧ R(r())) ∨ (Q(q()) ∧ S(s())) ∨ P(p())"),
        ps("P(p()) ∨ Q(q())"),
    )
    c: View = ps("R(r()) ∨ S(s()) ∨ ⊤")


class e15(DefaultInference, BaseExample):
    """
    Example 15

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    """

    v: tuple[View, View, View] = (
        ps(
            "(Ace(a()) ∧ Jack(j()) ∧ Queen(q())) ∨ (Eight(e()) ∧ Ten(t()) ∧ Four(f())) ∨ (Ace(a()))"
        ),
        ps("Ace(a()) ∧ Jack(j()) ∧ Eight(e()) ∧ Ten(t())"),
        ps("~Queen(q())"),
    )
    c: View = ps("Four(f())")


class e16(DefaultInference, BaseExample):
    """
    Example 16

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    """

    v: tuple[View, View, View] = (
        ps(
            "(Ten(t()) ∧ Eight(e()) ∧ Four(f())) ∨ (Jack(j()) ∧ King(k()) ∧ Queen(q())) ∨ (Ace(a()))"
        ),
        ps("~Four(f())"),
        ps("~Ace(a())"),
    )
    c: View = ps("Jack(j()) ∧ King(k()) ∧ Queen(q())")


class e17(DefaultInference, BaseExample):
    """
    Example 17

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    """

    v: tuple[View, View] = (
        ps("(King(k()) ∧ ~Ace(a())) ∨ (Ace(a()) ∧ ~King(k()))"),
        ps("King(k())"),
    )
    c: View = ps("~Ace(a())")


class e19(Suppose, BaseExample):
    """
    Example 19, page 84

    Suppose test
    """

    v: tuple[View, View] = (
        ps("⊤"),
        ps("~N()"),
    )
    c: View = ps("~N() → ~N()")


class e20(DefaultInference, BaseExample):
    """
    Example 20

    P1 Either there is a king in the hand or a queen in the hand.
    P2 On the supposition that there is a king, Mary wins.
    P3 On the supposition that there is a queen, Bill wins.
    C Either Mary wins or Bill wins.
    """

    v: tuple[View, View, View] = (
        ps("King(k()) ∨ Queen(q())"),
        ps("(King(k())) → (Win(mary()))"),
        ps("(Queen(q())) → (Win(bill()))"),
    )
    c: View = ps("Win(mary()) ∨ Win(bill())")


class e21(BaseExample):
    """
    Example 21
    """

    v: tuple[View] = (ps(f"⊤ → {samples.delta}"),)
    c: View = ps(f"⊤ → {samples.delta}").negation()

    @classmethod
    def test(cls, verbose: bool = False):
        x = View.get_falsum().suppose(cls.v[0], verbose=verbose)
        result = x.depose(verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e22(BaseExample):
    """
    Example 22

    It is not the case that A and B and C
    """

    v: tuple[View, View, View, View] = (
        ps(f"a() ∧ b() ∧ c()"),
        ps("a()"),
        ps("b()"),
        ps("c()"),
    )
    c: tuple[View, View] = (
        ps("~a() ∨ ~b() ∨ ~c()"),
        ps(
            "~a() ∧ b() ∧ c() ∨ ~a() ∧ b() ∧ ~c() ∨ ~a() ∧ ~b() ∧ c() ∨ ~a() ∧ ~b() ∧ ~c() ∨ a() ∧ ~b() ∧ c() ∨ a() ∧ ~b() ∧ ~c() ∨ a() ∧ b() ∧ ~c()"
        ),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = cls.v[0].negation()

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = (
            mid_result.inquire(cls.v[1], verbose=verbose)
            .inquire(cls.v[2], verbose=verbose)
            .inquire(cls.v[3], verbose=verbose)
        )

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e23_with_inquire(BaseExample):
    """
    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    """

    v: tuple[View, View] = (ps("K() ∧ L() ∨ S() ∧ P()"), ps("K()"))
    c: tuple[View, View] = (
        ps("K() ∧ L() ∨ S() ∧ P() ∧ K() ∨ S() ∧ P() ∧ ~K()"),
        ps("K() ∧ L() ∨ S() ∧ P() ∧ K()"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            View.get_verum()
            .update(cls.v[0], verbose=verbose)
            .inquire(cls.v[1], verbose=verbose)
        )

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = mid_result.update(cls.v[1], verbose=verbose)

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e23_without_inquire(BaseExample):
    v: tuple[View, View] = (ps("K() ∧ L() ∨ S() ∧ P()"), ps("K()"))
    c: tuple[View, View] = (
        ps("K() ∧ L() ∨ S() ∧ P()"),
        ps("K() ∧ L()"),
    )

    # TODO: Maybe add query or factor to remove K()
    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = View.get_verum().update(cls.v[0], verbose=verbose)

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = mid_result.update(cls.v[1], verbose=verbose)

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e24(BaseExample):
    """
    Example 24

    P1 There is an ace
    C There is an ace or a queen
    """

    v: tuple[View, View] = (ps("a()"), ps("q()"))
    c: tuple[View, View] = (ps("(a() ∧ q()) ∨ (a() ∧ ~q())"), ps("q() ∨ a()"))

    @classmethod
    def test(cls, verbose: bool = False):
        result_1 = cls.v[0].inquire(other=cls.v[1], verbose=verbose)

        if not result_1.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {result_1}"
            )

        result_2 = result_1.factor(cls.v[1], verbose=verbose).factor(
            cls.v[0], verbose=verbose
        )

        if not result_2.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result_2}")


class e25i(Query, BaseExample):
    """
    Example 25i
    """

    v: tuple[View, View] = (ps("(p() ∧ q()) ∨ (p() ∧ r())"), ps("p()"))
    c: View = ps("p()")


class e25ii(Query, BaseExample):
    """
    Example 25ii
    """

    v: tuple[View, View] = (ps("(p() ∧ q()) ∨ (p() ∧ r())"), ps("q()"))
    c: View = ps("⊤ ∨ q()")


class e25iii(Query, BaseExample):
    """
    Example 25iii
    """

    v: tuple[View, View] = (
        ps("(p() ∧ q()) ∨ (p() ∧ r()) ∨ s() ∨ t()"),
        ps("p() ∨ s()"),
    )
    c: View = ps("p() ∨ s() ∨ ⊤")


class e25iv(Query, BaseExample):
    """
    Example 25iv
    """

    v: tuple[View, View] = (
        ps("(p() ∧ q()) ∨ (p() ∧ r()) ∨ s() ∨ t()"),
        ps("p() ∨ s() ∨ t()"),
    )
    c: View = ps("p() ∨ s() ∨ t()")


class e25v(Query, BaseExample):
    """
    Example 25v
    """

    v: tuple[View, View] = (
        ps("(p() ∧ q() ∧ s()) ∨ (p() ∧ r() ∧ s())"),
        ps("s() → p()"),
    )
    c: View = ps("p()")


class e25vi(Query, BaseExample):
    """
    Example 25vi
    """

    v: tuple[View, View] = (
        ps("(p() ∧ q() ∧ s()) ∨ (p() ∧ r() ∧ s())"),
        ps("t() → p()"),
    )
    c: View = View.get_verum()


class e26(BaseExample):
    """
    Example 26

    P1 Either John plays and wins, or Mary plays, or Bill plays
    C Supposing John plays, John wins
    """

    v: tuple[View, View, View] = (
        ps("(Play(J()) ∧ Win(J())) ∨ Play(M()) ∨ Play(B())"),
        ps("Play(J())"),
        ps("Play(J()) → Win(J())"),
    )
    c: tuple[View, View] = (
        ps("Play(J()) → (Play(J()) ∧ Win(J()))"),
        ps("Play(J()) → Win(J())"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = cls.v[0].suppose(other=cls.v[1])

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = cls.c[0].query(other=cls.v[2])

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e28(DefaultInference, BaseExample):
    """
    Example 28

    P1 Is there a tiger?
    P2 Supposing there is a tiger, there is orange fur.
    P3 There is orange fur.
    C There is a tiger.
    """

    v: tuple[View, View, View] = (
        ps("Tiger(t()) ∨ ~Tiger(t())"),
        ps("(Tiger(t())) → (Tiger(t()) ∧ Orange(o()))"),
        ps("Orange(o())"),
    )
    c: View = ps("Tiger(t())")


class e32_1(DefaultInference, BaseExample):
    """
    Example 32-1

    P1 If P then Q.
    P2 P
    C Q
    """

    v: tuple[View, View] = (
        ps("(P(p())) → (P(p()) ∧ Q(q()))"),
        ps("P(p())"),
    )
    c: View = ps("Q(q())")


class e32_2(DefaultInference, BaseExample):
    """
    Example 32-2

    P1 P
    P2 If P then Q.
    C Q
    """

    v: tuple[View, View] = (
        ps("P(p())"),
        ps("(P(p())) → (P(p()) ∧ Q(q()))"),
    )
    c: View = ps("Q(q())")


class e33(DefaultInference, BaseExample):
    """
    Example 33

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    """

    v: tuple[View, View] = (
        ps("(R(r())) → (R(r()) ∧ E(e()))"),
        ps("E(e())"),
    )
    c: View = ps("R(r())")


class e40i(DefaultInference, BaseExample):
    """
    Example 40
    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    """

    v: tuple[View, View, View] = (
        ps(
            "(SquareB() ∧ ~TriangleB() ∧ ~CircleB()) ∨ (~SquareB() ∧ TriangleB() ∧ ~CircleB()) ∨ (~SquareB() ∧ ~TriangleB() ∧ CircleB())"
        ),
        ps("CircleT() → CircleT() ∧ SquareB()"),
        ps("TriangleB()"),
    )
    c: View = View.get_falsum()


class e40ii(BaseExample):
    """
    p120: The reader diverges from the default procedure,
    and deposes the conditional premise, and switches the premise
    order.
    """

    v: tuple[View, View, View] = (
        ps(
            "(SquareB() ∧ ~TriangleB() ∧ ~CircleB()) ∨ (~SquareB() ∧ TriangleB() ∧ ~CircleB()) ∨ (~SquareB() ∧ ~TriangleB() ∧ CircleB())"
        ),
        ps("TriangleB()"),
        ps("CircleT() → CircleT() ∧ SquareB()"),
    )
    c: View = ps("~SquareB() ∧ TriangleB() ∧ ~CircleB() ∧ ~CircleT()")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0]
            .update(cls.v[1], verbose=verbose)
            .update(cls.v[2].depose(verbose=verbose), verbose=verbose)
            .factor(View.get_falsum(), verbose=verbose)
        )

        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected result: {cls.c} but received {result}")


class e41(DefaultInference, BaseExample):
    """
    Example 41

    P1 P only if Q.
    P2 Not Q.
    C Not P.
    """

    v: tuple[View, View] = (
        ps("(~Q(q())) → (~Q(q()) ∧ ~P(p()))"),
        ps("~Q(q())"),
    )
    c: View = ps("~P(p())")


class e42(DefaultInference, BaseExample):
    """
    Example 42, p122

    P1 There is a circle at the top of the card only if there is a square
    at the bottom.
    P2 There is not a square at the bottom
    C There is not a circle at the top
    """

    v: tuple[View, View] = (
        ps("~SquareB() → ~CircleT() ∧ ~SquareB()"),
        ps("~SquareB()"),
    )
    c: View = ps("~CircleT()")


# e43 is not an example


class e44_1(DefaultInference, BaseExample):
    """
    Example 44-1

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    """

    v: tuple[View, View, View] = (
        ps("(Saleable(c()) ∧ Elegant(c())) ∨ (~Saleable(c()) ∧ ~Elegant(c()))"),
        ps("(Elegant(c()) ∧ Stable(c())) ∨ (~Elegant(c()) ∧ ~Stable(c()))"),
        ps("Saleable(c()) ∨ Stable(c()) ∨ (Saleable(c()) ∧ Elegant(c()))"),
    )
    c: View = ps("Saleable(c()) ∧ Elegant(c()) ∧ Stable(c())")


class e45(BaseExample):
    """
    Example 45

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    """

    v: tuple[View, View, View] = (ps("M() ∨ ⊤"), ps("B() ∨ ⊤"), ps("(M() ∧ B()) ∨ ⊤"))
    c: tuple[View, View] = (ps("(M() ∧ B()) ∨ M() ∨ B() ∨ ⊤"), ps("(M() ∧ B()) ∨ ⊤"))

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = cls.v[0].product(cls.v[1])

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = mid_result.query(cls.v[2], verbose=verbose)

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e46i(BaseExample):
    """
    Example 46

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    """

    v: tuple[View, View, View] = (
        ps("P() → P() ∧ V()"),
        ps("(M() ∧ ~P()) ∨ (P() ∧ ~M())"),
        ps("(V() ∧ M()) ∨ ⊤"),
    )
    c: tuple[View, View] = (ps("(P() ∧ V() ∧ ~M()) ∨ (~P() ∧ M())"), ps("⊤"))

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[0]
            .depose(verbose=verbose)
            .update(cls.v[1], verbose=verbose)
            .factor(View.get_falsum(), verbose=verbose)
        )

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = mid_result.query(cls.v[2], verbose=verbose)

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")

    class e46ii(Query, BaseExample):
        """
        p126, if we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
        """

        v: tuple[View, View] = (
            ps("(V() ∧ M() ∧ R()) ∨ (V() ∧ M() ∧ S()) ∨ T()"),
            ps("(V() ∧ M()) ∨ ⊤"),
        )
        c: View = ps("(V() ∧ M()) ∨ ⊤")


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
    C Truth
    """

    v: tuple[View, View] = (
        ps("∃x D(x*) ∧ T(x)"),
        ps("~D(Turgidum()*)"),
    )
    c: View = ps("⊤")


class e49(DefaultInference, BaseExample):
    """
    Example 49

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    """

    v: tuple[View, View] = (
        ps("∃x ∃y Ace(Mary()) ∧ King(x) ∨ Queen(John()) ∧ Jack(y)"),
        ps("King(Sally())"),
    )
    c: View = ps("⊤")


class e50_part1(BaseExample):
    v: tuple[View, View, View, View] = (
        ps("L(j(), s()) ∧ L(s(), g())"),
        ps("M(j()*) ∧ ~M(g()*)"),
        ps("⊥"),
        ps("∃a ∃b L(a, b) ∧ M(a*) ∧ ~M(b*)"),
    )
    c: tuple[View, View] = (
        ps("L(j(), s()) ∧ L(s(), g()) ∧ M(j()*) ∧ ~M(g()*)"),
        ps("⊤"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[0].update(cls.v[1], verbose=verbose).factor(cls.v[2], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )
        result = mid_result.query(cls.v[3], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e50_part2(BaseExample):
    v: tuple[View, View, View, View] = (
        ps("L(j(), s()) ∧ L(s(), g())"),
        ps("M(j()) ∧ ~M(g())"),
        ps("M(s())"),
        ps("∃a ∃b L(a, b) ∧ M(a*) ∧ ~M(b*)"),
    )
    g1: View = ps(
        "(L(j(), s()) ∧ L(s(), g()) ∧ M(j()) ∧ ~M(g()) ∧ M(s())) ∨ (L(j(), s()) ∧ L(s(), g()) ∧ M(j()) ∧ ~M(g()) ∧ ~M(s()))"
    )
    g2: View = ps(
        "(L(j(), s()) ∧ L(s(), g()) ∧ M(j()*) ∧ ~M(g()*) ∧ M(s()*)) ∨ (L(j(), s()) ∧ L(s(), g()) ∧ M(j()*) ∧ ~M(g()*) ∧ ~M(s()*))"
    )

    c: View = ps("∃a ∃b L(a, b) ∧ M(a*) ∧ ~M(b*)")

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[0]
            .update(cls.v[1], verbose=verbose)
            .inquire(cls.v[2], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.g1):
            raise RuntimeError(
                f"Expected mid result: {cls.g1} but received {mid_result}"
            )

        # Should use reorient once this exists
        result = cls.g2.query(cls.v[3], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


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


class e52(BasicStep, BaseExample):
    """
    Example 52

    P1 All Fs G.
    P2 John Gs.
    C John Fs and Gs.
    """

    v: tuple[View, View] = (
        ps("∀x (F(x)) → (F(x) ∧ G(x*))"),
        ps("G(John()*)"),
    )
    c: View = ps("F(John()) ∧ G(John()*)")


class e53(BaseExample):
    """
    Example 53, page 132 & page 175

    P All A are B.
    C All B are A.
    """

    v: tuple[View, View, View] = (
        ps("∀x A(x) → A(x) ∧ B(x)"),
        ps("∀x B(x)"),
        ps("∀x B(x) → A(x) ∧ B(x)"),
    )
    c: View = ps("∀x B(x) → A(x) ∧ B(x)")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0]
            .depose(verbose=verbose)
            .suppose(cls.v[1], verbose=verbose)
            .query(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e54(BasicStep, BaseExample):
    """
    Example 54

    P1 Sharks attack bathers.
    P2 Whitey is a shark.
    C Whitey attacks bathers.
    """

    v: tuple[View, View] = (
        ps("∀x (Shark(x*)) → ((Shark(x) ∧ Attack(x)) ∨ ⊤)"),
        ps("Shark(Whitey()*)"),
    )
    c: View = ps("Attack(Whitey()) ∧ Shark(Whitey()*)")


# class e55(BasicStep, BaseExample):
#     """
#     Example 55

#     P1 Montreal is north of New York
#     C New York is south of Montreal

#     Secret geographical premise: X north of Y implies Y south of X
#     """

#     v: tuple[View, View] = (
#         ps("North(Montreal(), NewYork())"),
#         ps("∀x ∀y North(x, y) → North(x, y) ∧ South(y, x)"),
#     )
#     c: View = ps("North(Montreal(), NewYork()) ∧ South(NewYork(), Montreal())")


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


class e57(BasicStep, BaseExample):
    """
    Example 57

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    """

    v: tuple[View, View] = (
        ps("∀x (B(x*)) → (B(x) ∧ A(x))"),
        ps("∃x C(x) ∧ B(x*)"),
    )
    c: View = ps("∃y A(y) ∧ B(y*) ∧ C(y)")


class e58_reversed(BasicStep, BaseExample):
    """
    Example 58 reversed

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    """

    v: tuple[View, View] = (
        ps("∀y (C(y)) → C(y) ∧ B(y*)"),
        ps("∃x B(x*) ∧ A(x)"),
    )
    c: View = ps("∃y C(y) ∧ A(y) ∧ B(y*)")


class e61(BasicStep, BaseExample):
    """
    Example 61
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    """

    v: tuple[View, View] = (ps("∀x ∃a D(x) ∧ B(x, a) ∧ M(a*) ∨ ~D(x)"), ps("M(j()*)"))
    c: View = ps(
        "∀x ∃a ((M(j()*) ∧ ~D(x)) ∨ (M(j()*) ∧ D(x) ∧ M(a*) ∧ B(x, a)))"
    )  # TODO: Make example better?


class e62(WHQuery, BaseExample):
    """
    Example 62, page 176
    """

    v = (
        ps(
            "(S(j()*) ∧  D(m()) ∧ T(n())) ∨ (S(m()*) ∧ L(n(),m())) ∨ (~S(n()*) ∧ D(b()))"
        ),
        ps("∃a S(a*)"),
    )
    c = ps("S(j()*) ∨ S(m()*) ∨ ⊤")


class e63(WHQuery, BaseExample):
    """
    Example 63, page 176
    """

    v = (
        ps("(S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(n()*))"),
        ps("∃a D(a*)"),
    )
    c = ps("D(n()*)")


class e63_modified(WHQuery, BaseExample):
    """
    Example 63, page 176
    """

    v = (
        ps("∀x ∃y (S(j()*) ∧  D(n()*)) ∨ (T(j()) ∧ ~D(j()*) ∧ D(f(y, x)*))"),
        ps("∃a D(a*)"),
    )
    c = ps("∀x ∃y (D(f(y,x)*) ∨ D(n()*))")


class UniProduct(BaseExample):
    v = (ps("∀x ∃a (P(x*) ∧ E(x,a)) ∨ ~P(x)"), ps("P(j()*)"))
    c: View = ps("∃a (P(j()*) ∧ E(j(),a)) ∨ ~P(j())")

    @classmethod
    def test(cls):
        result = cls.v[0].universal_product(cls.v[1])
        assert result.is_equivalent_under_arb_sub(cls.c)


class QueryTest(Query, BaseExample):
    """
    From page 173
    """

    v = (
        ps("∀x (T(x, j()) ∧ S(j()*) ∧ S(m()*)) ∨ (T(x, m()) ∧ S(j()*) ∧ S(m()*))"),
        ps("∀x ∃a T(x, a) ∧ S(a*)"),
    )
    c = ps("∀x ∃a T(x, a) ∧ S(a*)")


class QueryTest2(Query, BaseExample):
    """
    From page 173
    """

    v = (
        ps("∀x (T(x, j()) ∧ S(j()*) ∧ S(m()*)) ∨ (T(x, m()) ∧ S(j()*) ∧ S(m()*))"),
        ps("∃a ∀x T(x, a) ∧ S(a*)"),
    )
    c = ps("∀x ∃a T(x, a) ∧ S(a*)")


# Example 18
