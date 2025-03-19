__all__ = [
    "e1",
    "e2",
    "e3",
    "e5ii",
    "e5iii",
    "e5iv",
    "e5v",
    "e6",
    "e7",
    "e8",
    "e10",
    "e11",
    "e12i",
    "e12ii",
    "e12iii",
    "e13",
    "e14_1",
    "e14_2",
    "e14_3",
    "e14_6",
    "e14_7",
    "e15",
    "e16",
    "e17",
    "e19",
    "e20",
    "e21",
    "e22",
    "e23_with_inquire",
    "e23_without_inquire",
    "e24",
    "e25i",
    "e25ii",
    "e25iii",
    "e25iv",
    "e25v",
    "e25vi",
    "e26",
    "e26_does_it_follow",
    "e28",
    "e32_1",
    "e32_2",
    "e33",
    "e40i",
    "e40ii",
    "e41",
    "e42",
    "e44_1",
    "e45",
    "e46i",
    "e46ii",
    "e47",
    "e48",
    "e49",
    "e50_part1",
    "e50_part2",
    "e50_part2_arbs",
    "e51",
    "e52",
    "e53",
    "e53_does_it_follow",
    "e54",
    "e56_default_inference",
    "e56_basic_step",
    "e57",
    "e58_reversed",
    "e61",
    "e62",
    "e63",
    "e63_modified",
    "e64i",
    "e64ii",
    "e65",
    "e66i",
    "e66ii",
    "e67",
    "e69_part1",
    "e69_part2",
    "e70",
    "e71",
    "e72",
    "e74",
    "e76",
    "e81i",
    "e81ii",
    "e81iii",
    "e82i",
    "e82ii",
    "e82iii",
    "e82iv",
    "e83i",
    "e83ii",
    "e84i",
    "e84ii",
    "e85",
    "e86",
    "e88",
    "e90_condA",
    "e90_condB",
    "e92_award",
    "e92_deny",
    "e93_grp1",
    "new_e1",
    "new_e2",
    "else_inquire",
    "else_merge",
    "else_suppose",
    "else_uni_prod",
    "else_query",
    "else_which",
    "new_e5",
    "new_e6_leibniz",
    "new_e7_aristotle",
    "new_e8",
    "new_e9",
    "new_e10",
    "new_e11",
    "new_e12",
    "new_e13",
    "new_e14",
    "new_e15",
    "new_e16",
    "new_e17",
    "new_e18",
    "new_e19_first_atom_do_atom",
    "new_e20_nested_issue_in_pred",
    "new_e21_supp_is_something",
    "new_e22_restrict_dep_rel_is_not_other",
    "AnswerPotential",
    "UniProduct",
    "QueryTest",
    "QueryTest2",
]

import inspect
from abc import ABCMeta, abstractmethod
from pyclbr import Function
from typing import cast

from pyetr.atoms.terms.function import Function, NumFunc, RealNumber
from pyetr.atoms.terms.term import FunctionalTerm

from .func_library import div, log, power
from .inference import (
    basic_step,
    default_decision,
    default_inference_procedure,
    default_procedure_does_it_follow,
    default_procedure_what_is_prob,
)
from .view import View


def ps(s: str, custom_functions: list[NumFunc | Function] | None = None) -> View:
    return View.from_str(s, custom_functions)


name_mapping = {
    "v": "Views",
    "c": "Conclusion",
    "prob": "Probability",
    "cv": "Consequence Views",
    "pr": "Priority Views",
    "g1": "Another View",
    "g2": "Another View",
}


class BaseMeta(ABCMeta):
    @property
    def description(self):
        return inspect.getdoc(self)

    def __repr__(self):
        final_str = ""
        if self.description is not None:
            final_str += "\ndescription:\n"
            final_str += self.description

        for attr, mapped_name in name_mapping.items():
            if hasattr(self, attr):
                attribute = getattr(self, attr)
                long_name = " (" + mapped_name + ")"
                if isinstance(attribute, tuple):
                    full_name = ""
                    for i, v in enumerate(attribute):
                        full_name += f"v[{i}]: {v.to_str()}\n"
                else:
                    full_name = attr + long_name + ": " + attribute.to_str()
                final_str += "\n" + full_name

        if hasattr(self, "test"):
            final_str += "\n" + "test(verbose=False): Method used to test the example"
        final_str += "\n"
        return final_str


class BaseExample(metaclass=BaseMeta):
    """
    The base class for all examples. It contains a series of views (v)
    for operations and a conclusion (c).
    """

    v: tuple[View, ...]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "v"):
            raise TypeError("Example must have attribute v")
        if not hasattr(cls, "c"):
            raise TypeError("Example must have attribute c")
        v: tuple[View, ...] = getattr(cls, "v")
        assert isinstance(v, tuple)
        for i in v:
            assert isinstance(i, View)
        c: View | tuple[View, ...] | bool = getattr(cls, "c")
        assert (
            isinstance(c, bool)
            or isinstance(c, View)
            or (isinstance(c, tuple) and all(isinstance(x, View) for x in c))
        )

    @classmethod
    @abstractmethod
    def test(cls, verbose: bool = True):
        ...


class BaseTest:
    """
    The base class for all test types. Test types are mixins the define a test
    type, but not the associated views.
    """

    v: tuple[View, ...]
    c: View


class DefaultInference(BaseTest):
    @classmethod
    def test(cls, verbose: bool = True):
        result = default_inference_procedure(cls.v, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class BasicStep(BaseTest):
    @classmethod
    def test(cls, verbose: bool = True):
        result = basic_step(v=cls.v, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Product(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].product(cls.v[1])
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Sum(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].sum(cls.v[1])
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Answer(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].answer(cls.v[1])
        if not result == cls.c:
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Factor(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].factor(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Negation(BaseTest):
    v: tuple[View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].negation(verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Query(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].query(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Update(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].update(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class UniversalProduct(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].universal_product(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Which(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].which(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Suppose(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].suppose(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Inquire(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].inquire(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class Merge(BaseTest):
    v: tuple[View, View]

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].merge(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class DefaultDecision(BaseTest):
    v: tuple[View]
    cv: tuple[View, ...]
    pr: tuple[View, ...]
    c: View

    @classmethod
    def test(cls, verbose: bool = True):
        result = default_decision(dq=cls.v[0], cv=cls.cv, pr=cls.pr, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class WhatIsProb(BaseTest):
    v: tuple[View, ...]
    prob: View
    c: View

    @classmethod
    def test(cls, verbose: bool = True):
        result = default_procedure_what_is_prob(
            cls.v, prob_of=cls.prob, verbose=verbose
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e1(DefaultInference, BaseExample):
    """
    Example 1, p61:

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
    Example 2, p62:

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    """

    v: tuple[View, View] = (
        ps("{T()K(),Q()A()}"),
        ps("{K()}"),
    )
    c: View = ps("{T()}")


class e3(DefaultInference, BaseExample):
    """
    Example 3, p63:

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("{King()Ace(),Jack()Queen()}"),
        ps("{~Ace()}"),
    )
    c: View = ps("{Jack()Queen()}")


# e4 is not a test


class samples:
    gamma = "p1()q1()"
    delta = "r1()s1()"
    epsilon = "p2()q2()"
    theta = "s2()r2()"


class e5ii(Product, BaseExample):
    """
    Example 5, p72, part ii
    """

    v: tuple[View, View] = (
        ps("{" + f"{samples.delta},{samples.gamma}" + "}"),
        ps("{" + f"{samples.epsilon},{samples.theta}" + "}"),
    )
    c: View = ps(
        "{p2()r1()q2()s1(),s2()r1()r2()s1(),s2()p1()q1()r2(),p2()p1()q1()q2()}"
    )


class e5iii(Product, BaseExample):
    """
    Example 5, p72, part iii
    """

    v: tuple[View, View] = (
        ps("{" + f"{samples.gamma}, {samples.delta}" + "}"),
        View.get_falsum(),
    )
    c: View = View.get_falsum()


class e5iv(Product, BaseExample):
    """
    Example 5, p72, part iv
    """

    v: tuple[View, View] = (
        ps("{" + f"{samples.gamma}, {samples.delta}" + "}"),
        View.get_verum(),
    )
    c: View = ps("{" + f"{samples.gamma}, {samples.delta}" + "}")


class e5v(Product, BaseExample):
    """
    Example 5, p72, part v
    """

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


class e10(Answer, BaseExample):
    """
    Example 10, p76

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a king (reversed premises blocking illusory inference).
    """

    v: tuple[View, View] = (
        ps("{K()}"),
        ps("{T()K(),Q()A()}"),
    )
    c: View = ps("{K()}")


class e11(BasicStep, BaseExample):
    """
    Example 11, p77

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
    Example 12i, p78

    ItisnotthecasethatPorQorR
    """

    v: tuple[View] = (ps("{P(),Q(),R()}"),)
    c: View = ps("{~R()~Q()~P()}")


class e12ii(Negation, BaseExample):
    """
    Example 12ii, p78

    ItisnotthecasethatPandQandR
    """

    v: tuple[View] = (ps("{P()R()Q()}"),)
    c: View = ps("{~R(),~P(),~Q()}")


class e12iii(Negation, BaseExample):
    """
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    """

    v: tuple[View] = (ps("{P()Q(),R()}^{S()}"),)
    c: View = ps("{~P()S()~R(),~R()~Q()S()}")


class e13(DefaultInference, BaseExample):
    """
    Example 13, p80

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    """

    v: tuple[View, View] = (
        ps("{IsQueen()IsJack(),IsAce()IsKing()}"),
        ps("{~IsAce()}"),
    )
    c: View = ps("{IsQueen()IsJack()}")


class e14_1(Factor, BaseExample):
    """
    Example 14-1, p81

    Factor examples
    """

    v: tuple[View, View] = (
        ps("{P()R(),P()Q()}"),
        ps("{P()}"),
    )
    c: View = ps("{Q(),R()}")


class e14_2(Factor, BaseExample):
    """
    Example 14-2, p81

    Factor examples
    """

    v: tuple[View, View] = (
        ps("{P()R(),P()S()R(),P()S()Q()}"),
        ps("{P()}^{S()}"),
    )
    c: View = ps("{Q()S(),P()R(),S()R()}")


class e14_3(Factor, BaseExample):
    """
    Example 14-3, p81

    Factor examples
    """

    v: tuple[View, View] = (
        ps("{P()S(),Q()S(),P()R(),Q()R()}"),
        ps("{P(),Q()}"),
    )
    c: View = ps("{S(),R()}")


class e14_6(Factor, BaseExample):
    """
    Example 14-6, p81

    Factor examples
    """

    v: tuple[View, View] = (
        ps("{Q()S(),P()R()}"),
        ps("{T(),P(),Q()}"),
    )
    c: View = ps("{Q()S(),P()R()}")


class e14_7(Factor, BaseExample):
    """
    Example 14-7, p81

    Factor examples
    """

    v: tuple[View, View] = (
        ps("{Q()S(),P()R(),P()}"),
        ps("{P(),Q()}"),
    )
    c: View = ps("{0,S(),R()}")


class e15(DefaultInference, BaseExample):
    """
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    """

    v: tuple[View, View, View] = (
        ps("{Ace(),Jack()Queen()Ace(),Four()Ten()Eight()}"),
        ps("{Jack()Ten()Ace()Eight()}"),
        ps("{~Queen()}"),
    )
    c: View = ps("{Four()}")


class e16(DefaultInference, BaseExample):
    """
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    """

    v: tuple[View, View, View] = (
        ps("{King()Jack()Queen(),Ace(),Four()Ten()Eight()}"),
        ps("{~Four()}"),
        ps("{~Ace()}"),
    )
    c: View = ps("{King()Jack()Queen()}")


class e17(DefaultInference, BaseExample):
    """
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    """

    v: tuple[View, View] = (
        ps("{~King()Ace(),King()~Ace()}"),
        ps("{King()}"),
    )
    c: View = ps("{~Ace()}")


class e19(Suppose, BaseExample):
    """
    Example 19, p84

    Suppose test
    """

    v: tuple[View, View] = (
        ps("{0}"),
        ps("{~N()}"),
    )
    c: View = ps("{~N()}^{~N()}")


class e20(DefaultInference, BaseExample):
    """
    Example 20, p85

    P1 Either there is a king in the hand or a queen in the hand.
    P2 On the supposition that there is a king, Mary wins.
    P3 On the supposition that there is a queen, Bill wins.
    C Either Mary wins or Bill wins.
    """

    v: tuple[View, View, View] = (
        ps("{Queen(),King()}"),
        ps("{Win(mary())}^{King()}"),
        ps("{Win(bill())}^{Queen()}"),
    )
    c: View = ps("{Win(bill()),Win(mary())}")


class e21(BaseExample):
    """
    Example 21, p86

    Any view Δ^{0} = [Δ^{0}]ᶰ can be derived from the absurd view
    """

    v: tuple[View] = (ps("{" + f"{samples.delta}" + "}"),)
    c: View = ps("{" + f"{samples.delta}" + "}").negation()

    @classmethod
    def test(cls, verbose: bool = True):
        x = View.get_falsum().suppose(cls.v[0], verbose=verbose)
        result = x.depose(verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e22(BaseExample):
    """
    Example 22, p87

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
    def test(cls, verbose: bool = True):
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
    Example 23, p88, with inquire step

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
    def test(cls, verbose: bool = True):
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
    """
    Example 23, p88, without inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    """

    v: tuple[View, View] = (ps("{L()K(),P()S()}"), ps("{K()}"))
    c: tuple[View, View] = (
        ps("{L()K(),P()S()}"),
        ps("{L()K()}"),
    )

    @classmethod
    def test(cls, verbose: bool = True):
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
    Example 24, p89

    P1 There is an ace
    C There is an ace or a queen
    """

    v: tuple[View, View, View, View] = (
        ps("{a()}"),
        ps("{q()}"),
        ps("{~q()}"),
        ps("{a(),q()}"),
    )
    c: tuple[View, View] = (ps("{a()~q(),a()q()}"), ps("{a(),q()}"))

    @classmethod
    def test(cls, verbose: bool = True):
        result_1 = cls.v[0].inquire(other=cls.v[1], verbose=verbose)

        if not result_1.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {result_1}"
            )

        result_2 = result_1.factor(cls.v[2], verbose=verbose).query(
            cls.v[3], verbose=verbose
        )

        if not result_2.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result_2}")


class e25i(Query, BaseExample):
    """
    Example 25i, p89
    """

    v: tuple[View, View] = (ps("{p()r(),p()q()}"), ps("{p()}"))
    c: View = ps("{p()}")


class e25ii(Query, BaseExample):
    """
    Example 25ii, p89
    """

    v: tuple[View, View] = (ps("{p()r(),p()q()}"), ps("{q()}"))
    c: View = ps("{0,q()}")


class e25iii(Query, BaseExample):
    """
    Example 25iii, p89
    """

    v: tuple[View, View] = (
        ps("{t(),p()r(),p()q(),s()}"),
        ps("{p(),s()}"),
    )
    c: View = ps("{0,p(),s()}")


class e25iv(Query, BaseExample):
    """
    Example 25iv, p89
    """

    v: tuple[View, View] = (
        ps("{t(),p()r(),p()q(),s()}"),
        ps("{t(),p(),s()}"),
    )
    c: View = ps("{t(),p(),s()}")


class e25v(Query, BaseExample):
    """
    Example 25v, p89
    """

    v: tuple[View, View] = (
        ps("{s()p()q(),p()r()s()}"),
        ps("{p()}^{s()}"),
    )
    c: View = ps("{p()}")


class e25vi(Query, BaseExample):
    """
    Example 25vi, p89
    """

    v: tuple[View, View] = (
        ps("{s()p()q(),p()r()s()}"),
        ps("{p()}^{t()}"),
    )
    c: View = View.get_verum()


class e26(BaseExample):
    """
    Example 26, p90

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
    def test(cls, verbose: bool = True):
        mid_result = cls.v[0].suppose(other=cls.v[1])

        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        result = cls.c[0].query(other=cls.v[2])

        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected result: {cls.c[1]} but received {result}")


class e26_does_it_follow(e26):
    @classmethod
    def test(cls, verbose: bool = True):
        result = default_procedure_does_it_follow(
            (cls.v[0],), target=cls.v[2], verbose=verbose
        )

        if not result:
            raise RuntimeError(f"Did not follow, view {cls.v[0]}, target {cls.v[2]}")


class e28(BasicStep, BaseExample):
    """
    Example 28, p96

    P1 Is there a tiger?
    P2 Supposing there is a tiger, there is orange fur.
    P3 There is orange fur.
    C There is a tiger.
    """

    v: tuple[View, View, View] = (
        ps("{~Tiger(),Tiger()}"),
        ps("{Orange()Tiger()}^{Tiger()}"),
        ps("{Orange()}"),
    )
    c: View = ps("{Tiger()Orange()}")


class e32_1(DefaultInference, BaseExample):
    """
    Example 32-1, p107

    P1 If P then Q.
    P2 P
    C Q
    """

    v: tuple[View, View] = (
        ps("{P()Q()}^{P()}"),
        ps("{P()}"),
    )
    c: View = ps("{Q()}")


class e32_2(DefaultInference, BaseExample):
    """
    Example 32-2, p107

    P1 P
    P2 If P then Q.
    C Q
    """

    v: tuple[View, View] = (
        ps("{P()}"),
        ps("{P()Q()}^{P()}"),
    )
    c: View = ps("{Q()}")


class e33(DefaultInference, BaseExample):
    """
    Example 33, p108

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    """

    v: tuple[View, View] = (
        ps("{E()R()}^{R()}"),
        ps("{E()}"),
    )
    c: View = ps("{R()}")


class e40i(BaseExample):
    """
    Example 40, p119

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

    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .update(cls.v[1].depose(verbose=verbose), verbose=verbose)
            .update(cls.v[2], verbose=verbose)
            .factor(View.get_falsum(), verbose=verbose)
        )

        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected result: {cls.c} but received {result}")


class e40ii(BaseExample):
    """
    Example 40, p119-p120

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum

    The reader diverges from the default procedure,
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
    def test(cls, verbose: bool = True):
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
    Example 41, p121

    P1 P only if Q.
    P2 Not Q.
    C Not P.
    """

    v: tuple[View, View] = (
        ps("{~Q()~P()}^{~Q()}"),
        ps("{~Q()}"),
    )
    c: View = ps("{~P()}")


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
    Example 44-1, p123

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
    Example 45, p125

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    """

    v: tuple[View, View, View] = (ps("{0,M()}"), ps("{0,B()}"), ps("{0,B()M()}"))
    c: tuple[View, View] = (ps("{0,M(),B(),B()M()}"), ps("{0,B()M()}"))

    @classmethod
    def test(cls, verbose: bool = True):
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
    Example 46, p126

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
    def test(cls, verbose: bool = True):
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
    Example 46, part ii, p126

    If we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
    """

    v: tuple[View, View] = (
        ps("{V()S()M(),V()R()M(),T()}"),
        ps("{0,V()M()}"),
    )
    c: View = ps("{0,V()M()}")


class e47(DefaultInference, BaseExample):
    """
    Example 47, p129

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
    Example 48, p130

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
    Example 49, p130

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
    """
    Example 50, part1, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    """

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
    def test(cls, verbose: bool = True):
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
    """
    Example 50, part2, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    """

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
    def test(cls, verbose: bool = True):
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


class e50_part2_arbs(BaseExample):
    """
    Duplicate of e50, uses arb objects, some changes
    """

    v: tuple[View, View, View] = (
        ps("∃j ∃s ∃g {M(j)~M(g)L(j,s)L(s,g)}"),
        ps("∃s {M(s)}"),
        ps("∃b ∃a {M(a*)L(a,b)~M(b*)}"),
    )
    g1: View = ps("∃j ∃s ∃g {M(j)L(s,g)L(j,s)~M(g)M(s),M(j)L(s,g)L(j,s)~M(g)~M(s)}")
    g2: View = ps(
        "∃j ∃s ∃g {M(j*)L(s,g)L(j,s)~M(g*)M(s),M(j*)L(s,g)L(j,s)~M(g*)~M(s*)}"
    )

    c: View = ps("∃b ∃a {M(a*)L(a,b)~M(b*)}")

    @classmethod
    def test(cls, verbose: bool = True):
        mid_result = cls.v[0].inquire(cls.v[1], verbose=verbose)
        if not mid_result.is_equivalent_under_arb_sub(cls.g1):
            raise RuntimeError(
                f"Expected mid result: {cls.g1} but received {mid_result}"
            )

        # Should use reorient once this exists
        result = cls.g2.query(cls.v[2], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e51(BasicStep, BaseExample):
    """
    Example 51, p131

    P1: Every archaeon has a nucleus
    P2: Halobacterium is an archaeon

    C: Halobacterium is an archaeon and has a nucleus
    """

    v: tuple[View, View] = (
        ps("∀x {IsArchaeon(x*)HasNucleus(x)}^{IsArchaeon(x*)}"),
        ps("{IsArchaeon(Halobacterium()*)}"),
    )
    c: View = ps("{HasNucleus(Halobacterium())IsArchaeon(Halobacterium()*)}")


class e52(BasicStep, BaseExample):
    """
    Example 52, p132

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
    Example 53, p132 & p175

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
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .depose(verbose=verbose)
            .suppose(cls.v[1], verbose=verbose)
            .query(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e53_does_it_follow(e53):
    @classmethod
    def test(cls, verbose: bool = True):
        result = default_procedure_does_it_follow(
            (cls.v[0],), target=cls.v[2], verbose=verbose
        )

        if not result:
            raise RuntimeError(f"Did not follow, view {cls.v[0]}, target {cls.v[2]}")


class e54(BasicStep, BaseExample):
    """
    Example 54, p133

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
    Example 56, p134

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
    Example 57, p134

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
    Example 58 reversed, based on p135

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
    Example 61, p166
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    """

    v: tuple[View, View] = (ps("∀x ∃a {~D(x),M(a*)D(x)B(x,a)}"), ps("{M(j()*)}"))
    c: View = ps("∀x ∃a {M(j()*)M(a*)D(x)B(x,a),M(j()*)~D(x)}")


class e62(Which, BaseExample):
    """
    Example 62, p176
    """

    v = (
        ps("{L(n(),m())S(m()*),D(m())T(n())S(j()*),D(b())~S(n()*)}"),
        ps("∃a {S(a*)}"),
    )
    c = ps("{0,S(j()*),S(m()*)}")


class e63(Which, BaseExample):
    """
    Example 63, p176
    """

    v = (
        ps("{S(j()*)D(n()*),D(n()*)~D(j()*)T(j())}"),
        ps("∃a {D(a*)}"),
    )
    c = ps("{D(n()*)}")


class e63_modified(Which, BaseExample):
    """
    Example 63, p176
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

    v = (
        ps("∀x {90=* S(x*)T(x*), S(x)~T(x)}^{S(x)}"),
        ps("∀x {1=* ~S(x)T(x), ~S(x)~T(x)} ^ {~S(x*)}"),
        ps("{T(Smith()*)}"),
        ps("{S(Smith())}"),
    )
    c: View = ps("{90=* S(Smith()*), 0}")

    @classmethod
    def test(cls, verbose: bool = True):
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

    @classmethod
    def test(cls, verbose: bool = True):
        result = basic_step(v=cls.v[0:4], verbose=verbose).query(
            cls.v[4], verbose=verbose
        )

        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e65(BaseExample):
    """
    Example 65, p190, p224

    (Base-rate neglect with doctors and realistic disease) Imagine you conduct
    a screening using the Hemoccult test in a certain region. For symptom-free
    people over 50 years old who participate in screening using the Hemoccult test,
    the following information is available for this region.

    The probability that one of these people has colorectal cancer is 0.3%. If a
    person has colorectal cancer, the probability is 50 that he will have a positive
    Hemoccult test. If a person does not have a colorectal cancer, the probability is
    3% that he will still have a positive Hemoccult test in your screening. What is
    the probability that this person actually has colorectal cancer?
    """

    v = (
        ps("∀x {0.3=* P(x*)C(x), P(x)~C(x)}^{P(x)}"),
        ps("∀x {50=* P(x*)C(x)T(x),P(x)C(x)~T(x)}^{P(x)C(x)}"),
        ps("∀x {3=* P(x*)~C(x)T(x),P(x)~C(x)~T(x)}^{P(x)~C(x)}"),
        ps("∃a {P(a*)T(a)}"),
        ps("∃a {C(a)}"),
    )
    c: View = ps("∃a {15=* C(a), 0}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = basic_step(v=cls.v[0:4], verbose=verbose).query(
            cls.v[4], verbose=verbose
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e66i(BaseExample):
    """
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ?
    """

    v = (
        ps("{1=* D()T(), 1=* ~D()T(), 98=* ~D()}"),
        ps("{D()T()}"),
    )
    c: View = ps("{}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[1].stage, cls.v[0].weights
        )
        out = FunctionalTerm(f=RealNumber(num=1.0), t=())
        if not result == out:
            raise RuntimeError(f"Expected: {out} but received {result}")


class e66ii(e66i):
    v = (
        ps("{1=* D()T(), 1=* ~D()T(), 98=* ~D()}"),
        ps("{T()}"),
    )
    c: View = ps("{}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[1].stage, cls.v[0].weights
        )
        out = FunctionalTerm(f=RealNumber(num=2.0), t=())
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
        ps("{94=* IsCEO()HadPet(), ~IsCEO()}"),
        ps("{HadPet()}"),
        ps("{IsCEO()}"),
    )
    c: View = ps("{94=* IsCEO(), 0}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .suppose(cls.v[1], verbose=verbose)
            .depose(verbose=verbose)
            .query(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e69_part1(BaseExample):
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
    c: View = ps(
        "{0.000001=* ~Guilty(Suspect())Match(Suspect()), Guilty(Suspect())Match(Suspect())}"
    )

    # TODO: Switch to new basic step?
    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .update(cls.v[1].depose(verbose=verbose), verbose=verbose)
            .factor(View.get_falsum(), verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e69_part2(BaseExample):
    v = (
        ps(
            "{0.000001=* ~Guilty(Suspect())Match(Suspect()), Guilty(Suspect())Match(Suspect())}"
        ),
        ps("{999999.999999=* 0}^{Guilty(Suspect())Match(Suspect())}"),
        ps("{Guilty(Suspect())}"),
    )
    c: tuple[View, View] = (
        ps(
            "{0.000001=* ~Guilty(Suspect())Match(Suspect()), 999999.999999=* Guilty(Suspect())Match(Suspect())}"
        ),
        ps("{999999.999999=* Guilty(Suspect()), 0}"),
    )

    @classmethod
    def test(cls, verbose: bool = True):
        mid_result = cls.v[0].inquire(cls.v[1], verbose=verbose)
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )
        result = mid_result.query(cls.v[2], verbose=verbose)
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
    c: View = ps("{Disease()Symptom()}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0].update(cls.v[1], verbose=verbose).update(cls.v[2], verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e71(BaseExample):
    """
    Examples 71 & 78, p209, p212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    """

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
    def test(cls, verbose: bool = True):
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
    def test(cls, verbose: bool = True):
        mid_result = (
            cls.v[0]
            .inquire(cls.v[1], verbose=verbose)
            .inquire(cls.v[2], verbose=verbose)
            .inquire(cls.v[3], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(f"Expected: {cls.c[0]} but received {mid_result}")
        # NOTE: This is an additional inquire to what was in the book
        result = mid_result.inquire(cls.v[4], verbose=verbose).query(
            cls.v[4], verbose=verbose
        )
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e74(BaseExample):
    """
    Example 74, p197, p231

    (includes two background commitments)
    """

    v = (
        ps("{D(j())H(j()),H(j()),P(j())}"),
        ps("{E(j()*)}"),
        ps("Ax {0.85=* E(x)D(x), 0.15=* E(x)~D(x)} ^ {E(x*)}"),
        ps("Ax {0.1=* E(x)H(x), 0.9=* E(x)~H(x)} ^ {E(x*)}"),
    )
    c: tuple[View, View] = (
        ps(
            "{0.85**0.1=* E(j()*)D(j())H(j()), 0.85**0.9=* E(j())D(j())~H(j()), 0.15**0.1=* E(j())~D(j())H(j()), 0.15**0.9=* E(j())~D(j())~H(j())}"
        ),
        ps("{D(j())H(j())}"),
    )

    @classmethod
    def test(cls, verbose: bool = True):
        mid_result = (
            cls.v[1].update(cls.v[2], verbose=verbose).update(cls.v[3], verbose=verbose)
        )
        if not mid_result.is_equivalent_under_arb_sub(cls.c[0]):
            raise RuntimeError(
                f"Expected mid result: {cls.c[0]} but received {mid_result}"
            )

        # Should use reorient once this exists
        result = cls.v[0].answer(mid_result, verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c[1]):
            raise RuntimeError(f"Expected: {cls.c[1]} but received {result}")


class e76(BaseExample):
    """
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    """

    v = (
        ps("{Fired(i()*)Gun(i())Guitar(j())Outoftune(j()), Attic(a())}"),
        ps("Ax {Gun(x)Trigger(x)Fired(x),0}^{Gun(x)Fired(x*)}"),
        ps("{Trigger(i())}"),
    )
    c: View = ps("{Fired(i()*)Gun(i())Guitar(j())Outoftune(j())Trigger(i())}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .update(cls.v[1], verbose=verbose)
            .update(cls.v[2].update(cls.v[1], verbose=verbose), verbose=verbose)
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class e81_base(WhatIsProb):
    """
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    """

    v = (ps("{Box(Yellow())~Box(Brown()), Box(Brown())~Box(Yellow())}"),)
    prob: View
    c: View


class e81i(e81_base, BaseExample):
    """
    In the box there is a yellow card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Yellow())}")
    c = ps("{50=* Box(Yellow()), 0}")


class e81ii(e81_base, BaseExample):
    """
    In the box there is a yellow card and a brown card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Brown())Box(Yellow())}")
    c = ps("{0}")


class e81iii(e81_base, BaseExample):
    """
    In the box there is neither a yellow card nor a brown card
    """

    __doc__ = cast(str, e81_base.__doc__) + cast(str, __doc__)
    prob = ps("{~Box(Brown())~Box(Yellow())}")
    c = ps("{0}")


class e82_base(WhatIsProb):
    """
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    """

    v = (ps("{Box(Brown())Box(Yellow())}^{Box(Yellow())}"),)


class e82i(e82_base, BaseExample):
    """
    In the box there is a yellow card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Yellow())}")
    c = ps("{50=* Box(Yellow()), 0}")


class e82ii(e82_base, BaseExample):
    """
    In the box there is a yellow card and a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Brown())Box(Yellow())}")
    c = ps("{50=* Box(Brown())Box(Yellow()), 0}")


class e82iii(e82_base, BaseExample):
    """
    In the box there is a yellow card and there is not a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Yellow())~Box(Brown())}")
    c = ps("{0}")


class e82iv(e82_base, BaseExample):
    """
    In the box there is neither a yellow card nor a brown card.
    """

    __doc__ = cast(str, e82_base.__doc__) + cast(str, __doc__)
    prob = ps("{~Box(Brown())~Box(Yellow())}")
    c = ps("{0}")


class e83_base(WhatIsProb):
    """
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    """

    v = (
        ps(
            "{divide(100,3)=* Box(Red()), divide(100,3)=* Box(Green())Box(Blue()), divide(100,3)=* ~Box(Red())~Box(Green())~Box(Blue())}",
            custom_functions=[Function(name="divide", arity=2, func_caller=div)],
        ),
    )


class e83i(e83_base, BaseExample):
    """
    There is a red marble and blue in marble in the box.
    """

    __doc__ = cast(str, e83_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Red())Box(Blue())}")
    c = ps("{0}")


class e83ii(e83_base, BaseExample):
    """
    There is a green marble and there is a blue marble.
    """

    __doc__ = cast(str, e83_base.__doc__) + cast(str, __doc__)
    prob = ps("{Box(Green())Box(Blue())}")
    c = ps(
        "{divide(100,3)=* Box(Green())Box(Blue()), 0}",
        custom_functions=[Function(name="divide", arity=2, func_caller=div)],
    )


class e84i(WhatIsProb, BaseExample):
    """
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    """

    v = (
        ps(
            "{Box(Grey())Box(White())~Box(Mauve()),Box(Grey())Box(Mauve())~Box(White())}"
        ),
    )
    prob = ps("{Box(Grey())Box(Mauve())}")
    c = ps("{50=* Box(Grey())Box(Mauve()), 0}")


class e84ii(WhatIsProb, BaseExample):
    """
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    """

    # TODO: Look at default reasoning procedure for what is prob questions
    v = (
        ps(
            "{Box(Grey())~Box(White())~Box(Mauve()),Box(White())~Box(Grey())~Box(Mauve()),Box(Mauve())~Box(White())~Box(Grey())}"
        ),
    )
    prob = ps("{Box(Grey())Box(Mauve())}")
    c = ps("{0}")


class e85(WhatIsProb, BaseExample):
    """
    Example 85, p216

    Easy partial probability inference

    There is a box in which there is one and only one of these marbles: a
    green marble, a blue marble, or a red marble. The probability that a green
    marble is in the box is 0.6, and the probability that a blue marble is in
    the box is 0.2.

    What is the probability that a red marble is in the box?
    """

    v = (
        ps("{Box(Green()), Box(Blue()), Box(Red())}"),
        ps("{60=* Box(Green())}^{Box(Green())}"),
        ps("{20=* Box(Blue())}^{Box(Blue())}"),
    )
    prob = ps("{Box(Red())}")
    c = ps("{20=* Box(Red()), 0}")


class e86(WhatIsProb, BaseExample):
    """
    Example 86, p217

    You have a hand of several cards with only limited information about it.

    There is an ace and a queen or a king and a jack or a ten.
    The probability that there is an ace and a queen is 0.6
    The probability that there is a king and a jack is 0.2

    What is the probability that there is a ten?
    """

    v = (
        ps("{A()Q(), K()J(), X()}"),
        ps("{60=* A()Q()}^{A()Q()}"),
        ps("{20=* K()J()}^{K()J()}"),
    )
    prob = ps("{X()}")
    c = ps("{20=* X(), 0}")


class e88(BaseExample):
    """
    Example 88, p233

    P1: There is a 90% chance Superman can fly
    P2: Clark is superman

    C: There is a 90% chance Clark can fly
    """

    v: tuple[View, View, View, View] = (
        ps("{90=* CanFly(Superman())}"),
        ps("{==(Clark(), Superman())}"),
        ps("{==(Clark(), Superman()*)}"),
        ps("{==(Clark(), Clark())}"),
    )
    c: View = ps("{90=* CanFly(Clark())}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = (
            cls.v[0]
            .update(cls.v[1], verbose=verbose)
            .factor(cls.v[2], verbose=verbose)
            .factor(cls.v[3], verbose=verbose)
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
    """

    v = (ps("{do(Buy(Video()*)),~do(Buy(Video()*))}"),)
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
    messy divorce. The facts of the case are complicated by ambiguous economic, social, and
    emotional considerations, and you decide to base your decision entirely on the following
    few observations.

    ParentA: average income, average health, average working hours, reasonable rapport with the
    child, relatively social life.

    ParentB: above-average income, very close relationship with the child, extremely active
    social life, lots of work-related travel, minor health problems.
    """

    cv = (
        ps("Ax {Custody(x*)} ^ {do(Award(x*))}"),
        ps("Ax {~Custody(x*)} ^ {do(Deny(x*))}"),
        ps(
            "{MedRapp(ParentA())MedTime(ParentA())HighRapp(ParentB())LowTime(ParentB())}"
        ),
    )
    pr = (
        ps("Ax {1=+ 0} ^ {Custody(x*)MedRapp(x)}"),
        ps("Ax {3=+ 0} ^ {Custody(x*)HighRapp(x)}"),
        ps("Ax {1=+ 0} ^ {Custody(x*)MedTime(x)}"),
        ps("Ax {1=+ 0} ^ {~Custody(x*)MedTime(x)}"),
        ps("Ax {2=+ 0} ^ {~Custody(x*)LowTime(x)}"),
    )


class e92_award(DefaultDecision, e92_base, BaseExample):
    """
    To which parent would you award sole custody of the child?
    """

    __doc__ = cast(str, e92_base.__doc__) + cast(str, __doc__)
    v = (ps("{do(Award(ParentA()*)), do(Award(ParentB()*))}"),)

    c = ps("{do(Award(ParentB()*))}")


class e92_deny(DefaultDecision, e92_base, BaseExample):
    """
    To which parent would you deny sole custody of the child?
    """

    __doc__ = cast(str, e92_base.__doc__) + cast(str, __doc__)
    v = (ps("{do(Deny(ParentA()*)), do(Deny(ParentB()*))}"),)
    c = ps("{do(Deny(ParentB()*))}")


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
            "Ax {power(++(1, log(++(1, x))), -1)=+ 0} ^ {D(x*)}",
            custom_functions=[power, log],
        ),
        ps("Ax {++(1, log(++(1, x)))=+ 0} ^ {S(x*)}", custom_functions=[log]),
    )
    cv = (
        ps("{D(400*)} ^ {do(A())}"),
        ps("{0.33=* D(0.0*), ~D(0.0)} ^ {do(B())}"),
        ps("{0.67=* D(600*), ~D(600)} ^ {do(B())}"),
    )
    c = ps("{do(B())}")

    @classmethod
    def test(cls, verbose: bool = True):
        absurd_view = ps("{D(0)D(600)}")
        absurd_state = next(iter(absurd_view.stage))
        result = default_decision(
            dq=cls.v[0],
            cv=cls.cv,
            pr=cls.pr,
            verbose=verbose,
            absurd_states=[absurd_state],
        )
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class new_e1(BaseExample):
    v = (ps("Ax Ea Ay {P(x,a)Q(a,y)}"), ps("Eb Az {P(b,z)}"))
    c = ps("Eb Ax Az Ea Ay {P(x,a)P(b,z)Q(a,y)}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].update(cls.v[1], verbose=verbose)
        if not result.is_equivalent_under_arb_sub(cls.c):
            raise RuntimeError(f"Expected: {cls.c} but received {result}")


class new_e2(BaseExample):
    v = (ps("Ea Ax {P(a)Q(x*)}"), ps("Ax Eb {Q(x*)R(b)}^{Q(x*)}"))
    c = ps("Ea Ax Eb {P(a)Q(x*)R(b)}")

    @classmethod
    def test(cls, verbose: bool = True):
        result = cls.v[0].dependency_relation.fusion(cls.v[1].dependency_relation)
        if result != cls.c.dependency_relation:
            raise RuntimeError(
                f"Expected: {cls.c.dependency_relation.detailed} but received {result.detailed}"
            )


class new_e3_base:
    v = (ps("Ea Ax {P(a)Q(x*)}"), ps("Ax Eb {Q(x*)R(b)}^{Q(x*)}"))
    c = ps("Ea Ax {P(a)Q(x*)}")


class else_inquire(new_e3_base, Inquire, BaseExample):
    pass


class else_merge(new_e3_base, Merge, BaseExample):
    pass


class else_suppose(new_e3_base, Suppose, BaseExample):
    pass


class else_uni_prod(new_e3_base, UniversalProduct, BaseExample):
    pass


class new_e4_base:
    v = (ps("Ea Ax {P(a)Q(x*)}"), ps("Ay Ea {Q(y*)R(a)}^{Q(y*)}"))
    c = ps("Ea Ax {P(a)Q(x*)}")


class else_query(new_e4_base, Query, BaseExample):
    pass


class else_which(new_e4_base, Which, BaseExample):
    pass


class new_e5(Query, BaseExample):
    v = (
        ps("Ax Ay Ea Eb Az Ec {Q(x*)P(y)P(a*)P(b)P(z)P(c)}"),
        ps("Ed Ee Ef {P(d*)Q(e*)Q(f*)}"),
    )
    c = ps("∃e ∃d ∃f {P(d*)Q(f*)Q(e*)}")


class new_e6_leibniz(Factor, BaseExample):
    v = (ps("Ea Eb {P(f(a), a)~P(f(b), a)==(a,b)}"), ps("{}"))
    c = ps("{}")


class new_e7_aristotle(Factor, BaseExample):
    v = (ps("Ea {~==(a,a)}"), ps("{}"))
    c = ps("{}")


class new_e8(Update, BaseExample):
    v = (ps("{t()=+ A()}"), ps("{u()=* A()}"))
    c = ps("{u()=* t()=+ A()}")


class new_e9(DefaultInference, BaseExample):
    v = (ps("Ax {P(x*)}"), ps("{P(j()*)}"))
    c = ps("{0}")


class new_e10(Query, BaseExample):
    v = (ps("Ax {f(x)=* A(x*)}"), ps("Ee {f(e)=* A(e*)}"))
    c = ps("Ee {f(e)=* A(e*)}")


class new_e11(Query, BaseExample):
    v = (ps("{f(12)=* A(12*)}"), ps("Ee {f(e)=* A(e*)}"))
    c = ps("Ee {f(e)=* A(e*)}")


class new_e12(Inquire, BaseExample):
    v = (ps("{A()}"), ps("{}"))
    c = ps("{A()}")


class new_e13(WhatIsProb, BaseExample):
    v = (ps("{f(12)=* A(12*), B()}"),)
    prob = ps("Ee {A(e*)}")
    c = ps("{}")


class new_e14(Update, BaseExample):
    v = (ps("Ax Ey {A(f(x*))B(g(x*,y))}"), ps("{A(f(j()*))}"))
    c = ps("Ey {A(f(j()*))B(g(j()*, y))}")


class new_e15(Factor, BaseExample):
    v = (
        ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}"),
        ps("{==(Clark()*,Superman())}"),
    )
    c = ps("Ek {Defeats(k,Clark())==(Clark(),Clark())}")


class new_e16(Factor, BaseExample):
    v = (ps("Ek Ex {==(Clark(),x)Defeats(k,x)}"), ps("Ex {==(Clark()*,x)}"))
    c = ps("Ek {Defeats(k,Clark())==(Clark(),Clark())}")


class new_e17(Factor, BaseExample):
    v = (ps("Ek Ex {==(Clark(),x)do(Defeats(k,x))}"), ps("Ex {==(Clark()*,x)}"))
    c = ps("Ek {do(Defeats(k,Clark()))==(Clark(),Clark())}")


class new_e18(Update, BaseExample):
    v = (ps("{m()=* A()}"), ps("{n()=* B()}"))
    c = ps("{m() ** n()=* A() B()}")


class new_e19_first_atom_do_atom(Factor, BaseExample):
    v = (ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}"), ps("{do(A())}"))
    c = ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}")


class new_e20_nested_issue_in_pred(Factor, BaseExample):
    v = (
        ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}"),
        ps("{==(Clark(),f(Superman()*))}"),
    )
    c = ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}")


class new_e21_supp_is_something(Factor, BaseExample):
    v = (
        ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}"),
        ps("{==(Clark()*,Superman())}^{}"),
    )
    c = ps("Ek {==(Clark(),Superman())Defeats(k, Superman())}")


class new_e22_restrict_dep_rel_is_not_other(Factor, BaseExample):
    v = (ps("Ek Ex {==(Clark(),x)do(Defeats(k,x))}"), ps("Ey {==(Clark()*,y)}"))
    c = ps("Ek Ex {==(Clark(),x)do(Defeats(k,x))}")


class AnswerPotential(BaseExample):
    v = (
        ps("{1.0=* 2.0=+ A()B() , 0.4=* B()C(), C()A()}"),
        ps("{A()}"),
        ps("{B()}"),
        ps("{C()}"),
        ps("{C()D()}"),
        ps("{C()~B()}"),
    )
    c = ps("{}")

    @classmethod
    def test(cls, verbose: bool = True):
        out = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[1].stage, cls.v[0].weights
        )
        assert isinstance(out.f, RealNumber)
        assert out.f.num == 2.0, f"{out.f.num} not equal to {2.0}"
        out = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[2].stage, cls.v[0].weights
        )
        assert isinstance(out.f, RealNumber)
        assert out.f.num == 2.4, f"{out.f.num} not equal to {2.4}"
        out = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[3].stage, cls.v[0].weights
        )
        assert isinstance(out.f, RealNumber)
        assert out.f.num == 0.4, f"{out.f.num} not equal to {0.4}"

        out = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[4].stage, cls.v[0].weights
        )
        assert isinstance(out.f, RealNumber)
        assert out.f.num == 0.0, f"{out.f.num} not equal to {0.0}"

        out = cls.v[0].stage.equilibrium_answer_potential(
            cls.v[5].stage, cls.v[0].weights
        )
        assert isinstance(out.f, RealNumber)
        assert out.f.num == 0.0, f"{out.f.num} not equal to {0.0}"


class UniProduct(UniversalProduct, BaseExample):
    v = (ps("∀x ∃a {P(x)E(x,a),~P(x*)}"), ps("{P(j()*)}"))
    c: View = ps("∃a {~P(j()*),P(j())E(j(),a)}")


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
