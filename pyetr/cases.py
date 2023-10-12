__all__ = ["BaseExample"]
from abc import ABCMeta, abstractmethod
from typing import cast

from pyetr.atoms.terms.function import RealNumber
from pyetr.atoms.terms.term import FunctionalTerm

from .func_library import log_func, power_func
from .inference import basic_step, default_decision, default_inference_procedure
from .new_parsing import parse_string_to_view as ps
from .view import View


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
        ...


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
        result = basic_step(v=cls.v, verbose=verbose)
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
        result = cls.v[0].which(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Suppose(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].suppose(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class DefaultDecision(BaseTest):
    v: tuple[View]
    cv: tuple[View, ...]
    pr: tuple[View, ...]
    c: View

    @classmethod
    def test(cls, verbose: bool = False):
        result = default_decision(dq=cls.v[0], cv=cls.cv, pr=cls.pr, verbose=verbose)
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
            "{KneelingByTheFire(Jane())LookingAtTV(Jane()), PeeringIntoTheGarden(Mark())StandingAtTheWindow(Mark())}"
        ),
        ps("{KneelingByTheFire(Jane())}"),
    )
    c: View = ps("{LookingAtTV(Jane())}")


class e2(DefaultInference, BaseExample):
    """
    Example 2 (p. 62):

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    """

    v: tuple[View, View] = (
        ps("{T(w())K(z()),Q(y())A(x())}"),
        ps("{K(z())}"),
    )
    c: View = ps("{T(w())}")


class e3(DefaultInference, BaseExample):
    """
    Example 3 (p.63):

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("{King(k())Ace(a()),Jack(j())Queen(q())}"),
        ps("{~Ace(a())}"),
    )
    c: View = ps("{Jack(j())Queen(q())}")


# e4 is not a test


class samples:
    gamma = "p1()q1()"
    delta = "r1()s1()"
    epsilon = "p2()q2()"
    theta = "s2()r2()"


class e5ii(Product, BaseExample):
    v: tuple[View, View] = (
        ps("{" + f"{samples.delta},{samples.gamma}" + "}"),
        ps("{" + f"{samples.epsilon},{samples.theta}" + "}"),
    )
    c: View = ps(
        "{p2()r1()q2()s1(),s2()r1()r2()s1(),s2()p1()q1()r2(),p2()p1()q1()q2()}"
    )


class e5iii(Product, BaseExample):
    v: tuple[View, View] = (
        ps("{" + f"{samples.gamma}, {samples.delta}" + "}"),
        View.get_falsum(),
    )
    c: View = View.get_falsum()


class e5iv(Product, BaseExample):
    v: tuple[View, View] = (
        ps("{" + f"{samples.gamma}, {samples.delta}" + "}"),
        View.get_verum(),
    )
    c: View = ps("{" + f"{samples.gamma}, {samples.delta}" + "}")


class e5v(Product, BaseExample):
    v: tuple[View, View] = (
        View.get_verum(),
        ps("{" + f"{samples.gamma}, {samples.delta}" + "}"),
    )
    c: View = ps("{" + f"{samples.gamma}, {samples.delta}" + "}")


class e6(Product, BaseExample):
    """
    Example 6, p72

    There is an Ace and a King = (There is an Ace) x (There is a king)
    """

    v: tuple[View, View] = (ps("{a()}"), ps("{k()}"))
    c: View = ps("{a()k()}")


class e7(Sum, BaseExample):
    """
    Example 7, p73

    There is an Ace or there is a king = (There is an Ace) + (There is a king)
    """

    v: tuple[View, View] = (ps("{a()}"), ps("{k()}"))
    c: View = ps("{a(),k()}")


class e8(DefaultInference, BaseExample):
    """
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    """

    v: tuple[View, View] = (ps("{t()k(),a()q()}"), ps("{k()}"))
    c: View = ps("{t()}")


class e10(DefaultInference, BaseExample):
    """
    Example 10 (p.76)

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a ten.
    """

    v: tuple[View, View] = (
        ps("{K(x())}"),
        ps("{T(w())K(z()),Q(y())A(x())}"),
    )
    c: View = ps("{0}")


class e11(BasicStep, BaseExample):
    """
    Example 11 (p. 77)

    P1 Either John smokes or Mary smokes.
    P2 Supposing John smokes, John drinks.
    P3 Supposing Mary smokes, Mary eats.
    C Either John smokes and drinks or Mary smokes and drinks.
    """

    v: tuple[View, View, View] = (
        ps("{Smokes(j()),Smokes(m())}"),
        ps("{Drinks(j())}^{Smokes(j())}"),
        ps("{Eats(m())}^{Smokes(m())}"),
    )
    c: View = ps("{Smokes(j())Drinks(j()),Eats(m())Smokes(m())}")


class e12i(Negation, BaseExample):
    """
    Example 12i (p. 78)

    ItisnotthecasethatPorQorR
    """

    v: tuple[View] = (ps("{P(p()),Q(q()),R(r())}"),)
    c: View = ps("{~R(r())~Q(q())~P(p())}")


class e12ii(Negation, BaseExample):
    """
    Example 12ii (p. 78)

    ItisnotthecasethatPandQandR
    """

    v: tuple[View] = (ps("{P(p())R(r())Q(q())}"),)
    c: View = ps("{~R(r()),~P(p()),~Q(q())}")


class e12iii(Negation, BaseExample):
    """
    Example 12iii (p. 79)

    It is not the case that, supposing S, ((P and Q) or R)
    """

    v: tuple[View] = (ps("{P(p())Q(q()),R(r())}^{S(s())}"),)
    c: View = ps("{~P(p())S(s())~R(r()),~R(r())~Q(q())S(s())}")


class e13(DefaultInference, BaseExample):
    """
    Example 13 (p. 80)

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("{IsQueen(q())IsJack(j()),IsAce(a())IsKing(k())}"),
        ps("{~IsAce(a())}"),
    )
    c: View = ps("{IsQueen(q())IsJack(j())}")


class e14_1(Factor, BaseExample):
    """
    Example 14-1(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("{P(p())R(r()),P(p())Q(q())}"),
        ps("{P(p())}"),
    )
    c: View = ps("{Q(q()),R(r())}")


class e14_2(Factor, BaseExample):
    """
    Example 14-2(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("{P(p())R(r()),P(p())S(s())R(r()),P(p())S(s())Q(q())}"),
        ps("{P(p())}^{S(s())}"),
    )
    c: View = ps("{Q(q())S(s()),P(p())R(r()),S(s())R(r())}")


class e14_3(Factor, BaseExample):
    """
    Example 14-3(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("{P(p())S(s()),Q(q())S(s()),P(p())R(r()),Q(q())R(r())}"),
        ps("{P(p()),Q(q())}"),
    )
    c: View = ps("{S(s()),R(r())}")


class e14_6(Factor, BaseExample):
    """
    Example 14-6(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("{Q(q())S(s()),P(p())R(r())}"),
        ps("{T(t()),P(p()),Q(q())}"),
    )
    c: View = ps("{Q(q())S(s()),P(p())R(r())}")


class e14_7(Factor, BaseExample):
    """
    Example 14-7(p. 81) Factor examples
    """

    v: tuple[View, View] = (
        ps("{Q(q())S(s()),P(p())R(r()),P(p())}"),
        ps("{P(p()),Q(q())}"),
    )
    c: View = ps("{0,S(s()),R(r())}")


class e15(DefaultInference, BaseExample):
    """
    Example 15

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    """

    v: tuple[View, View, View] = (
        ps("{Ace(a()),Jack(j())Queen(q())Ace(a()),Four(f())Ten(t())Eight(e())}"),
        ps("{Jack(j())Ten(t())Ace(a())Eight(e())}"),
        ps("{~Queen(q())}"),
    )
    c: View = ps("{Four(f())}")


class e16(DefaultInference, BaseExample):
    """
    Example 16

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    """

    v: tuple[View, View, View] = (
        ps("{King(k())Jack(j())Queen(q()),Ace(a()),Four(f())Ten(t())Eight(e())}"),
        ps("{~Four(f())}"),
        ps("{~Ace(a())}"),
    )
    c: View = ps("{King(k())Jack(j())Queen(q())}")


class e17(DefaultInference, BaseExample):
    """
    Example 17

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    """

    v: tuple[View, View] = (
        ps("{~King(k())Ace(a()),King(k())~Ace(a())}"),
        ps("{King(k())}"),
    )
    c: View = ps("{~Ace(a())}")


class e19(Suppose, BaseExample):
    """
    Example 19, page 84

    Suppose test
    """

    v: tuple[View, View] = (
        ps("{0}"),
        ps("{~N()}"),
    )
    c: View = ps("{~N()}^{~N()}")


class e20(DefaultInference, BaseExample):
    """
    Example 20

    P1 Either there is a king in the hand or a queen in the hand.
    P2 On the supposition that there is a king, Mary wins.
    P3 On the supposition that there is a queen, Bill wins.
    C Either Mary wins or Bill wins.
    """

    v: tuple[View, View, View] = (
        ps("{Queen(q()),King(k())}"),
        ps("{Win(mary())}^{King(k())}"),
        ps("{Win(bill())}^{Queen(q())}"),
    )
    c: View = ps("{Win(bill()),Win(mary())}")


class e21(BaseExample):
    """
    Example 21
    """

    v: tuple[View] = (ps("{" + f"{samples.delta}" + "}"),)
    c: View = ps("{" + f"{samples.delta}" + "}").negation()

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
        ps("{a()c()b()}"),
        ps("{a()}"),
        ps("{b()}"),
        ps("{c()}"),
    )
    c: tuple[View, View] = (
        ps("{~c(),~b(),~a()}"),
        ps(
            "{~c()a()~b(),~c()~a()~b(),~c()~a()b(),~c()a()b(),a()~b()c(),~a()c()b(),~a()~b()c()}"
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

    v: tuple[View, View] = (ps("{L()K(),P()S()}"), ps("{K()}"))
    c: tuple[View, View] = (
        ps("{P()S()~K(),L()K(),P()S()K()}"),
        ps("{L()K(),P()S()K()}"),
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
    v: tuple[View, View] = (ps("{L()K(),P()S()}"), ps("{K()}"))
    c: tuple[View, View] = (
        ps("{L()K(),P()S()}"),
        ps("{L()K()}"),
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

    v: tuple[View, View] = (ps("{a()}"), ps("{q()}"))
    c: tuple[View, View] = (ps("{a()~q(),a()q()}"), ps("{a(),q()}"))

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

    v: tuple[View, View] = (ps("{p()r(),p()q()}"), ps("{p()}"))
    c: View = ps("{p()}")


class e25ii(Query, BaseExample):
    """
    Example 25ii
    """

    v: tuple[View, View] = (ps("{p()r(),p()q()}"), ps("{q()}"))
    c: View = ps("{0,q()}")


class e25iii(Query, BaseExample):
    """
    Example 25iii
    """

    v: tuple[View, View] = (
        ps("{t(),p()r(),p()q(),s()}"),
        ps("{p(),s()}"),
    )
    c: View = ps("{0,p(),s()}")


class e25iv(Query, BaseExample):
    """
    Example 25iv
    """

    v: tuple[View, View] = (
        ps("{t(),p()r(),p()q(),s()}"),
        ps("{t(),p(),s()}"),
    )
    c: View = ps("{t(),p(),s()}")


class e25v(Query, BaseExample):
    """
    Example 25v
    """

    v: tuple[View, View] = (
        ps("{s()p()q(),p()r()s()}"),
        ps("{p()}^{s()}"),
    )
    c: View = ps("{p()}")


class e25vi(Query, BaseExample):
    """
    Example 25vi
    """

    v: tuple[View, View] = (
        ps("{s()p()q(),p()r()s()}"),
        ps("{p()}^{t()}"),
    )
    c: View = View.get_verum()


class e26(BaseExample):
    """
    Example 26

    P1 Either John plays and wins, or Mary plays, or Bill plays
    C Supposing John plays, John wins
    """

    v: tuple[View, View, View] = (
        ps("{Play(J())Win(J()),Play(B()),Play(M())}"),
        ps("{Play(J())}"),
        ps("{Win(J())}^{Play(J())}"),
    )
    c: tuple[View, View] = (
        ps("{Play(J())Win(J())}^{Play(J())}"),
        ps("{Win(J())}^{Play(J())}"),
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
        ps("{~Tiger(t()),Tiger(t())}"),
        ps("{Orange(o())Tiger(t())}^{Tiger(t())}"),
        ps("{Orange(o())}"),
    )
    c: View = ps("{Tiger(t())}")


class e32_1(DefaultInference, BaseExample):
    """
    Example 32-1

    P1 If P then Q.
    P2 P
    C Q
    """

    v: tuple[View, View] = (
        ps("{P(p())Q(q())}^{P(p())}"),
        ps("{P(p())}"),
    )
    c: View = ps("{Q(q())}")


class e32_2(DefaultInference, BaseExample):
    """
    Example 32-2

    P1 P
    P2 If P then Q.
    C Q
    """

    v: tuple[View, View] = (
        ps("{P(p())}"),
        ps("{P(p())Q(q())}^{P(p())}"),
    )
    c: View = ps("{Q(q())}")


class e33(DefaultInference, BaseExample):
    """
    Example 33

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    """

    v: tuple[View, View] = (
        ps("{E(e())R(r())}^{R(r())}"),
        ps("{E(e())}"),
    )
    c: View = ps("{R(r())}")


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
            "{~CircleB()~TriangleB()SquareB(),CircleB()~TriangleB()~SquareB(),~CircleB()TriangleB()~SquareB()}"
        ),
        ps("{CircleT()SquareB()}^{CircleT()}"),
        ps("{TriangleB()}"),
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
            "{~CircleB()~TriangleB()SquareB(),CircleB()~TriangleB()~SquareB(),~CircleB()TriangleB()~SquareB()}"
        ),
        ps("{TriangleB()}"),
        ps("{CircleT()SquareB()}^{CircleT()}"),
    )
    c: View = ps("{~CircleB()~CircleT()TriangleB()~SquareB()}")

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
        ps("{~Q(q())~P(p())}^{~Q(q())}"),
        ps("{~Q(q())}"),
    )
    c: View = ps("{~P(p())}")


class e42(DefaultInference, BaseExample):
    """
    Example 42, p122

    P1 There is a circle at the top of the card only if there is a square
    at the bottom.
    P2 There is not a square at the bottom
    C There is not a circle at the top
    """

    v: tuple[View, View] = (
        ps("{~CircleT()~SquareB()}^{~SquareB()}"),
        ps("{~SquareB()}"),
    )
    c: View = ps("{~CircleT()}")


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
        ps("{Saleable(c())Elegant(c()),~Elegant(c())~Saleable(c())}"),
        ps("{~Stable(c())~Elegant(c()),Stable(c())Elegant(c())}"),
        ps("{Saleable(c())Elegant(c()),Stable(c()),Saleable(c())}"),
    )
    c: View = ps("{Stable(c())Saleable(c())Elegant(c())}")


class e45(BaseExample):
    """
    Example 45

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    """

    v: tuple[View, View, View] = (ps("{0,M()}"), ps("{0,B()}"), ps("{0,B()M()}"))
    c: tuple[View, View] = (ps("{0,M(),B(),B()M()}"), ps("{0,B()M()}"))

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
        ps("{V()P()}^{P()}"),
        ps("{~P()M(),P()~M()}"),
        ps("{0,V()M()}"),
    )
    c: tuple[View, View] = (ps("{~P()M(),V()P()~M()}"), ps("{0}"))

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
        ps("{V()S()M(),V()R()M(),T()}"),
        ps("{0,V()M()}"),
    )
    c: View = ps("{0,V()M()}")


class e47(DefaultInference, BaseExample):
    """
    P1: Some thermotogum stains gram-negative
    P2: Maritima is a thermotogum

    C: Maritima stains gram negative
    """

    v: tuple[View, View] = (
        ps("∃x {StainsGramNegative(x)Thermotogum(x*)}"),
        ps("{Thermotogum(Maritima()*)}"),
    )
    c: View = ps("{StainsGramNegative(Maritima())}")


class e48(DefaultInference, BaseExample):
    """
    P1 Some dictyoglomus is thermophobic.
    P2 Turgidum is not a dictyoglomus.
    C Truth
    """

    v: tuple[View, View] = (
        ps("∃x {D(x*)T(x)}"),
        ps("{~D(Turgidum()*)}"),
    )
    c: View = ps("{0}")


class e49(DefaultInference, BaseExample):
    """
    Example 49

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    """

    v: tuple[View, View] = (
        ps("∃x ∃y {Ace(Mary())King(x),Queen(John())Jack(y)}"),
        ps("{King(Sally())}"),
    )
    c: View = ps("{0}")


class e50_part1(BaseExample):
    v: tuple[View, View, View, View] = (
        ps("{L(j(),s())L(s(),g())}"),
        ps("{M(j()*)~M(g()*)}"),
        ps("{}"),
        ps("∃b ∃a {M(a*)L(a,b)~M(b*)}"),
    )
    c: tuple[View, View] = (
        ps("{L(j(),s())M(j()*)~M(g()*)L(s(),g())}"),
        ps("{0}"),
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
        ps("{L(j(),s())L(s(),g())}"),
        ps("{M(j())~M(g())}"),
        ps("{M(s())}"),
        ps("∃b ∃a {M(a*)L(a,b)~M(b*)}"),
    )
    g1: View = ps(
        "{M(j())L(s(),g())L(j(),s())~M(g())M(s()),M(j())L(s(),g())L(j(),s())~M(g())~M(s())}"
    )
    g2: View = ps(
        "{M(j()*)L(s(),g())L(j(),s())~M(g()*)M(s()),M(j()*)L(s(),g())L(j(),s())~M(g()*)~M(s()*)}"
    )

    c: View = ps("∃b ∃a {M(a*)L(a,b)~M(b*)}")

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
        ps("∀x {IsArcheon(x*)HasNucleus(x)}^{IsArcheon(x*)}"),
        ps("{IsArcheon(Halobacterium()*)}"),
    )
    c: View = ps("{HasNucleus(Halobacterium())IsArcheon(Halobacterium()*)}")


class e52(BasicStep, BaseExample):
    """
    Example 52

    P1 All Fs G.
    P2 John Gs.
    C John Fs and Gs.
    """

    v: tuple[View, View] = (
        ps("∀x {F(x)G(x*)}^{F(x)}"),
        ps("{G(John()*)}"),
    )
    c: View = ps("{G(John()*)F(John())}")


class e53(BaseExample):
    """
    Example 53, page 132 & page 175

    P All A are B.
    C All B are A.
    """

    v: tuple[View, View, View] = (
        ps("∀x {A(x)B(x)}^{A(x)}"),
        ps("∀x {B(x)}"),
        ps("∀x {A(x)B(x)}^{B(x)}"),
    )
    c: View = ps("∀x {A(x)B(x)}^{B(x)}")

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
        ps("∀x {0,Shark(x*)Attack(x)}^{Shark(x*)}"),
        ps("{Shark(Whitey()*)}"),
    )
    c: View = ps("{Shark(Whitey()*)Attack(Whitey())}")


# class e55(BasicStep, BaseExample):
#     """
#     Example 55

#     P1 Montreal is north of New York
#     C New York is south of Montreal

#     Secret geographical premise: X north of Y implies Y south of X
#     """

#     v: tuple[View, View] = (
#         ps("{North(Montreal(),NewYork())}"),
#         ps("∀y ∀x {North(x,y)South(y,x)}^{North(x,y)}"),
#     )
#     c: View = ps("{North(Montreal(),NewYork())South(NewYork(),Montreal())}")


class e56_default_inference(DefaultInference, BaseExample):
    """
    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    """

    v: tuple[View, View] = (
        ps("∀x ∃y {Student(y*)Teaches(x,y)Professor(x)}^{Professor(x)}"),
        ps("∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}"),
    )
    c: View = ps("∃b ∃y {0,Book(b)Reads(y,b)}")


class e56_basic_step(BasicStep, e56_default_inference):
    c: View = ps(
        "∀a ∃c ∃b {Book(c)Student(b*)Professor(a)Teaches(a,b)Reads(b,c)}^{Professor(a)}"
    ).depose()


class e57(BasicStep, BaseExample):
    """
    Example 57

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    """

    v: tuple[View, View] = (
        ps("∀x {B(x*)A(x)}^{B(x*)}"),
        ps("∃x {B(x*)C(x)}"),
    )
    c: View = ps("∃y {A(y)C(y)B(y*)}")


class e58_reversed(BasicStep, BaseExample):
    """
    Example 58 reversed

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    """

    v: tuple[View, View] = (
        ps("∀y {B(y*)C(y)}^{C(y)}"),
        ps("∃x {B(x*)A(x)}"),
    )
    c: View = ps("∃y {A(y)C(y)B(y*)}")


class e61(BasicStep, BaseExample):
    """
    Example 61
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    """

    v: tuple[View, View] = (ps("∀x ∃a {~D(x),M(a*)D(x)B(x,a)}"), ps("{M(j()*)}"))
    c: View = ps(
        "∀x ∃a {M(j()*)M(a*)D(x)B(x,a),M(j()*)~D(x)}"
    )  # TODO: Make example better?


class e62(WHQuery, BaseExample):
    """
    Example 62, page 176
    """

    v = (
        ps("{L(n(),m())S(m()*),D(m())T(n())S(j()*),D(b())~S(n()*)}"),
        ps("∃a {S(a*)}"),
    )
    c = ps("{0,S(j()*),S(m()*)}")


class e63(WHQuery, BaseExample):
    """
    Example 63, page 176
    """

    v = (
        ps("{S(j()*)D(n()*),D(n()*)~D(j()*)T(j())}"),
        ps("∃a {D(a*)}"),
    )
    c = ps("{D(n()*)}")


class e63_modified(WHQuery, BaseExample):
    """
    Example 63, page 176
    """

    v = (
        ps("∀x ∃y {S(j()*)D(n()*),D(f(y,x)*)~D(j()*)T(j())}"),
        ps("∃a {D(a*)}"),
    )
    c = ps("∀x ∃y {D(n()*),D(f(y,x)*)}")


class e64i(BaseExample):
    """
    Example 64, p189, p223

    A device has been invented for screening a population for a disease known as psylicrapitis.
    The device is a very good one, but not perfect. If someone is a sufferer, there is a 90% chance
    that he will recorded positively. If he is not a sufferer, there is still a 1% chance that he will
    be recorded positively.

    Roughly 1% of the population has the disease. Mr Smith has been tested, and the result is positive.

    What is the chance that he is in fact a sufferer?
    """

    # TODO: Issues not in book - this isn't procedure in book, uses query instead of which
    # TODO: Note typo line 2 introduction of P
    v = (
        ps("∀x {90=* S(x*)T(x*), S(x)~T(x)}^{S(x)}"),
        ps("∀x {1=* ~S(x)T(x), ~S(x)~T(x)} ^ {~S(x*)}"),
        ps("{T(Smith()*)}"),
        ps("{S(Smith())}"),
    )
    c: View = ps("{90=* S(Smith()*), 0}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = basic_step(v=cls.v[0:3], verbose=verbose).query(
            cls.v[3], verbose=verbose
        )

        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e64ii(e64i):
    v = (
        ps("∀x {90=* P(x)S(x*)T(x*), P(x)S(x)~T(x)}^{P(x)S(x)}"),
        ps("∀x {1=* P(x)~S(x)T(x), P(x)~S(x)~T(x)} ^ {P(x)~S(x*)}"),
        ps("∀x {1=* P(x)S(x*), P(x)~S(x)} ^ {P(x)}"),
        ps("{P(Smith())T(Smith()*)}"),
        ps("{S(Smith())}"),
    )
    c: View = ps("{90=* S(Smith()*)}")

    # TODO: Why no 0 here? Should there be a 0 in 2nd atom?
    @classmethod
    def test(cls, verbose: bool = False):
        result = basic_step(v=cls.v[0:4], verbose=verbose).query(
            cls.v[4], verbose=verbose
        )

        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e65(BaseExample):
    """
    Example 65 p190, p224

    (Base-rate neglect with doctors and realistic disease) Imagine you conduct
    a screening using the hemoccult test in a certain region. For symptom-free
    people over 50 years old who participate in screening using the hemocult test,
    the following information is available for this region.

    The probability that one of these people has colorectal cancer is 0.3%. If a
    person has colorectal cancer, the probability is 50 that he will have a positive
    hemocult test. If a person does not have a colorectal cancer, the probability is
    3% that he will still have a positive hemoccult test in your screening. What is
    the probability that this person actually has colorectal cancer?
    """

    v = (
        ps("∀x {0.3=* P(x)C(x), P(x)~C(x)}^{P(x)}"),
        ps("∀x {50=* P(x)C(x)T(x),P(x)C(x)~T(x)}^{P(x)C(x)}"),
        ps("∀x {3=* P(x)~C(x)T(x),P(x)~C(x)~T(x)}^{P(x)~C(x)}"),
        ps("∃a {P(a)T(a)}"),
        ps("∃a ∀x {x=* C(a)}"),  # TODO: Specifically has no dep
    )
    c: View = ps("∃a {15=* C(a), 0}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0]
            .depose(verbose=verbose)
            .update(cls.v[1], verbose=verbose)
            .update(cls.v[2], verbose=verbose)
            .update(cls.v[3], verbose=verbose)
            .factor(View.get_falsum(), verbose=verbose)
            .which(cls.v[4], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e66i(BaseExample):
    """
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ? # TODO: Why this ?
    """

    v = (
        ps("{1=* D()T(), 1=* ~D()T(), 98=* ~D()}"),
        ps("{D()T()}"),
    )
    c: View = ps("{}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[1].stage, cls.v[0].weights
        )
        out = FunctionalTerm(f=RealNumber(num=1), t=())
        if not result == out:
            raise RuntimeError(f"Expected: {out} but received {result}")


class e66ii(e66i):
    v = (
        ps("{1=* D()T(), 1=* ~D()T(), 98=* ~D()}"),
        ps("{P()}"),
    )
    c: View = ps("{}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[1].stage, cls.v[1].weights
        )
        out = FunctionalTerm(f=RealNumber(num=2), t=())
        if not result == out:
            raise RuntimeError(f"Expected: {out} but received {result}")


class e67(BaseExample):
    """
    Example 67, p191, p220

    Results of a recent survey of seventy-four chief executive officers indicate there
    may be a link between childhood pet ownership and future career success. Fully 94%
    of the CEOs, all of them employed within Fortune 500 companies, had possessed a dog,
    a cat, or both, as youngsters.
    """

    v = (
        ps("{94=* IsCEO()HadPet(), HadPet()}"),
        ps("{HadPet()}"),
        ps("Ax {x=* IsCEO()}"),
    )
    c: View = ps("{94=* IsCEO()}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0].suppose(cls.v[1], verbose=verbose).which(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e69_part1(BasicStep, BaseExample):
    """
    Example 69, p192, p218

    The suspect's DNA matches the crime sample.

    If the suspect is not guilty, then the probability of such a DNA match is 1 in
    a million

    Is the suspect likely to be guilty?
    """

    v = (
        ps("{Match(Suspect())}"),
        ps(
            "{0.000001=* ~Guilty(Suspect())Match(Suspect()), ~Guilty(Suspect())~Match(Suspect())} ^ {~Guilty(Suspect())}"
        ),
    )
    c = ps(
        "{0.000001=* ~Guilty(Suspect())Match(Suspect()), Guilty(Suspect())~Match(Suspect())}"
    )


class e69_part2(BaseExample):
    v = (
        ps(
            "{0.000001=* ~Guilty(Suspect())Match(Suspect()), Guilty(Suspect())~Match(Suspect())}"
        ),
        ps("{999999.999999=* 0}^{Guilty(Suspect())Match(Suspect())}"),
        ps("Ax {x=* Guilty(Suspect())}"),
    )
    c: tuple[View, View] = (
        ps(
            "{0.000001=* ~Guilty(Suspect())Match(Suspect()), 999999.999999=* Guilt(Suspect())Match(Suspect())}"
        ),
        ps("{999999.999999=* Guilt(Suspect()), 0}"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = cls.v[0].inquire(cls.v[1], verbose=verbose)
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )
        result = mid_result.which(cls.v[2], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e70(BaseExample):
    """
    Example 70, p194, p221

    P1 Pat has either the disease or a benign condition
    P2 If she has the disease, then she will have a certain symptom.
    P3 In fact, she has the symptom
    """

    v = (
        ps("{Disease(), Benign()}"),
        ps("{Disease()Symptom()}^{Disease()}"),
        ps("{Symptom()}"),
    )
    c: View = ps("{Disease()}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0].update(cls.v[1], verbose=verbose).update(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e71(BaseExample):
    """
    Example 71, and 78, page 212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    """

    # TODO: Note typo on 212, By~Bb -> By~By
    v = (
        ps("{B(yellow())~B(brown()), ~B(yellow())B(brown())}"),
        ps("{50=* 0}^{B(yellow())~B(brown())}"),
        ps("{50=* 0}^{~B(yellow())B(brown())}"),
        ps("{B(yellow())~B(brown())}"),
    )
    c: tuple[View, View] = (
        ps("{50=* B(yellow())~B(brown()), 50=* ~B(yellow())B(brown())}"),
        ps("{50=* B(yellow())~B(brown()), 0}"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[0]
            .inquire(cls.v[1], verbose=verbose)
            .inquire(cls.v[2], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(f"Expected: {cls.c[0]} but received {mid_result}")

        result = mid_result.query(cls.v[3], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e72(BaseExample):
    """
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    """

    v = (
        ps("{B(g())B(b())~B(r()), B(r())~B(g()), B(r())~B(b())}"),
        ps("{33.333333=* 0} ^ {B(g())B(b())~B(r())}"),
        ps("{33.333333=* 0} ^ {B(r())~B(g())}"),
        ps("{33.333333=* 0} ^ {B(r())~B(b())}"),
        ps("{B(r())B(b())}"),
    )
    c: tuple[View, View] = (
        ps(
            "{33.333333=* B(g())B(b())~B(r()), 33.333333=* B(r())~B(g()), 33.333333=* B(r())~B(b())}"
        ),
        ps("{33.333333=* B(r())B(b()), 0}"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[0]
            .inquire(cls.v[1], verbose=verbose)
            .inquire(cls.v[2], verbose=verbose)
            .inquire(cls.v[3], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(f"Expected: {cls.c[0]} but received {mid_result}")

        result = mid_result.query(cls.v[4], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e74(BaseExample):
    """
    Example 74, p197, p231

    (includes two background commitments)
    """  # TODO: Note typo with brackets in book, p231

    v = (
        ps("Ej {D(j)H(j),H(j),P(j)}"),
        ps("Ej {E(j)}"),
        ps("Ax {0.85=* E(x)D(x), 0.15=* E(x)~D(x)} ^ {E(x)}"),
        ps("Ax {0.1=* E(x)H(x), 0.9=* E(x)~H(x)} ^ {E(x)}"),
    )
    c: tuple[View, View] = (
        ps(
            "Ej {0.85**0.1=* E(j)D(j)H(j), 0.85**0.9=* E(j)D(j)~H(j), 0.15**0.1=* E(j)~D(j)H(j), 0.15**0.9=* E(j)~D(j)~H(j)}"
        ),
        ps("Ej {D(j)H(j)}"),
    )

    @classmethod
    def test(cls, verbose: bool = False):
        mid_result = (
            cls.v[1].update(cls.v[2], verbose=verbose).update(cls.v[3], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        # Should use reorient once this exists
        result = cls.v[0].update(mid_result, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e76(DefaultInference, BaseExample):
    """
    Example 76 (guns and guitars)
    p199, p226

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    """  # TODO: Note assuming exists i

    v = (
        ps("Ei Ej {Fired(i)Gun(i)Guitar(j)Outoftune(j)}"),
        ps("Ax {Gun(x)Trigger(x)Fired(x)}^{Gun(x)Trigger(x)}"),
        ps("Ei {Trigger(i)}"),
    )
    c: View = ps("Ei Ej {Fired(i)Gun(i)Guitar(j)Outoftune(j)Trigger(i)}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0].update(cls.v[1], verbose=verbose).update(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e81_base:
    """
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    """


class e81i(e81_base):
    """
    In the box there is at least a yellow card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    # TODO: Add test
    # v = (
    #     ps("{50=* Box(Yellow()),50=* Box(Brown())}"),
    #     ps("{Box(Yellow())}")
    # )
    # c = ps("{50=* Box(Yellow())}")


class e81ii(e81_base):
    """
    In the box there is a yellow card and a brown card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e81iii(e81_base):
    """
    In the box there is neither a yellow card nor a brown card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e82_base:
    """
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    """


class e82i(e82_base):
    """
    In the box there is at least a yellow card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e82ii(e82_base):
    """
    In the box there is a yellow card and a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e82iii(e82_base):
    """
    In the box there is a yellow card and there is not a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e82iv(e82_base):
    """
    In the box there is neither a yellow card nor a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    # TODO: Add test


class e83i:
    """
    Example 83, p214

    There is a box in which there is at least a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability there is a red marble and blue in marble in the box?
    """

    # TODO: Add test


class e83ii:
    """
    Example 83, p214

    There is a box in which there is at least a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability there is a green marble and there is a blue marble?
    """

    # TODO: Add test


class e84i:
    """
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    """

    # TODO: Add test


class e84ii:
    """
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or
    else a mauve marble, but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    """

    # TODO: Add test


class e85:
    """
    Example 85, p216

    Easy partial probability inference

    There is a box in which there is one and only one of these marbles: a
    green marble, a blue marble, or a red marble. The probability that a green
    marble is in the box is 0.6, and the probability that a blue marble is in
    the box is 0.2.

    What is the probability that a red marble is in the box?
    """

    # TODO: Add test


class e86:
    """
    Example 86, p217

    You have a hand of several cards with only limited information about it.

    There is an ace and a queen or a kind and a jack or a ten.
    The probability that there is an ace and a queen is 0.6
    The probability that there is a king and a jack is 0.2

    What is the probability that there is a ten?
    """

    # TODO: Add test


class e88(BaseExample):
    """
    Example 88, p233

    P1: There is a 90% chance Superman can fly
    P2: Clark is superman

    C: There is a 90% chance Clark can fly
    """

    v: tuple[View, View, View] = (
        ps("{90=* CanFly(Superman())}"),
        ps("{==(Clark(), Superman())}"),
        ps("{==(Clark(), Superman()*)}"),
    )
    c: View = ps("{90=* CanFly(Clark())}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = (
            cls.v[0].update(cls.v[1], verbose=verbose).factor(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e90_condA(DefaultDecision, BaseExample):
    """
    Example 90, p249, p273

    Imagine that you have been saving some extra money on the side to make some purchases,
    and on your most recent visit to the video store you come across a special sale of a new
    video. This video is one with your favourite actor or actress, and your favourite type of
    movie (such as a comedy, drama, thriller etc.). This particular video that you are considering
    is one you have been thinking about buying a long time. It is a available at a special sale price
    of $14.99. What would you do in this situation?
    """  # TODO: Contradiction factor not show in book

    v = (ps("{do(Buy(Video()*)),~do(Buy(Video()))}"),)
    cv = (ps("Ax {Fun()}^{do(Buy(x*))}"),)
    pr = (ps("{1=+ 0} ^ {Fun()}"),)
    c = ps("{do(Buy(Video()*))}")


class e90_condB(e90_condA):
    v = (ps("Ea {do(Buy(Video()*)),do(Buy(a*))}"),)
    c = ps("Ea {do(Buy(Video()*)), do(Buy(a*))}")


class e92_base:
    """
    Example 92, p253, p274
    Imagine that you serve on the jury of an only-child sole-custody case following a relatively
    messy divorce. The facts of the case are compilicated by ambiguous economic, social, and
    emotional considerations, and you decide to base your decision entirely on the following
    few observations.

    ParentA: average income, average health, average working hours, reasonable rapport with the
    child, relatively social life.

    ParentB: above-average income, very close relationship with the child, extremely active
    social life, lots of work-related travel, minor health problems.

    """  # TODO: Contradiction factor not show in book

    cv = (
        ps("Ax {Custody(x)} ^ {do(Award(x))}"),
        ps("Ax {~Custody(x)} ^ {do(Deny(x))}"),
        ps(
            "{MedRapp(ParentA())MedTime(ParentA())HighRapp(ParentB())LowTime(ParentB())}"
        ),
    )
    pr = (
        ps("Ax {1=+ 0} ^ {Custody(x)MedRapp(x)}"),
        ps("Ax {3=+ 0} ^ {Custody(x)HighRapp(x)}"),
        ps("Ax {1=+ 0} ^ {Custody(x)MedTime(x)}"),
        ps(
            "Ax {1=+ 0} ^ {~Custody(x)MedTime(x)}"
        ),  # TODO: Thís is inverse of above - typo?
        ps("Ax {2=+ 0} ^ {~Custody(x)LowTime(x)}"),
    )


class e92_award(DefaultDecision, e92_base, BaseExample):
    """
    To which parent would you award sole custody of the child?
    """

    __doc__ = cast(str, e92_base.__doc__) + cast(str, __doc__)
    v = (ps("{do(Award(ParentA())), do(Award(ParentB()))}"),)

    c = ps("{do(Award(ParentB()))}")


class e92_deny(DefaultDecision, e92_base, BaseExample):
    """
    To which parent would you deny sole custody of the child?
    """

    __doc__ = cast(str, e92_base.__doc__) + cast(str, __doc__)
    v = (ps("{do(Deny(ParentA())), do(Deny(ParentB()))}"),)
    c = ps("{do(Deny(ParentB()))}")


class e93_grp1(DefaultDecision, BaseExample):
    """
    Example 93, p255, p276

    The US is preparing for the outbreak of an unusual Asian disease, which
    is expected to kill 600 people. There are two possible treatments (A) and (B)
    with the following results:

    (Group 1) (A) 400 people die. (B) Nobody dies with 1/3 chance, 600 people die with 2/3 chance.
    Which treatment would you choose?
    """

    v = (ps("{do(A()),do(B())}"),)
    pr = (
        ps(
            "Ax {power(++(1, log(++(1, x))), -1)=+ 0} ^ {D(x)}",
            custom_functions=[power_func, log_func],
        ),
        ps("Ax {++(1, log(++(1, x)))=+ 0} ^ {S(x)}", custom_functions=[log_func]),
    )
    cv = (
        ps("{D(400)} ^ {do(A())}"),
        ps("{0.33=* D(0.0), ~D(0.0)} ^ {do(B())}"),
        ps("{0.67=* D(600), ~D(600)} ^ {do(B())}"),
    )
    c = ps("{do(A())}")


class UniProduct(BaseExample):
    v = (ps("∀x ∃a {P(x)E(x,a),~P(x*)}"), ps("{P(j()*)}"))
    c: View = ps("∃a {~P(j()*),P(j())E(j(),a)}")

    @classmethod
    def test(cls, verbose: bool = False):
        result = cls.v[0].universal_product(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class QueryTest(Query, BaseExample):
    """
    From page 173
    """

    v = (
        ps("∀x {T(x,m())S(m()*)S(j()*),T(x,j())S(m()*)S(j()*)}"),
        ps("∀x ∃a {T(x,a)S(a*)}"),
    )
    c = ps("∀x ∃a {T(x,a)S(a*)}")


class QueryTest2(Query, BaseExample):
    """
    From page 173
    """

    v = (
        ps("∀x {T(x,m())S(m()*)S(j()*),T(x,j())S(m()*)S(j()*)}"),
        ps("∃a ∀x {T(x,a)S(a*)}"),
    )
    c = ps("∀x ∃a {T(x,a)S(a*)}")
