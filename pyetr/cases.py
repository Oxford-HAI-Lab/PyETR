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


class e44_1(DefaultInference, BaseExample):
    """
    Example 44-1

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    """

    v: tuple[View, View, View] = (
        ps("(Saleable(c()) ∧ Elegant(c())) ∨ (~Saleable(c()) ∧ ~Elegant(c())) "),
        ps("(Elegant(c()) ∧ Stable(c())) ∨ (~Elegant(c()) ∧ ~Stable(c()))"),
        ps("Saleable(c()) ∨ Stable(c()) ∨ (Saleable(c()) ∧ Elegant(c()))"),
    )
    c: View = ps("Saleable(c()) ∧ Elegant(c()) ∧ Stable(c())")


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
        # TODO: The book here is probably incorrect, so have updated to be truth as output
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
