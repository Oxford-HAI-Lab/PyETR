# Case Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L391)


```
description:
    Example 1, p61:

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else
    Mark is standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire.
    C Jane is looking at the TV.
    
v (Views): (
   {LookingAtTV(Jane())KneelingByTheFire(Jane()),PeeringIntoTheGarden(Mark())StandingAtTheWindow(Mark())},
   {KneelingByTheFire(Jane())}
)
c (Conclusion): {LookingAtTV(Jane())}
test(verbose=False): Method used to test the example
```

## e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L410)


```
description:
    Example 2, p62:

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    
v (Views): (
   {T()K(),Q()A()},
   {K()}
)
c (Conclusion): {T()}
test(verbose=False): Method used to test the example
```

## e3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L426)


```
description:
    Example 3, p63:

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v (Views): (
   {King()Ace(),Jack()Queen()},
   {~Ace()}
)
c (Conclusion): {Jack()Queen()}
test(verbose=False): Method used to test the example
```

## e5ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L453)


```
description:
    Example 5, p72, part ii
    
v (Views): (
   {r1()s1(),q1()p1()},
   {q2()p2(),s2()r2()}
)
c (Conclusion): {q2()p2()r1()s1(),s2()r1()r2()s1(),s2()q1()r2()p1(),q2()p2()q1()p1()}
test(verbose=False): Method used to test the example
```

## e5iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L467)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L479)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L491)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L503)


```
description:
    Example 6, p72

    There is an Ace and a King = (There is an Ace) x (There is a king)
    
v (Views): (
   {a()},
   {k()}
)
c (Conclusion): {k()a()}
test(verbose=False): Method used to test the example
```

## e7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L514)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L525)


```
description:
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    
v (Views): (
   {k()t(),q()a()},
   {k()}
)
c (Conclusion): {t()}
test(verbose=False): Method used to test the example
```

## e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L539)


```
description:
    Example 10, p76

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a ten.
    
v (Views): (
   {K(x())},
   {T(w())K(z()),A(x())Q(y())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L555)


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
c (Conclusion): {Smokes(j())Drinks(j()),Smokes(m())Eats(m())}
test(verbose=False): Method used to test the example
```

## e12i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L573)


```
description:
    Example 12i, p78

    ItisnotthecasethatPorQorR
    
v (Views): (
   {P(),Q(),R()}
)
c (Conclusion): {~Q()~P()~R()}
test(verbose=False): Method used to test the example
```

## e12ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L584)


```
description:
    Example 12ii, p78

    ItisnotthecasethatPandQandR
    
v (Views): (
   {P()Q()R()}
)
c (Conclusion): {~R(),~P(),~Q()}
test(verbose=False): Method used to test the example
```

## e12iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L595)


```
description:
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    
v (Views): (
   {P()Q(),R()}^{S()}
)
c (Conclusion): {~P()S()~R(),~Q()S()~R()}
test(verbose=False): Method used to test the example
```

## e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L606)


```
description:
    Example 13, p80

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v (Views): (
   {IsQueen()IsJack(),IsKing()IsAce()},
   {~IsAce()}
)
c (Conclusion): {IsQueen()IsJack()}
test(verbose=False): Method used to test the example
```

## e14_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L622)


```
description:
    Example 14-1, p81

    Factor examples
    
v (Views): (
   {P()R(),P()Q()},
   {P()}
)
c (Conclusion): {Q(),R()}
test(verbose=False): Method used to test the example
```

## e14_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L636)


```
description:
    Example 14-2, p81

    Factor examples
    
v (Views): (
   {P()R(),P()S()R(),P()Q()S()},
   {P()}^{S()}
)
c (Conclusion): {Q()S(),P()R(),S()R()}
test(verbose=False): Method used to test the example
```

## e14_3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L650)


```
description:
    Example 14-3, p81

    Factor examples
    
v (Views): (
   {P()S(),Q()S(),P()R(),Q()R()},
   {P(),Q()}
)
c (Conclusion): {S(),R()}
test(verbose=False): Method used to test the example
```

## e14_6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L664)


```
description:
    Example 14-6, p81

    Factor examples
    
v (Views): (
   {Q()S(),P()R()},
   {T(),P(),Q()}
)
c (Conclusion): {Q()S(),P()R()}
test(verbose=False): Method used to test the example
```

## e14_7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L678)


```
description:
    Example 14-7, p81

    Factor examples
    
v (Views): (
   {Q()S(),P()R(),P()},
   {P(),Q()}
)
c (Conclusion): {0,S(),R()}
test(verbose=False): Method used to test the example
```

## e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L692)


```
description:
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    
v (Views): (
   {Ace(),Ace()Jack()Queen(),Eight()Four()Ten()},
   {Ace()Jack()Eight()Ten()},
   {~Queen()}
)
c (Conclusion): {Four()}
test(verbose=False): Method used to test the example
```

## e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L710)


```
description:
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    
v (Views): (
   {King()Jack()Queen(),Ace(),Eight()Four()Ten()},
   {~Four()},
   {~Ace()}
)
c (Conclusion): {King()Jack()Queen()}
test(verbose=False): Method used to test the example
```

## e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L727)


```
description:
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    
v (Views): (
   {Ace()~King(),King()~Ace()},
   {King()}
)
c (Conclusion): {~Ace()}
test(verbose=False): Method used to test the example
```

## e19
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L743)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L757)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L775)


```
description:
    Example 21, p86

    Any view Δ^{0} = [Δ^{0}]ᶰ can be derived from the absurd view
    
v (Views): (
   {r1()s1()}
)
c (Conclusion): {~r1(),~s1()}
test(verbose=False): Method used to test the example
```

## e22
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L793)


```
description:
    Example 22, p87

    It is not the case that A and B and C
    
v (Views): (
   {a()c()b()},
   {a()},
   {b()},
   {c()}
)
c (Conclusion): (
   {~c(),~b(),~a()},
   {~c()a()~b(),~c()~a()~b(),~c()b()~a(),~c()a()b(),a()c()~b(),b()~a()c(),c()~a()~b()}
)
test(verbose=False): Method used to test the example
```

## e23_with_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L832)


```
description:
    Example 23, p88, with inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v (Views): (
   {L()K(),P()S()},
   {K()}
)
c (Conclusion): (
   {P()S()~K(),L()K(),P()S()K()},
   {L()K(),P()S()K()}
)
test(verbose=False): Method used to test the example
```

## e23_without_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L868)


```
description:
    Example 23, p88, without inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v (Views): (
   {L()K(),P()S()},
   {K()}
)
c (Conclusion): (
   {L()K(),P()S()},
   {L()K()}
)
test(verbose=False): Method used to test the example
```

## e24
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L900)


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
   {a()~q(),q()a()},
   {a(),q()}
)
test(verbose=False): Method used to test the example
```

## e25i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L933)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L942)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L951)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L963)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L975)


```
description:
    Example 25v, p89
    
v (Views): (
   {q()s()p(),r()s()p()},
   {p()}^{s()}
)
c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25vi
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L987)


```
description:
    Example 25vi, p89
    
v (Views): (
   {q()s()p(),r()s()p()},
   {p()}^{t()}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e26
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L999)


```
description:
    Example 26, p90

    P1 Either John plays and wins, or Mary plays, or Bill plays
    C Supposing John plays, John wins
    
v (Views): (
   {Win(J())Play(J()),Play(B()),Play(M())},
   {Play(J())},
   {Win(J())}^{Play(J())}
)
c (Conclusion): (
   {Win(J())Play(J())}^{Play(J())},
   {Win(J())}^{Play(J())}
)
test(verbose=False): Method used to test the example
```

## e26_does_it_follow
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1032)


```
v (Views): (
   {Win(J())Play(J()),Play(B()),Play(M())},
   {Play(J())},
   {Win(J())}^{Play(J())}
)
c (Conclusion): (
   {Win(J())Play(J())}^{Play(J())},
   {Win(J())}^{Play(J())}
)
test(verbose=False): Method used to test the example
```

## e28
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1043)


```
description:
    Example 28, p96

    P1 Is there a tiger?
    P2 Supposing there is a tiger, there is orange fur.
    P3 There is orange fur.
    C There is a tiger.
    
v (Views): (
   {~Tiger(),Tiger()},
   {Orange()Tiger()}^{Tiger()},
   {Orange()}
)
c (Conclusion): {Orange()Tiger()}
test(verbose=False): Method used to test the example
```

## e32_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1061)


```
description:
    Example 32-1, p107

    P1 If P then Q.
    P2 P
    C Q
    
v (Views): (
   {P()Q()}^{P()},
   {P()}
)
c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e32_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1077)


```
description:
    Example 32-2, p107

    P1 P
    P2 If P then Q.
    C Q
    
v (Views): (
   {P()},
   {P()Q()}^{P()}
)
c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e33
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1093)


```
description:
    Example 33, p108

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    
v (Views): (
   {E()R()}^{R()},
   {E()}
)
c (Conclusion): {R()}
test(verbose=False): Method used to test the example
```

## e40i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1109)


```
description:
    Example 40, p119

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    
v (Views): (
   {SquareB()~CircleB()~TriangleB(),~SquareB()~TriangleB()CircleB(),TriangleB()~CircleB()~SquareB()},
   {SquareB()CircleT()}^{CircleT()},
   {TriangleB()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e40ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1142)


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
   {SquareB()~CircleB()~TriangleB(),~SquareB()~TriangleB()CircleB(),TriangleB()~CircleB()~SquareB()},
   {TriangleB()},
   {SquareB()CircleT()}^{CircleT()}
)
c (Conclusion): {~CircleT()TriangleB()~CircleB()~SquareB()}
test(verbose=False): Method used to test the example
```

## e41
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1179)


```
description:
    Example 41, p121

    P1 P only if Q.
    P2 Not Q.
    C Not P.
    
v (Views): (
   {~Q()~P()}^{~Q()},
   {~Q()}
)
c (Conclusion): {~P()}
test(verbose=False): Method used to test the example
```

## e42
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1195)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1215)


```
description:
    Example 44-1, p123

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    
v (Views): (
   {Elegant(c())Saleable(c()),~Elegant(c())~Saleable(c())},
   {~Elegant(c())~Stable(c()),Elegant(c())Stable(c())},
   {Elegant(c())Saleable(c()),Stable(c()),Saleable(c())}
)
c (Conclusion): {Elegant(c())Saleable(c())Stable(c())}
test(verbose=False): Method used to test the example
```

## e45
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1233)


```
description:
    Example 45, p125

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    
v (Views): (
   {0,M()},
   {0,B()},
   {0,M()B()}
)
c (Conclusion): (
   {0,M(),B(),M()B()},
   {0,M()B()}
)
test(verbose=False): Method used to test the example
```

## e46i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1260)


```
description:
    Example 46, p126

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    
v (Views): (
   {P()V()}^{P()},
   {M()~P(),P()~M()},
   {0,M()V()}
)
c (Conclusion): (
   {M()~P(),P()V()~M()},
   {0}
)
test(verbose=False): Method used to test the example
```

## e46ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1297)


```
description:
    Example 46, part ii, p126

    If we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
    
v (Views): (
   {M()V()S(),M()V()R(),T()},
   {0,M()V()}
)
c (Conclusion): {0,M()V()}
test(verbose=False): Method used to test the example
```

## e47
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1311)


```
description:
    Example 47, p129

    P1: Some thermotogum stains gram-negative
    P2: Maritima is a thermotogum

    C: Maritima stains gram negative
    
v (Views): (
   ∃x {StainsGramNegative(x)Thermotogum(x*)},
   {Thermotogum(Maritima()*)}
)
c (Conclusion): {StainsGramNegative(Maritima())}
test(verbose=False): Method used to test the example
```

## e48
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1328)


```
description:
    Example 48, p130

    P1 Some dictyoglomus is thermophobic.
    P2 Turgidum is not a dictyoglomus.
    C Truth
    
v (Views): (
   ∃x {T(x)D(x*)},
   {~D(Turgidum()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e49
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1344)


```
description:
    Example 49, p130

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    
v (Views): (
   ∃x ∃y {Ace(Mary())King(x),Queen(John())Jack(y)},
   {King(Sally())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e50_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1361)


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
   {~M(g()*)L(j(),s())M(j()*)L(s(),g())},
   {0}
)
test(verbose=False): Method used to test the example
```

## e50_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1398)


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
g1 (Another View): {L(j(),s())~M(g())L(s(),g())M(s())M(j()),~M(s())L(j(),s())~M(g())L(s(),g())M(j())}
g2 (Another View): {L(j(),s())~M(g()*)L(s(),g())M(s())M(j()*),~M(s()*)L(j(),s())~M(g()*)L(s(),g())M(j()*)}
test(verbose=False): Method used to test the example
```

## e50_part2_arbs
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1443)


```
description:
    Duplicate of e50, uses arb objects, some changes
    
v (Views): (
   ∃j ∃g ∃s {L(j,s)~M(g)L(s,g)M(j)},
   ∃s {M(s)},
   ∃a ∃b {~M(b*)M(a*)L(a,b)}
)
c (Conclusion): ∃a ∃b {~M(b*)M(a*)L(a,b)}
g1 (Another View): ∃j ∃g ∃s {M(j)L(s,g)M(s)L(j,s)~M(g),M(j)L(s,g)L(j,s)~M(g)~M(s)}
g2 (Another View): ∃j ∃g ∃s {M(j*)L(s,g)M(s)L(j,s)~M(g*),M(j*)L(s,g)L(j,s)~M(g*)~M(s*)}
test(verbose=False): Method used to test the example
```

## e51
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1474)


```
description:
    Example 51, p131

    P1: Every archaeon has a nucleus
    P2: Halobacterium is an archaeon

    C: Halobacterium is an archaeon and has a nucleus
    
v (Views): (
   ∀x {IsArchaeon(x*)HasNucleus(x)}^{IsArchaeon(x*)},
   {IsArchaeon(Halobacterium()*)}
)
c (Conclusion): {IsArchaeon(Halobacterium()*)HasNucleus(Halobacterium())}
test(verbose=False): Method used to test the example
```

## e52
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1491)


```
description:
    Example 52, p132

    P1 All Fs G.
    P2 John Gs.
    C John Fs and Gs.
    
v (Views): (
   ∀x {F(x)G(x*)}^{F(x)},
   {G(John()*)}
)
c (Conclusion): {F(John())G(John()*)}
test(verbose=False): Method used to test the example
```

## e53
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1507)


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

## e54
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1534)


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
c (Conclusion): {Attack(Whitey())Shark(Whitey()*)}
test(verbose=False): Method used to test the example
```

## e56_default_inference
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1567)


```
description:
    Example 56, p134

    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    
v (Views): (
   ∀x ∃y {Student(y*)Professor(x)Teaches(x,y)}^{Professor(x)},
   ∀z ∃w {Reads(z,w)Student(z*)Book(w)}^{Student(z*)}
)
c (Conclusion): ∃y ∃b {0,Reads(y,b)Book(b)}
test(verbose=False): Method used to test the example
```

## e56_basic_step
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1584)


```
v (Views): (
   ∀x ∃y {Student(y*)Professor(x)Teaches(x,y)}^{Professor(x)},
   ∀z ∃w {Reads(z,w)Student(z*)Book(w)}^{Student(z*)}
)
c (Conclusion): ∀a ∃b ∃c {Professor(a)Student(b*)Book(c)Teaches(a,b)Reads(b,c),~Professor(a)}
test(verbose=False): Method used to test the example
```

## e57
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1590)


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
c (Conclusion): ∃y {B(y*)C(y)A(y)}
test(verbose=False): Method used to test the example
```

## e58_reversed
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1606)


```
description:
    Example 58 reversed, based on p135

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    
v (Views): (
   ∀y {B(y*)C(y)}^{C(y)},
   ∃x {A(x)B(x*)}
)
c (Conclusion): ∃y {B(y*)C(y)A(y)}
test(verbose=False): Method used to test the example
```

## e61
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1622)


```
description:
    Example 61, p166
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    
v (Views): (
   ∀x ∃a {~D(x),M(a*)B(x,a)D(x)},
   {M(j()*)}
)
c (Conclusion): ∀x ∃a {M(a*)B(x,a)D(x)M(j()*),~D(x)M(j()*)}
test(verbose=False): Method used to test the example
```

## e62
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1635)


```
description:
    Example 62, p176
    
v (Views): (
   {L(n(),m())S(m()*),S(j()*)T(n())D(m()),~S(n()*)D(b())},
   ∃a {S(a*)}
)
c (Conclusion): {0,S(j()*),S(m()*)}
test(verbose=False): Method used to test the example
```

## e63
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1647)


```
description:
    Example 63, p176
    
v (Views): (
   {S(j()*)D(n()*),~D(j()*)T(j())D(n()*)},
   ∃a {D(a*)}
)
c (Conclusion): {D(n()*)}
test(verbose=False): Method used to test the example
```

## e63_modified
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1659)


```
description:
    Example 63, p176
    
v (Views): (
   ∀x ∃y {S(j()*)D(n()*),~D(j()*)T(j())D(f(y,x)*)},
   ∃a {D(a*)}
)
c (Conclusion): ∀x ∃y {D(n()*),D(f(y,x)*)}
test(verbose=False): Method used to test the example
```

## e64i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1671)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1703)


```
v (Views): (
   ∀x {90.0=* S(x*)T(x*)P(x),S(x*)~T(x)P(x)}^{S(x*)P(x)},
   ∀x {1.0=* T(x)~S(x*)P(x),~T(x)~S(x*)P(x)}^{~S(x*)P(x)},
   ∀x {1.0=* S(x*)P(x),~S(x)P(x)}^{P(x)},
   {P(Smith())T(Smith()*)},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*)}
test(verbose=False): Method used to test the example
```

## e65
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1723)


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
   ∀x {50.0=* C(x)T(x)P(x*),~T(x)C(x)P(x*)}^{C(x)P(x*)},
   ∀x {3.0=* T(x)~C(x)P(x*),~T(x)~C(x)P(x*)}^{~C(x)P(x*)},
   ∃a {P(a*)T(a)},
   ∃a {C(a)}
)
c (Conclusion): ∃a {15.0=* C(a),0}
test(verbose=False): Method used to test the example
```

## e66i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1757)


```
description:
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ?
    
v (Views): (
   {1.0=* D()T(),1.0=* ~D()T(),98.0=* ~D()},
   {D()T()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e66ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1785)


```
v (Views): (
   {1.0=* D()T(),1.0=* ~D()T(),98.0=* ~D()},
   {T()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e67
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1802)


```
description:
    Example 67, p191, p220

    Results of a recent survey of seventy-four chief executive officers indicate there
    may be a link between childhood pet ownership and future career success. Fully 94%
    of the CEOs, all of them employed within Fortune 500 companies, had possessed a dog,
    a cat, or both, as youngsters.
    
v (Views): (
   {94.0=* HadPet()IsCEO(),~IsCEO()},
   {HadPet()},
   {IsCEO()}
)
c (Conclusion): {94.0=* IsCEO(),0}
test(verbose=False): Method used to test the example
```

## e69_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1831)


```
description:
    Example 69, p192, p218

    The suspect's DNA matches the crime sample.

    If the suspect is not guilty, then the probability of such a DNA match is 1 in
    a million

    Is the suspect likely to be guilty?
    
v (Views): (
   {Match(Suspect())},
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),~Guilty(Suspect())~Match(Suspect())}^{~Guilty(Suspect())}
)
c (Conclusion): {0.000001=* ~Guilty(Suspect())Match(Suspect()),Match(Suspect())Guilty(Suspect())}
test(verbose=False): Method used to test the example
```

## e69_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1865)


```
v (Views): (
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),Match(Suspect())Guilty(Suspect())},
   {999999.999999=* 0}^{Match(Suspect())Guilty(Suspect())},
   {Guilty(Suspect())}
)
c (Conclusion): (
   {0.000001=* ~Guilty(Suspect())Match(Suspect()),999999.999999=* Match(Suspect())Guilty(Suspect())},
   {999999.999999=* Guilty(Suspect()),0}
)
test(verbose=False): Method used to test the example
```

## e70
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1892)


```
description:
    Example 70, p194, p221

    P1 Pat has either the disease or a benign condition
    P2 If she has the disease, then she will have a certain symptom.
    P3 In fact, she has the symptom
    
v (Views): (
   {Disease(),Benign()},
   {Disease()Symptom()}^{Disease()},
   {Symptom()}
)
c (Conclusion): {Disease()Symptom()}
test(verbose=False): Method used to test the example
```

## e71
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1917)


```
description:
    Examples 71 & 78, p209, p212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    
v (Views): (
   {B(yellow())~B(brown()),~B(yellow())B(brown())},
   {50.0=* 0}^{B(yellow())~B(brown())},
   {50.0=* 0}^{~B(yellow())B(brown())},
   {B(yellow())~B(brown())}
)
c (Conclusion): (
   {50.0=* B(yellow())~B(brown()),50.0=* ~B(yellow())B(brown())},
   {50.0=* B(yellow())~B(brown()),0}
)
test(verbose=False): Method used to test the example
```

## e72
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1954)


```
description:
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    
v (Views): (
   {B(g())~B(r())B(b()),~B(g())B(r()),B(r())~B(b())},
   {33.333333=* 0}^{B(g())~B(r())B(b())},
   {33.333333=* 0}^{~B(g())B(r())},
   {33.333333=* 0}^{B(r())~B(b())},
   {B(r())B(b())}
)
c (Conclusion): (
   {33.333333=* B(g())~B(r())B(b()),33.333333=* ~B(g())B(r()),33.333333=* B(r())~B(b())},
   {33.333333=* B(r())B(b()),0}
)
test(verbose=False): Method used to test the example
```

## e74
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1998)


```
description:
    Example 74, p197, p231

    (includes two background commitments)
    
v (Views): (
   {D(j())H(j()),H(j()),P(j())},
   {E(j()*)},
   ∀x {0.85=* D(x)E(x*),0.15=* ~D(x)E(x*)}^{E(x*)},
   ∀x {0.1=* E(x*)H(x),0.9=* ~H(x)E(x*)}^{E(x*)}
)
c (Conclusion): (
   {0.085=* E(j()*)H(j())D(j()),0.765=* ~H(j())E(j()*)D(j()),0.015=* ~D(j())E(j()*)H(j()),0.135=* ~D(j())E(j()*)~H(j())},
   {D(j())H(j())}
)
test(verbose=False): Method used to test the example
```

## e76
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2034)


```
description:
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    
v (Views): (
   {Guitar(j())Gun(i())Fired(i()*)Outoftune(j()),Attic(a())},
   ∀x {Trigger(x)Gun(x)Fired(x*),0}^{Gun(x)Fired(x*)},
   {Trigger(i())}
)
c (Conclusion): {Fired(i()*)Guitar(j())Trigger(i())Gun(i())Outoftune(j())}
test(verbose=False): Method used to test the example
```

## e81i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2076)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Yellow()),0}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2086)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card and a brown card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2096)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is neither a yellow card nor a brown card
    
v (Views): (
   {~Box(Brown())Box(Yellow()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2119)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card.
    
v (Views): (
   {Box(Brown())Box(Yellow())}^{Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Yellow()),0}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2129)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and a brown card.
    
v (Views): (
   {Box(Brown())Box(Yellow())}^{Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Brown())Box(Yellow()),0}
prob (Probability): {Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2139)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and there is not a brown card.
    
v (Views): (
   {Box(Brown())Box(Yellow())}^{Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2149)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is neither a yellow card nor a brown card.
    
v (Views): (
   {Box(Brown())Box(Yellow())}^{Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e83i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2178)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a red marble and blue in marble in the box.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Green())Box(Blue()),33.333333333333336=* ~Box(Green())~Box(Blue())~Box(Red())}
)
c (Conclusion): {0}
prob (Probability): {Box(Blue())Box(Red())}
test(verbose=False): Method used to test the example
```

## e83ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2188)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a green marble and there is a blue marble.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Green())Box(Blue()),33.333333333333336=* ~Box(Green())~Box(Blue())~Box(Red())}
)
c (Conclusion): {33.333333333333336=* Box(Green())Box(Blue()),0}
prob (Probability): {Box(Green())Box(Blue())}
test(verbose=False): Method used to test the example
```

## e84i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2201)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(Mauve())Box(White())Box(Grey()),~Box(White())Box(Mauve())Box(Grey())}
)
c (Conclusion): {50.0=* Box(Mauve())Box(Grey()),0}
prob (Probability): {Box(Mauve())Box(Grey())}
test(verbose=False): Method used to test the example
```

## e84ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2223)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(Mauve())~Box(White())Box(Grey()),~Box(Mauve())Box(White())~Box(Grey()),~Box(White())Box(Mauve())~Box(Grey())}
)
c (Conclusion): {0}
prob (Probability): {Box(Mauve())Box(Grey())}
test(verbose=False): Method used to test the example
```

## e85
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2246)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2269)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2291)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2321)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2339)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2375)


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
   {MedTime(ParentA())MedRapp(ParentA())LowTime(ParentB())HighRapp(ParentB())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{HighRapp(x)Custody(x*)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}
)
test(verbose=False): Method used to test the example
```

## e92_deny
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2386)


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
   {MedTime(ParentA())MedRapp(ParentA())LowTime(ParentB())HighRapp(ParentB())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{HighRapp(x)Custody(x*)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}
)
test(verbose=False): Method used to test the example
```

## e93_grp1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2396)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2438)


```
v (Views): (
   ∀x ∃a ∀y {P(x,a)Q(a,y)},
   ∃b ∀z {P(b,z)}
)
c (Conclusion): ∃b ∀x ∀z ∃a ∀y {P(b,z)P(x,a)Q(a,y)}
test(verbose=False): Method used to test the example
```

## new_e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2449)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x ∃b {R(b)Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2467)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_merge
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2471)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_suppose
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2475)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_uni_prod
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2479)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_query
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2488)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {R(a)Q(y*)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_which
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2492)


```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {R(a)Q(y*)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## new_e5
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2496)


```
v (Views): (
   ∀y ∀x ∃b ∃a ∀z ∃c {P(a*)Q(x*)P(y)P(c)P(b)P(z)},
   ∃d ∃f ∃e {P(d*)Q(e*)Q(f*)}
)
c (Conclusion): ∃d ∃f ∃e {P(d*)Q(e*)Q(f*)}
test(verbose=False): Method used to test the example
```

## new_e6_leibniz
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2504)


```
v (Views): (
   ∃a ∃b {~P(f(b),a)==(a,b)P(f(a),a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e7_aristotle
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2509)


```
v (Views): (
   ∃a {~==(a,a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2514)


```
v (Views): (
   {t()=+ A()},
   {u()=* A()}
)
c (Conclusion): {u()=* t()=+ A()}
test(verbose=False): Method used to test the example
```

## new_e9
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2519)


```
v (Views): (
   ∀x {P(x*)},
   {P(j()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## new_e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2524)


```
v (Views): (
   ∀x {f(x)=* A(x*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2529)


```
v (Views): (
   {f(12.0)=* A(12.0*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e12
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2534)


```
v (Views): (
   {A()},
   {}
)
c (Conclusion): {A()}
test(verbose=False): Method used to test the example
```

## new_e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2539)


```
v (Views): (
   {f(12.0)=* A(12.0*),B()}
)
c (Conclusion): {}
prob (Probability): ∃e {A(e*)}
test(verbose=False): Method used to test the example
```

## new_e14
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2545)


```
v (Views): (
   ∀x ∃y {A(f(x*))B(g(x*,y))},
   {A(f(j()*))}
)
c (Conclusion): ∃y {B(g(j()*,y))A(f(j()*))}
test(verbose=False): Method used to test the example
```

## new_e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2550)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}
)
c (Conclusion): ∃k {Defeats(k,Clark())==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2558)


```
v (Views): (
   ∃x ∃k {Defeats(k,x)==(Clark(),x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {Defeats(k,Clark())==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2563)


```
v (Views): (
   ∃x ∃k {do(Defeats(k,x))==(Clark(),x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {do(Defeats(k,Clark()))==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e18
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2568)


```
v (Views): (
   {m()=* A()},
   {n()=* B()}
)
c (Conclusion): {m()**n()=* B()A()}
test(verbose=False): Method used to test the example
```

## new_e19_first_atom_do_atom
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2573)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {do(A())}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e20_nested_issue_in_pred
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2578)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark(),f(Superman()*))}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e21_supp_is_something
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2586)


```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}^{}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e22_restrict_dep_rel_is_not_other
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2594)


```
v (Views): (
   ∃x ∃k {do(Defeats(k,x))==(Clark(),x)},
   ∃y {==(Clark()*,y)}
)
c (Conclusion): ∃x ∃k {do(Defeats(k,x))==(Clark(),x)}
test(verbose=False): Method used to test the example
```

## AnswerPotential
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2599)


```
v (Views): (
   {1.0=* 2.0=+ B()A(),0.4=* C()B(),C()A()},
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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2641)


```
v (Views): (
   ∀x ∃a {E(x,a)P(x),~P(x*)},
   {P(j()*)}
)
c (Conclusion): ∃a {~P(j()*),E(j(),a)P(j())}
test(verbose=False): Method used to test the example
```

## QueryTest
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2646)


```
description:
    From page 173
    
v (Views): (
   ∀x {S(j()*)T(x,m())S(m()*),S(j()*)T(x,j())S(m()*)},
   ∀x ∃a {T(x,a)S(a*)}
)
c (Conclusion): ∀x ∃a {T(x,a)S(a*)}
test(verbose=False): Method used to test the example
```

## QueryTest2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2658)


```
description:
    From page 173
    
v (Views): (
   ∀x {S(j()*)T(x,m())S(m()*),S(j()*)T(x,j())S(m()*)},
   ∃a ∀x {T(x,a)S(a*)}
)
c (Conclusion): ∀x ∃a {T(x,a)S(a*)}
test(verbose=False): Method used to test the example
```