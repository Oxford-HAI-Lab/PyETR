# Case Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L394)


```
description:
    Example 1, p61:

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else
    Mark is standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire.
    C Jane is looking at the TV.
    
v (Views): (
   {KneelingByTheFire(Jane())LookingAtTV(Jane()),StandingAtTheWindow(Mark())PeeringIntoTheGarden(Mark())},
   {KneelingByTheFire(Jane())}
)
c (Conclusion): {LookingAtTV(Jane())}
test(verbose=False): Method used to test the example
```

## e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L413)


```
description:
    Example 2, p62:

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    
v (Views): (
   {K()T(),Q()A()},
   {K()}
)
c (Conclusion): {T()}
test(verbose=False): Method used to test the example
```

## e3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L429)


```
description:
    Example 3, p63:

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v (Views): (
   {Ace()King(),Jack()Queen()},
   {~Ace()}
)
c (Conclusion): {Jack()Queen()}
test(verbose=False): Method used to test the example
```

## e5ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L456)


```
description:
    Example 5, p72, part ii
    
v (Views): (
   {r1()s1(),q1()p1()},
   {q2()p2(),s2()r2()}
)
c (Conclusion): {s1()r1()q2()p2(),s2()r1()s1()r2(),q1()s2()p1()r2(),q1()p1()q2()p2()}
test(verbose=False): Method used to test the example
```

## e5iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L470)


```
description:
    Example 5, p72, part iii
    
v (Views): (
   {q1()p1(),r1()s1()},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e5iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L482)


```
description:
    Example 5, p72, part iv
    
v (Views): (
   {q1()p1(),r1()s1()},
   {0}
)
c (Conclusion): {q1()p1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e5v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L494)


```
description:
    Example 5, p72, part v
    
v (Views): (
   {0},
   {q1()p1(),r1()s1()}
)
c (Conclusion): {q1()p1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L506)


```
description:
    Example 6, p72

    There is an Ace and a King = (There is an Ace) x (There is a king)
    
v (Views): (
   {a()},
   {k()}
)
c (Conclusion): {a()k()}
test(verbose=False): Method used to test the example
```

## e7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L517)


```
description:
    Example 7, p73

    There is an Ace or there is a king = (There is an Ace) + (There is a king)
    
v (Views): (
   {a()},
   {k()}
)
c (Conclusion): {a(),k()}
test(verbose=False): Method used to test the example
```

## e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L528)


```
description:
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    
v (Views): (
   {t()k(),a()q()},
   {k()}
)
c (Conclusion): {t()}
test(verbose=False): Method used to test the example
```

## e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L542)


```
description:
    Example 10, p76

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a ten.
    
v (Views): (
   {K(x())},
   {K(z())T(w()),A(x())Q(y())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L558)


```
description:
    Example 11, p77

    P1 Either John smokes or Mary smokes.
    P2 Supposing John smokes, John drinks.
    P3 Supposing Mary smokes, Mary eats.
    C Either John smokes and drinks or Mary smokes and drinks.
    
v (Views): (
   {Smokes(j()),Smokes(m())},
   {Drinks(j())}^{Smokes(j())},
   {Eats(m())}^{Smokes(m())}
)
c (Conclusion): {Drinks(j())Smokes(j()),Smokes(m())Eats(m())}
test(verbose=False): Method used to test the example
```

## e12i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L576)


```
description:
    Example 12i, p78

    ItisnotthecasethatPorQorR
    
v (Views): (
   {P(),Q(),R()}
)
c (Conclusion): {~P()~Q()~R()}
test(verbose=False): Method used to test the example
```

## e12ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L587)


```
description:
    Example 12ii, p78

    ItisnotthecasethatPandQandR
    
v (Views): (
   {R()Q()P()}
)
c (Conclusion): {~R(),~P(),~Q()}
test(verbose=False): Method used to test the example
```

## e12iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L598)


```
description:
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    
v (Views): (
   {Q()P(),R()}^{S()}
)
c (Conclusion): {~P()S()~R(),S()~Q()~R()}
test(verbose=False): Method used to test the example
```

## e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L609)


```
description:
    Example 13, p80

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v (Views): (
   {IsQueen()IsJack(),IsAce()IsKing()},
   {~IsAce()}
)
c (Conclusion): {IsQueen()IsJack()}
test(verbose=False): Method used to test the example
```

## e14_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L625)


```
description:
    Example 14-1, p81

    Factor examples
    
v (Views): (
   {R()P(),Q()P()},
   {P()}
)
c (Conclusion): {Q(),R()}
test(verbose=False): Method used to test the example
```

## e14_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L639)


```
description:
    Example 14-2, p81

    Factor examples
    
v (Views): (
   {R()P(),R()S()P(),Q()S()P()},
   {P()}^{S()}
)
c (Conclusion): {S()Q(),R()P(),R()S()}
test(verbose=False): Method used to test the example
```

## e14_3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L653)


```
description:
    Example 14-3, p81

    Factor examples
    
v (Views): (
   {S()P(),S()Q(),R()P(),R()Q()},
   {P(),Q()}
)
c (Conclusion): {S(),R()}
test(verbose=False): Method used to test the example
```

## e14_6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L667)


```
description:
    Example 14-6, p81

    Factor examples
    
v (Views): (
   {S()Q(),R()P()},
   {T(),P(),Q()}
)
c (Conclusion): {S()Q(),R()P()}
test(verbose=False): Method used to test the example
```

## e14_7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L681)


```
description:
    Example 14-7, p81

    Factor examples
    
v (Views): (
   {S()Q(),R()P(),P()},
   {P(),Q()}
)
c (Conclusion): {0,S(),R()}
test(verbose=False): Method used to test the example
```

## e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L695)


```
description:
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    
v (Views): (
   {Ace(),Jack()Ace()Queen(),Ten()Eight()Four()},
   {Jack()Ace()Eight()Ten()},
   {~Queen()}
)
c (Conclusion): {Four()}
test(verbose=False): Method used to test the example
```

## e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L713)


```
description:
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    
v (Views): (
   {Jack()Queen()King(),Ace(),Ten()Eight()Four()},
   {~Four()},
   {~Ace()}
)
c (Conclusion): {Jack()Queen()King()}
test(verbose=False): Method used to test the example
```

## e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L730)


```
description:
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    
v (Views): (
   {Ace()~King(),~Ace()King()},
   {King()}
)
c (Conclusion): {~Ace()}
test(verbose=False): Method used to test the example
```

## e19
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L746)


```
description:
    Example 19, p84

    Suppose test
    
v (Views): (
   {0},
   {~N()}
)
c (Conclusion): {~N()}^{~N()}
test(verbose=False): Method used to test the example
```

## e20
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L760)


```
description:
    Example 20, p85

    P1 Either there is a king in the hand or a queen in the hand.
    P2 On the supposition that there is a king, Mary wins.
    P3 On the supposition that there is a queen, Bill wins.
    C Either Mary wins or Bill wins.
    
v (Views): (
   {Queen(),King()},
   {Win(mary())}^{King()},
   {Win(bill())}^{Queen()}
)
c (Conclusion): {Win(bill()),Win(mary())}
test(verbose=False): Method used to test the example
```

## e21
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L778)


```
description:
    Example 21, p86

    Any view Δ^{0} = [Δ^{0}]ᶰ can be derived from the absurd view
    
v (Views): (
   {r1()s1()}
)
c (Conclusion): {~s1(),~r1()}
test(verbose=False): Method used to test the example
```

## e22
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L796)


```
description:
    Example 22, p87

    It is not the case that A and B and C
    
v (Views): (
   {a()b()c()},
   {a()},
   {b()},
   {c()}
)
c (Conclusion): (
   {~c(),~b(),~a()},
   {a()~c()~b(),~a()~c()~b(),~a()~c()b(),a()~c()b(),a()~b()c(),~a()b()c(),~a()~b()c()}
)
test(verbose=False): Method used to test the example
```

## e23_with_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L835)


```
description:
    Example 23, p88, with inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v (Views): (
   {K()L(),S()P()},
   {K()}
)
c (Conclusion): (
   {S()~K()P(),K()L(),K()S()P()},
   {K()L(),K()S()P()}
)
test(verbose=False): Method used to test the example
```

## e23_without_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L871)


```
description:
    Example 23, p88, without inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v (Views): (
   {K()L(),S()P()},
   {K()}
)
c (Conclusion): (
   {K()L(),S()P()},
   {K()L()}
)
test(verbose=False): Method used to test the example
```

## e24
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L903)


```
description:
    Example 24, p89

    P1 There is an ace
    C There is an ace or a queen
    
v (Views): (
   {a()},
   {q()},
   {~q()},
   {a(),q()}
)
c (Conclusion): (
   {a()~q(),a()q()},
   {a(),q()}
)
test(verbose=False): Method used to test the example
```

## e25i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L936)


```
description:
    Example 25i, p89
    
v (Views): (
   {r()p(),q()p()},
   {p()}
)
c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L945)


```
description:
    Example 25ii, p89
    
v (Views): (
   {r()p(),q()p()},
   {q()}
)
c (Conclusion): {0,q()}
test(verbose=False): Method used to test the example
```

## e25iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L954)


```
description:
    Example 25iii, p89
    
v (Views): (
   {t(),r()p(),q()p(),s()},
   {p(),s()}
)
c (Conclusion): {0,p(),s()}
test(verbose=False): Method used to test the example
```

## e25iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L966)


```
description:
    Example 25iv, p89
    
v (Views): (
   {t(),r()p(),q()p(),s()},
   {t(),p(),s()}
)
c (Conclusion): {t(),p(),s()}
test(verbose=False): Method used to test the example
```

## e25v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L978)


```
description:
    Example 25v, p89
    
v (Views): (
   {q()p()s(),r()p()s()},
   {p()}^{s()}
)
c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25vi
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L990)


```
description:
    Example 25vi, p89
    
v (Views): (
   {q()p()s(),r()p()s()},
   {p()}^{t()}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e26
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1002)


```
description:
    Example 26, p90

    P1 Either John plays and wins, or Mary plays, or Bill plays
    C Supposing John plays, John wins
    
v (Views): (
   {Play(J())Win(J()),Play(B()),Play(M())},
   {Play(J())},
   {Win(J())}^{Play(J())}
)
c (Conclusion): (
   {Play(J())Win(J())}^{Play(J())},
   {Win(J())}^{Play(J())}
)
test(verbose=False): Method used to test the example
```

## e26_does_it_follow
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1035)


```
v (Views): (
   {Play(J())Win(J()),Play(B()),Play(M())},
   {Play(J())},
   {Win(J())}^{Play(J())}
)
c (Conclusion): (
   {Play(J())Win(J())}^{Play(J())},
   {Win(J())}^{Play(J())}
)
test(verbose=False): Method used to test the example
```

## e28
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1046)


```
description:
    Example 28, p96

    P1 Is there a tiger?
    P2 Supposing there is a tiger, there is orange fur.
    P3 There is orange fur.
    C There is a tiger.
    
v (Views): (
   {~Tiger(),Tiger()},
   {Tiger()Orange()}^{Tiger()},
   {Orange()}
)
c (Conclusion): {Tiger()Orange()}
test(verbose=False): Method used to test the example
```

## e32_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1064)


```
description:
    Example 32-1, p107

    P1 If P then Q.
    P2 P
    C Q
    
v (Views): (
   {Q()P()}^{P()},
   {P()}
)
c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e32_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1080)


```
description:
    Example 32-2, p107

    P1 P
    P2 If P then Q.
    C Q
    
v (Views): (
   {P()},
   {Q()P()}^{P()}
)
c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e33
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1096)


```
description:
    Example 33, p108

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    
v (Views): (
   {R()E()}^{R()},
   {E()}
)
c (Conclusion): {R()}
test(verbose=False): Method used to test the example
```

## e40i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1112)


```
description:
    Example 40, p119

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    
v (Views): (
   {SquareB()~CircleB()~TriangleB(),~TriangleB()~SquareB()CircleB(),~CircleB()TriangleB()~SquareB()},
   {CircleT()SquareB()}^{CircleT()},
   {TriangleB()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e40ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1145)


```
description:
    Example 40, p119-p120

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum

    The reader diverges from the default procedure,
    and deposes the conditional premise, and switches the premise
    order.
    
v (Views): (
   {SquareB()~CircleB()~TriangleB(),~TriangleB()~SquareB()CircleB(),~CircleB()TriangleB()~SquareB()},
   {TriangleB()},
   {CircleT()SquareB()}^{CircleT()}
)
c (Conclusion): {~CircleB()TriangleB()~CircleT()~SquareB()}
test(verbose=False): Method used to test the example
```

## e41
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1182)


```
description:
    Example 41, p121

    P1 P only if Q.
    P2 Not Q.
    C Not P.
    
v (Views): (
   {~P()~Q()}^{~Q()},
   {~Q()}
)
c (Conclusion): {~P()}
test(verbose=False): Method used to test the example
```

## e42
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1198)


```
description:
    Example 42, p122

    P1 There is a circle at the top of the card only if there is a square
    at the bottom.
    P2 There is not a square at the bottom
    C There is not a circle at the top
    
v (Views): (
   {~CircleT()~SquareB()}^{~SquareB()},
   {~SquareB()}
)
c (Conclusion): {~CircleT()}
test(verbose=False): Method used to test the example
```

## e44_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1218)


```
description:
    Example 44-1, p123

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    
v (Views): (
   {Saleable(c())Elegant(c()),~Elegant(c())~Saleable(c())},
   {~Elegant(c())~Stable(c()),Elegant(c())Stable(c())},
   {Saleable(c())Elegant(c()),Stable(c()),Saleable(c())}
)
c (Conclusion): {Saleable(c())Stable(c())Elegant(c())}
test(verbose=False): Method used to test the example
```

## e45
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1236)


```
description:
    Example 45, p125

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    
v (Views): (
   {0,M()},
   {0,B()},
   {0,B()M()}
)
c (Conclusion): (
   {0,M(),B(),B()M()},
   {0,B()M()}
)
test(verbose=False): Method used to test the example
```

## e46i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1263)


```
description:
    Example 46, p126

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    
v (Views): (
   {P()V()}^{P()},
   {~P()M(),~M()P()},
   {0,M()V()}
)
c (Conclusion): (
   {~P()M(),P()~M()V()},
   {0}
)
test(verbose=False): Method used to test the example
```

## e46ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1300)


```
description:
    Example 46, part ii, p126

    If we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
    
v (Views): (
   {M()S()V(),M()R()V(),T()},
   {0,M()V()}
)
c (Conclusion): {0,M()V()}
test(verbose=False): Method used to test the example
```

## e47
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1314)


```
description:
    Example 47, p129

    P1: Some thermotogum stains gram-negative
    P2: Maritima is a thermotogum

    C: Maritima stains gram negative
    
v (Views): (
   ∃x {Thermotogum(x*)StainsGramNegative(x)},
   {Thermotogum(Maritima()*)}
)
c (Conclusion): {StainsGramNegative(Maritima())}
test(verbose=False): Method used to test the example
```

## e48
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1331)


```
description:
    Example 48, p130

    P1 Some dictyoglomus is thermophobic.
    P2 Turgidum is not a dictyoglomus.
    C Truth
    
v (Views): (
   ∃x {D(x*)T(x)},
   {~D(Turgidum()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e49
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1347)


```
description:
    Example 49, p130

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    
v (Views): (
   ∃y ∃x {Ace(Mary())King(x),Queen(John())Jack(y)},
   {King(Sally())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e50_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1364)


```
description:
    Example 50, part1, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v (Views): (
   {L(j(),s())L(s(),g())},
   {~M(g()*)M(j()*)},
   {},
   ∃a ∃b {~M(b*)M(a*)L(a,b)}
)
c (Conclusion): (
   {~M(g()*)M(j()*)L(j(),s())L(s(),g())},
   {0}
)
test(verbose=False): Method used to test the example
```

## e50_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1401)


```
description:
    Example 50, part2, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v (Views): (
   {L(j(),s())L(s(),g())},
   {~M(g())M(j())},
   {M(s())},
   ∃a ∃b {~M(b*)M(a*)L(a,b)}
)
c (Conclusion): ∃a ∃b {~M(b*)M(a*)L(a,b)}
g1 (Another View): {M(s())M(j())L(s(),g())~M(g())L(j(),s()),~M(s())M(j())L(s(),g())~M(g())L(j(),s())}
g2 (Another View): {M(s())M(j()*)L(s(),g())~M(g()*)L(j(),s()),~M(s()*)M(j()*)L(s(),g())~M(g()*)L(j(),s())}
test(verbose=False): Method used to test the example
```

## e50_part2_arbs
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1446)


```
description:
    Duplicate of e50, uses arb objects, some changes
    
v (Views): (
   ∃g ∃s ∃j {M(j)L(j,s)L(s,g)~M(g)},
   ∃s {M(s)},
   ∃a ∃b {~M(b*)M(a*)L(a,b)}
)
c (Conclusion): ∃a ∃b {~M(b*)M(a*)L(a,b)}
g1 (Another View): ∃g ∃s ∃j {M(j)L(j,s)L(s,g)M(s)~M(g),M(j)L(j,s)L(s,g)~M(s)~M(g)}
g2 (Another View): ∃g ∃s ∃j {M(j*)L(j,s)L(s,g)M(s)~M(g*),M(j*)L(j,s)L(s,g)~M(s*)~M(g*)}
test(verbose=False): Method used to test the example
```

## e51
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1477)


```
description:
    Example 51, p131

    P1: Every archaeon has a nucleus
    P2: Halobacterium is an archaeon

    C: Halobacterium is an archaeon and has a nucleus
    
v (Views): (
   ∀x {HasNucleus(x)IsArchaeon(x*)}^{IsArchaeon(x*)},
   {IsArchaeon(Halobacterium()*)}
)
c (Conclusion): {IsArchaeon(Halobacterium()*)HasNucleus(Halobacterium())}
test(verbose=False): Method used to test the example
```

## e52
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1494)


```
description:
    Example 52, p132

    P1 All Fs G.
    P2 John Gs.
    C John Fs and Gs.
    
v (Views): (
   ∀x {G(x*)F(x)}^{F(x)},
   {G(John()*)}
)
c (Conclusion): {G(John()*)F(John())}
test(verbose=False): Method used to test the example
```

## e53
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1510)


```
description:
    Example 53, p132 & p175

    P All A are B.
    C All B are A.
    
v (Views): (
   ∀x {A(x)B(x)}^{A(x)},
   ∀x {B(x)},
   ∀x {A(x)B(x)}^{B(x)}
)
c (Conclusion): ∀x {A(x)B(x)}^{B(x)}
test(verbose=False): Method used to test the example
```

## e53_does_it_follow
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1537)


```
v (Views): (
   ∀x {A(x)B(x)}^{A(x)},
   ∀x {B(x)},
   ∀x {A(x)B(x)}^{B(x)}
)
c (Conclusion): ∀x {A(x)B(x)}^{B(x)}
test(verbose=False): Method used to test the example
```

## e54
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1548)


```
description:
    Example 54, p133

    P1 Sharks attack bathers.
    P2 Whitey is a shark.
    C Whitey attacks bathers.
    
v (Views): (
   ∀x {0,Shark(x*)Attack(x)}^{Shark(x*)},
   {Shark(Whitey()*)}
)
c (Conclusion): {Shark(Whitey()*)Attack(Whitey())}
test(verbose=False): Method used to test the example
```

## e56_default_inference
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1581)


```
description:
    Example 56, p134

    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    
v (Views): (
   ∀x ∃y {Professor(x)Teaches(x,y)Student(y*)}^{Professor(x)},
   ∀z ∃w {Student(z*)Book(w)Reads(z,w)}^{Student(z*)}
)
c (Conclusion): ∃y ∃b {0,Book(b)Reads(y,b)}
test(verbose=False): Method used to test the example
```

## e56_basic_step
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1598)


```
v (Views): (
   ∀x ∃y {Professor(x)Teaches(x,y)Student(y*)}^{Professor(x)},
   ∀z ∃w {Student(z*)Book(w)Reads(z,w)}^{Student(z*)}
)
c (Conclusion): ∀a ∃b ∃c {Reads(b,c)Teaches(a,b)Professor(a)Book(c)Student(b*),~Professor(a)}
test(verbose=False): Method used to test the example
```

## e57
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1604)


```
description:
    Example 57, p134

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    
v (Views): (
   ∀x {A(x)B(x*)}^{B(x*)},
   ∃x {C(x)B(x*)}
)
c (Conclusion): ∃y {C(y)B(y*)A(y)}
test(verbose=False): Method used to test the example
```

## e58_reversed
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1620)


```
description:
    Example 58 reversed, based on p135

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    
v (Views): (
   ∀y {C(y)B(y*)}^{C(y)},
   ∃x {A(x)B(x*)}
)
c (Conclusion): ∃y {C(y)B(y*)A(y)}
test(verbose=False): Method used to test the example
```

## e61
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1636)


```
description:
    Example 61, p166
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    
v (Views): (
   ∀x ∃a {~D(x),D(x)B(x,a)M(a*)},
   {M(j()*)}
)
c (Conclusion): ∀x ∃a {D(x)B(x,a)M(j()*)M(a*),~D(x)M(j()*)}
test(verbose=False): Method used to test the example
```

## e62
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1649)


```
description:
    Example 62, p176
    
v (Views): (
   {S(m()*)L(n(),m()),S(j()*)T(n())D(m()),D(b())~S(n()*)},
   ∃a {S(a*)}
)
c (Conclusion): {0,S(j()*),S(m()*)}
test(verbose=False): Method used to test the example
```

## e63
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1661)


```
description:
    Example 63, p176
    
v (Views): (
   {D(n()*)S(j()*),D(n()*)T(j())~D(j()*)},
   ∃a {D(a*)}
)
c (Conclusion): {D(n()*)}
test(verbose=False): Method used to test the example
```

## e63_modified
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1673)


```
description:
    Example 63, p176
    
v (Views): (
   ∀x ∃y {D(n()*)S(j()*),T(j())D(f(y,x)*)~D(j()*)},
   ∃a {D(a*)}
)
c (Conclusion): ∀x ∃y {D(n()*),D(f(y,x)*)}
test(verbose=False): Method used to test the example
```

## e64i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1685)


```
description:
    Example 64, p189, p223

    A device has been invented for screening a population for a disease known as psylicrapitis.
    The device is a very good one, but not perfect. If someone is a sufferer, there is a 90% chance
    that he will recorded positively. If he is not a sufferer, there is still a 1% chance that he will
    be recorded positively.

    Roughly 1% of the population has the disease. Mr Smith has been tested, and the result is positive.

    What is the chance that he is in fact a sufferer?
    
v (Views): (
   ∀x {90.0=* S(x*)T(x*),S(x*)~T(x)}^{S(x*)},
   ∀x {1.0=* T(x)~S(x*),~S(x*)~T(x)}^{~S(x*)},
   {T(Smith()*)},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*),0}
test(verbose=False): Method used to test the example
```

## e64ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1717)


```
v (Views): (
   ∀x {90.0=* T(x*)S(x*)P(x),S(x*)P(x)~T(x)}^{S(x*)P(x)},
   ∀x {1.0=* T(x)~S(x*)P(x),~S(x*)P(x)~T(x)}^{~S(x*)P(x)},
   ∀x {1.0=* S(x*)P(x),~S(x)P(x)}^{P(x)},
   {T(Smith()*)P(Smith())},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*)}
test(verbose=False): Method used to test the example
```

## e65
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1737)


```
description:
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
    
v (Views): (
   ∀x {0.3=* C(x)P(x*),~C(x)P(x*)}^{P(x*)},
   ∀x {50.0=* T(x)C(x)P(x*),C(x)P(x*)~T(x)}^{C(x)P(x*)},
   ∀x {3.0=* ~C(x)T(x)P(x*),~C(x)P(x*)~T(x)}^{~C(x)P(x*)},
   ∃a {T(a)P(a*)},
   ∃a {C(a)}
)
c (Conclusion): ∃a {15.0=* C(a),0}
test(verbose=False): Method used to test the example
```

## e66i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1771)


```
description:
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ?
    
v (Views): (
   {1.0=* T()D(),1.0=* ~D()T(),98.0=* ~D()},
   {T()D()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e66ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1799)


```
v (Views): (
   {1.0=* T()D(),1.0=* ~D()T(),98.0=* ~D()},
   {T()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e67
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1816)


```
description:
    Example 67, p191, p220

    Results of a recent survey of seventy-four chief executive officers indicate there
    may be a link between childhood pet ownership and future career success. Fully 94%
    of the CEOs, all of them employed within Fortune 500 companies, had possessed a dog,
    a cat, or both, as youngsters.
    
v (Views): (
   {94.0=* IsCEO()HadPet(),~IsCEO()},
   {HadPet()},
   {IsCEO()}
)
c (Conclusion): {94.0=* IsCEO(),0}
test(verbose=False): Method used to test the example
```

## e69_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1845)


```
description:
    Example 69, p192, p218

    The suspect's DNA matches the crime sample.

    If the suspect is not guilty, then the probability of such a DNA match is 1 in
    a million

    Is the suspect likely to be guilty?
    
v (Views): (
   {Match(Suspect())},
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),~Match(Suspect())~Guilty(Suspect())}^{~Guilty(Suspect())}
)
c (Conclusion): {0.000001=* ~Guilty(Suspect())Match(Suspect()),Guilty(Suspect())Match(Suspect())}
test(verbose=False): Method used to test the example
```

## e69_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1879)


```
v (Views): (
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),Guilty(Suspect())Match(Suspect())},
   {999999.999999=* 0}^{Guilty(Suspect())Match(Suspect())},
   {Guilty(Suspect())}
)
c (Conclusion): (
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),999999.999999=* Guilty(Suspect())Match(Suspect())},
   {999999.999999=* Guilty(Suspect()),0}
)
test(verbose=False): Method used to test the example
```

## e70
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1906)


```
description:
    Example 70, p194, p221

    P1 Pat has either the disease or a benign condition
    P2 If she has the disease, then she will have a certain symptom.
    P3 In fact, she has the symptom
    
v (Views): (
   {Disease(),Benign()},
   {Symptom()Disease()}^{Disease()},
   {Symptom()}
)
c (Conclusion): {Symptom()Disease()}
test(verbose=False): Method used to test the example
```

## e71
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1931)


```
description:
    Examples 71 & 78, p209, p212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    
v (Views): (
   {~B(brown())B(yellow()),B(brown())~B(yellow())},
   {50.0=* 0}^{~B(brown())B(yellow())},
   {50.0=* 0}^{B(brown())~B(yellow())},
   {~B(brown())B(yellow())}
)
c (Conclusion): (
   {50.0=* ~B(brown())B(yellow()),50.0=* B(brown())~B(yellow())},
   {50.0=* ~B(brown())B(yellow()),0}
)
test(verbose=False): Method used to test the example
```

## e72
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1968)


```
description:
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    
v (Views): (
   {B(b())~B(r())B(g()),~B(g())B(r()),~B(b())B(r())},
   {33.333333=* 0}^{B(b())~B(r())B(g())},
   {33.333333=* 0}^{~B(g())B(r())},
   {33.333333=* 0}^{~B(b())B(r())},
   {B(b())B(r())}
)
c (Conclusion): (
   {33.333333=* B(b())~B(r())B(g()),33.333333=* ~B(g())B(r()),33.333333=* ~B(b())B(r())},
   {33.333333=* B(b())B(r()),0}
)
test(verbose=False): Method used to test the example
```

## e74
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2012)


```
description:
    Example 74, p197, p231

    (includes two background commitments)
    
v (Views): (
   {H(j())D(j()),H(j()),P(j())},
   {E(j()*)},
   ∀x {0.85=* E(x*)D(x),0.15=* E(x*)~D(x)}^{E(x*)},
   ∀x {0.1=* E(x*)H(x),0.9=* E(x*)~H(x)}^{E(x*)}
)
c (Conclusion): (
   {0.085=* H(j())E(j()*)D(j()),0.765=* E(j()*)~H(j())D(j()),0.015=* ~D(j())H(j())E(j()*),0.135=* ~D(j())E(j()*)~H(j())},
   {H(j())D(j())}
)
test(verbose=False): Method used to test the example
```

## e76
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2048)


```
description:
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    
v (Views): (
   {Gun(i())Guitar(j())Outoftune(j())Fired(i()*),Attic(a())},
   ∀x {Gun(x)Fired(x*)Trigger(x),0}^{Gun(x)Fired(x*)},
   {Trigger(i())}
)
c (Conclusion): {Outoftune(j())Guitar(j())Gun(i())Fired(i()*)Trigger(i())}
test(verbose=False): Method used to test the example
```

## e81i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2090)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),~Box(Yellow())Box(Brown())}
)
c (Conclusion): {50.0=* Box(Yellow()),0}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2100)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card and a brown card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),~Box(Yellow())Box(Brown())}
)
c (Conclusion): {0}
prob (Probability): {Box(Yellow())Box(Brown())}
test(verbose=False): Method used to test the example
```

## e81iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2110)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is neither a yellow card nor a brown card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),~Box(Yellow())Box(Brown())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2133)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card.
    
v (Views): (
   {Box(Yellow())Box(Brown())}^{Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Yellow()),0}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2143)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and a brown card.
    
v (Views): (
   {Box(Yellow())Box(Brown())}^{Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Yellow())Box(Brown()),0}
prob (Probability): {Box(Yellow())Box(Brown())}
test(verbose=False): Method used to test the example
```

## e82iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2153)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and there is not a brown card.
    
v (Views): (
   {Box(Yellow())Box(Brown())}^{Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2163)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is neither a yellow card nor a brown card.
    
v (Views): (
   {Box(Yellow())Box(Brown())}^{Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e83i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2192)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a red marble and blue in marble in the box.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* ~Box(Blue())~Box(Green())~Box(Red())}
)
c (Conclusion): {0}
prob (Probability): {Box(Blue())Box(Red())}
test(verbose=False): Method used to test the example
```

## e83ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2202)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a green marble and there is a blue marble.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* ~Box(Blue())~Box(Green())~Box(Red())}
)
c (Conclusion): {33.333333333333336=* Box(Blue())Box(Green()),0}
prob (Probability): {Box(Blue())Box(Green())}
test(verbose=False): Method used to test the example
```

## e84i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2215)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(Mauve())Box(Grey())Box(White()),~Box(White())Box(Grey())Box(Mauve())}
)
c (Conclusion): {50.0=* Box(Grey())Box(Mauve()),0}
prob (Probability): {Box(Grey())Box(Mauve())}
test(verbose=False): Method used to test the example
```

## e84ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2237)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(White())~Box(Mauve())Box(Grey()),~Box(Mauve())~Box(Grey())Box(White()),~Box(White())~Box(Grey())Box(Mauve())}
)
c (Conclusion): {0}
prob (Probability): {Box(Grey())Box(Mauve())}
test(verbose=False): Method used to test the example
```

## e85
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2260)


```
description:
    Example 85, p216

    Easy partial probability inference

    There is a box in which there is one and only one of these marbles: a
    green marble, a blue marble, or a red marble. The probability that a green
    marble is in the box is 0.6, and the probability that a blue marble is in
    the box is 0.2.

    What is the probability that a red marble is in the box?
    
v (Views): (
   {Box(Green()),Box(Blue()),Box(Red())},
   {60.0=* Box(Green())}^{Box(Green())},
   {20.0=* Box(Blue())}^{Box(Blue())}
)
c (Conclusion): {20.0=* Box(Red()),0}
prob (Probability): {Box(Red())}
test(verbose=False): Method used to test the example
```

## e86
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2283)


```
description:
    Example 86, p217

    You have a hand of several cards with only limited information about it.

    There is an ace and a queen or a king and a jack or a ten.
    The probability that there is an ace and a queen is 0.6
    The probability that there is a king and a jack is 0.2

    What is the probability that there is a ten?
    
v (Views): (
   {Q()A(),J()K(),X()},
   {60.0=* Q()A()}^{Q()A()},
   {20.0=* J()K()}^{J()K()}
)
c (Conclusion): {20.0=* X(),0}
prob (Probability): {X()}
test(verbose=False): Method used to test the example
```

## e88
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2305)


```
description:
    Example 88, p233

    P1: There is a 90% chance Superman can fly
    P2: Clark is superman

    C: There is a 90% chance Clark can fly
    
v (Views): (
   {90.0=* CanFly(Superman())},
   {==(Clark(),Superman())},
   {==(Clark(),Superman()*)},
   {==(Clark(),Clark())}
)
c (Conclusion): {90.0=* CanFly(Clark())}
test(verbose=False): Method used to test the example
```

## e90_condA
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2335)


```
description:
    Example 90, p249, p273

    Imagine that you have been saving some extra money on the side to make some purchases,
    and on your most recent visit to the video store you come across a special sale of a new
    video. This video is one with your favourite actor or actress, and your favourite type of
    movie (such as a comedy, drama, thriller etc.). This particular video that you are considering
    is one you have been thinking about buying a long time. It is a available at a special sale price
    of $14.99. What would you do in this situation?
    
v (Views): (
   {do(Buy(Video()*)),~do(Buy(Video()))}
)
c (Conclusion): {do(Buy(Video()*))}
cv (Consequence Views): (
   ∀x {Fun()}^{do(Buy(x*))}
)
pr (Priority Views): (
   {1.0=+ 0}^{Fun()}
)
test(verbose=False): Method used to test the example
```

## e90_condB
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2353)


```
v (Views): (
   ∃a {do(Buy(Video()*)),do(Buy(a*))}
)
c (Conclusion): ∃a {do(Buy(Video()*)),do(Buy(a*))}
cv (Consequence Views): (
   ∀x {Fun()}^{do(Buy(x*))}
)
pr (Priority Views): (
   {1.0=+ 0}^{Fun()}
)
test(verbose=False): Method used to test the example
```

## e92_award
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2389)


```
description:
    Example 92, p253, p274
    Imagine that you serve on the jury of an only-child sole-custody case following a relatively
    messy divorce. The facts of the case are complicated by ambiguous economic, social, and
    emotional considerations, and you decide to base your decision entirely on the following
    few observations.

    ParentA: average income, average health, average working hours, reasonable rapport with the
    child, relatively social life.

    ParentB: above-average income, very close relationship with the child, extremely active
    social life, lots of work-related travel, minor health problems.
    
    To which parent would you award sole custody of the child?
    
v (Views): (
   {do(Award(ParentA()*)),do(Award(ParentB()*))}
)
c (Conclusion): {do(Award(ParentB()*))}
cv (Consequence Views): (
   ∀x {Custody(x*)}^{do(Award(x*))},
   ∀x {~Custody(x*)}^{do(Deny(x*))},
   {HighRapp(ParentB())MedRapp(ParentA())MedTime(ParentA())LowTime(ParentB())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{MedRapp(x)Custody(x*)},
   ∀x {3.0=+ 0}^{HighRapp(x)Custody(x*)},
   ∀x {1.0=+ 0}^{MedTime(x)Custody(x*)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{~Custody(x*)LowTime(x)}
)
test(verbose=False): Method used to test the example
```

## e92_deny
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2400)


```
description:
    Example 92, p253, p274
    Imagine that you serve on the jury of an only-child sole-custody case following a relatively
    messy divorce. The facts of the case are complicated by ambiguous economic, social, and
    emotional considerations, and you decide to base your decision entirely on the following
    few observations.

    ParentA: average income, average health, average working hours, reasonable rapport with the
    child, relatively social life.

    ParentB: above-average income, very close relationship with the child, extremely active
    social life, lots of work-related travel, minor health problems.
    
    To which parent would you deny sole custody of the child?
    
v (Views): (
   {do(Deny(ParentA()*)),do(Deny(ParentB()*))}
)
c (Conclusion): {do(Deny(ParentB()*))}
cv (Consequence Views): (
   ∀x {Custody(x*)}^{do(Award(x*))},
   ∀x {~Custody(x*)}^{do(Deny(x*))},
   {HighRapp(ParentB())MedRapp(ParentA())MedTime(ParentA())LowTime(ParentB())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{MedRapp(x)Custody(x*)},
   ∀x {3.0=+ 0}^{HighRapp(x)Custody(x*)},
   ∀x {1.0=+ 0}^{MedTime(x)Custody(x*)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{~Custody(x*)LowTime(x)}
)
test(verbose=False): Method used to test the example
```

## e93_grp1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2410)


```
description:
    Example 93, p255, p276

    The US is preparing for the outbreak of an unusual Asian disease, which
    is expected to kill 600 people. There are two possible treatments (A) and (B)
    with the following results:

    (Group 1) (A) 400 people die. (B) Nobody dies with 1/3 chance, 600 people die with 2/3 chance.
    Which treatment would you choose?
    
v (Views): (
   {do(A()),do(B())}
)
c (Conclusion): {do(B())}
cv (Consequence Views): (
   {D(400.0*)}^{do(A())},
   {0.33=* D(0.0*),~D(0.0)}^{do(B())},
   {0.67=* D(600.0*),~D(600.0)}^{do(B())}
)
pr (Priority Views): (
   ∀x {power(σ(log(σ(x,1.0)),1.0),-1.0)=+ 0}^{D(x*)},
   ∀x {σ(log(σ(x,1.0)),1.0)=+ 0}^{S(x*)}
)
test(verbose=False): Method used to test the example
```

## new_e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2452)


```
v (Views): (
   ∀x ∃a ∀y {P(x,a)Q(a,y)},
   ∃b ∀z {P(b,z)}
)
c (Conclusion): ∃b ∀z ∀x ∃a ∀y {P(x,a)Q(a,y)P(b,z)}
test(verbose=False): Method used to test the example
```

## new_e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2463)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x ∃b {Q(x*)R(b)P(a)}
test(verbose=False): Method used to test the example
```

## else_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2481)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_merge
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2485)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_suppose
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2489)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_uni_prod
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2493)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_query
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2502)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_which
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2506)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## new_e5
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2510)


```
v (Views): (
   ∀x ∀y ∃a ∃b ∀z ∃c {P(c)Q(x*)P(y)P(a*)P(z)P(b)},
   ∃f ∃e ∃d {Q(e*)Q(f*)P(d*)}
)
c (Conclusion): ∃f ∃e ∃d {Q(e*)Q(f*)P(d*)}
test(verbose=False): Method used to test the example
```

## new_e6_leibniz
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2518)


```
v (Views): (
   ∃b ∃a {P(f(a),a)==(a,b)~P(f(b),a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e7_aristotle
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2523)


```
v (Views): (
   ∃a {~==(a,a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2528)


```
v (Views): (
   {t()=+ A()},
   {u()=* A()}
)
c (Conclusion): {u()=* t()=+ A()}
test(verbose=False): Method used to test the example
```

## new_e9
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2533)


```
v (Views): (
   ∀x {P(x*)},
   {P(j()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## new_e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2538)


```
v (Views): (
   ∀x {f(x)=* A(x*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2543)


```
v (Views): (
   {f(12.0)=* A(12.0*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e12
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2548)


```
v (Views): (
   {A()},
   {}
)
c (Conclusion): {A()}
test(verbose=False): Method used to test the example
```

## new_e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2553)


```
v (Views): (
   {f(12.0)=* A(12.0*),B()}
)
c (Conclusion): {}
prob (Probability): ∃e {A(e*)}
test(verbose=False): Method used to test the example
```

## new_e14
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2559)


```
v (Views): (
   ∀x ∃y {B(g(x*,y))A(f(x*))},
   {A(f(j()*))}
)
c (Conclusion): ∃y {A(f(j()*))B(g(j()*,y))}
test(verbose=False): Method used to test the example
```

## new_e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2564)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}
)
c (Conclusion): ∃k {Defeats(k,Clark())==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2572)


```
v (Views): (
   ∃x ∃k {==(Clark(),x)Defeats(k,x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {Defeats(k,Clark())==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2577)


```
v (Views): (
   ∃x ∃k {==(Clark(),x)do(Defeats(k,x))},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {do(Defeats(k,Clark()))==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e18
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2582)


```
v (Views): (
   {m()=* A()},
   {n()=* B()}
)
c (Conclusion): {m()**n()=* B()A()}
test(verbose=False): Method used to test the example
```

## new_e19_first_atom_do_atom
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2587)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {do(A())}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e20_nested_issue_in_pred
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2592)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark(),f(Superman()*))}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e21_supp_is_something
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2600)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}^{}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e22_restrict_dep_rel_is_not_other
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2608)


```
v (Views): (
   ∃x ∃k {==(Clark(),x)do(Defeats(k,x))},
   ∃y {==(Clark()*,y)}
)
c (Conclusion): ∃x ∃k {==(Clark(),x)do(Defeats(k,x))}
test(verbose=False): Method used to test the example
```

## AnswerPotential
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2613)


```
v (Views): (
   {1.0=* 2.0=+ B()A(),0.4=* B()C(),C()A()},
   {A()},
   {B()},
   {C()},
   {C()D()},
   {C()~B()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## UniProduct
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2655)


```
v (Views): (
   ∀x ∃a {E(x,a)P(x),~P(x*)},
   {P(j()*)}
)
c (Conclusion): ∃a {~P(j()*),E(j(),a)P(j())}
test(verbose=False): Method used to test the example
```

## QueryTest
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2660)


```
description:
    From page 173
    
v (Views): (
   ∀x {S(m()*)S(j()*)T(x,m()),S(m()*)S(j()*)T(x,j())},
   ∀x ∃a {S(a*)T(x,a)}
)
c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```

## QueryTest2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2672)


```
description:
    From page 173
    
v (Views): (
   ∀x {S(m()*)S(j()*)T(x,m()),S(m()*)S(j()*)T(x,j())},
   ∃a ∀x {S(a*)T(x,a)}
)
c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```