# Case Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L433)


```
description:
    Example 1, p61:

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else
    Mark is standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire.
    C Jane is looking at the TV.
    
v[0]: {KneelingByTheFire(Jane())LookingAtTV(Jane()),PeeringIntoTheGarden(Mark())StandingAtTheWindow(Mark())}
v[1]: {KneelingByTheFire(Jane())}

c (Conclusion): {LookingAtTV(Jane())}
test(verbose=False): Method used to test the example
```

## e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L452)


```
description:
    Example 2, p62:

    P1 There is at least an ace and a queen, or else at least a king and a ten.
    P2 There is a king.
    C There is a ten.
    
v[0]: {A()Q(),K()T()}
v[1]: {K()}

c (Conclusion): {T()}
test(verbose=False): Method used to test the example
```

## e3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L468)


```
description:
    Example 3, p63:

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v[0]: {Ace()King(),Jack()Queen()}
v[1]: {~Ace()}

c (Conclusion): {Jack()Queen()}
test(verbose=False): Method used to test the example
```

## e5ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L495)


```
description:
    Example 5, p72, part ii
    
v[0]: {p1()q1(),r1()s1()}
v[1]: {p2()q2(),r2()s2()}

c (Conclusion): {p1()p2()q1()q2(),p1()q1()r2()s2(),p2()q2()r1()s1(),r1()r2()s1()s2()}
test(verbose=False): Method used to test the example
```

## e5iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L509)


```
description:
    Example 5, p72, part iii
    
v[0]: {p1()q1(),r1()s1()}
v[1]: {}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e5iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L521)


```
description:
    Example 5, p72, part iv
    
v[0]: {p1()q1(),r1()s1()}
v[1]: {0}

c (Conclusion): {p1()q1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e5v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L533)


```
description:
    Example 5, p72, part v
    
v[0]: {0}
v[1]: {p1()q1(),r1()s1()}

c (Conclusion): {p1()q1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L545)


```
description:
    Example 6, p72

    There is an Ace and a King = (There is an Ace) x (There is a king)
    
v[0]: {a()}
v[1]: {k()}

c (Conclusion): {a()k()}
test(verbose=False): Method used to test the example
```

## e7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L556)


```
description:
    Example 7, p73

    There is an Ace or there is a king = (There is an Ace) + (There is a king)
    
v[0]: {a()}
v[1]: {k()}

c (Conclusion): {a(),k()}
test(verbose=False): Method used to test the example
```

## e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L567)


```
description:
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    
v[0]: {a()q(),k()t()}
v[1]: {k()}

c (Conclusion): {t()}
test(verbose=False): Method used to test the example
```

## e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L581)


```
description:
    Example 10, p76

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a king (reversed premises blocking illusory inference).
    
v[0]: {K()}
v[1]: {A()Q(),K()T()}

c (Conclusion): {K()}
test(verbose=False): Method used to test the example
```

## e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L597)


```
description:
    Example 11, p77

    P1 Either John smokes or Mary smokes.
    P2 Supposing John smokes, John drinks.
    P3 Supposing Mary smokes, Mary eats.
    C Either John smokes and drinks or Mary smokes and drinks.
    
v[0]: {Smokes(j()),Smokes(m())}
v[1]: {Drinks(j())}^{Smokes(j())}
v[2]: {Eats(m())}^{Smokes(m())}

c (Conclusion): {Drinks(j())Smokes(j()),Eats(m())Smokes(m())}
test(verbose=False): Method used to test the example
```

## e12i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L615)


```
description:
    Example 12i, p78

    ItisnotthecasethatPorQorR
    
v[0]: {P(),Q(),R()}

c (Conclusion): {~P()~Q()~R()}
test(verbose=False): Method used to test the example
```

## e12ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L626)


```
description:
    Example 12ii, p78

    ItisnotthecasethatPandQandR
    
v[0]: {P()Q()R()}

c (Conclusion): {~P(),~Q(),~R()}
test(verbose=False): Method used to test the example
```

## e12iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L637)


```
description:
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    
v[0]: {P()Q(),R()}^{S()}

c (Conclusion): {S()~P()~R(),S()~Q()~R()}
test(verbose=False): Method used to test the example
```

## e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L648)


```
description:
    Example 13, p80

    P1 There is an ace and a king or a queen and a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v[0]: {IsAce()IsKing(),IsJack()IsQueen()}
v[1]: {~IsAce()}

c (Conclusion): {IsJack()IsQueen()}
test(verbose=False): Method used to test the example
```

## e14_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L664)


```
description:
    Example 14-1, p81

    Factor examples
    
v[0]: {P()Q(),P()R()}
v[1]: {P()}

c (Conclusion): {Q(),R()}
test(verbose=False): Method used to test the example
```

## e14_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L678)


```
description:
    Example 14-2, p81

    Factor examples
    
v[0]: {P()Q()S(),P()R(),P()R()S()}
v[1]: {P()}^{S()}

c (Conclusion): {P()R(),Q()S(),R()S()}
test(verbose=False): Method used to test the example
```

## e14_3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L692)


```
description:
    Example 14-3, p81

    Factor examples
    
v[0]: {P()R(),P()S(),Q()R(),Q()S()}
v[1]: {P(),Q()}

c (Conclusion): {R(),S()}
test(verbose=False): Method used to test the example
```

## e14_6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L706)


```
description:
    Example 14-6, p81

    Factor examples
    
v[0]: {P()R(),Q()S()}
v[1]: {P(),Q(),T()}

c (Conclusion): {P()R(),Q()S()}
test(verbose=False): Method used to test the example
```

## e14_7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L720)


```
description:
    Example 14-7, p81

    Factor examples
    
v[0]: {P(),P()R(),Q()S()}
v[1]: {P(),Q()}

c (Conclusion): {0,R(),S()}
test(verbose=False): Method used to test the example
```

## e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L734)


```
description:
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    
v[0]: {Ace(),Ace()Jack()Queen(),Eight()Four()Ten()}
v[1]: {Ace()Eight()Jack()Ten()}
v[2]: {~Queen()}

c (Conclusion): {Four()}
test(verbose=False): Method used to test the example
```

## e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L752)


```
description:
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    
v[0]: {Ace(),Eight()Four()Ten(),Jack()King()Queen()}
v[1]: {~Four()}
v[2]: {~Ace()}

c (Conclusion): {Jack()King()Queen()}
test(verbose=False): Method used to test the example
```

## e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L769)


```
description:
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    
v[0]: {Ace()~King(),King()~Ace()}
v[1]: {King()}

c (Conclusion): {~Ace()}
test(verbose=False): Method used to test the example
```

## e19
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L785)


```
description:
    Example 19, p84

    Suppose test
    
v[0]: {0}
v[1]: {~N()}

c (Conclusion): {~N()}^{~N()}
test(verbose=False): Method used to test the example
```

## e20
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L799)


```
description:
    Example 20, p85

    P1 Either there is a king in the hand or a queen in the hand.
    P2 On the supposition that there is a king, Mary wins.
    P3 On the supposition that there is a queen, Bill wins.
    C Either Mary wins or Bill wins.
    
v[0]: {King(),Queen()}
v[1]: {Win(mary())}^{King()}
v[2]: {Win(bill())}^{Queen()}

c (Conclusion): {Win(bill()),Win(mary())}
test(verbose=False): Method used to test the example
```

## e21
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L817)


```
description:
    Example 21, p86

    Any view Δ^{0} = [Δ^{0}]ᶰ can be derived from the absurd view
    
v[0]: {r1()s1()}

c (Conclusion): {~r1(),~s1()}
test(verbose=False): Method used to test the example
```

## e22
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L835)


```
description:
    Example 22, p87

    It is not the case that A and B and C
    
v[0]: {a()b()c()}
v[1]: {a()}
v[2]: {b()}
v[3]: {c()}

v[0]: {~a(),~b(),~c()}
v[1]: {a()b()~c(),a()c()~b(),a()~b()~c(),b()c()~a(),b()~a()~c(),c()~a()~b(),~a()~b()~c()}

test(verbose=False): Method used to test the example
```

## e23_with_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L874)


```
description:
    Example 23, p88, with inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v[0]: {K()L(),P()S()}
v[1]: {K()}

v[0]: {K()L(),K()P()S(),P()S()~K()}
v[1]: {K()L(),K()P()S()}

test(verbose=False): Method used to test the example
```

## e23_without_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L910)


```
description:
    Example 23, p88, without inquire step

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else Mark is
    standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire

    C Jane is looking at the TV
    
v[0]: {K()L(),P()S()}
v[1]: {K()}

v[0]: {K()L(),P()S()}
v[1]: {K()L()}

test(verbose=False): Method used to test the example
```

## e24
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L942)


```
description:
    Example 24, p89

    P1 There is an ace
    C There is an ace or a queen
    
v[0]: {a()}
v[1]: {q()}
v[2]: {~q()}
v[3]: {a(),q()}

v[0]: {a()q(),a()~q()}
v[1]: {a(),q()}

test(verbose=False): Method used to test the example
```

## e25i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L975)


```
description:
    Example 25i, p89
    
v[0]: {p()q(),p()r()}
v[1]: {p()}

c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L984)


```
description:
    Example 25ii, p89
    
v[0]: {p()q(),p()r()}
v[1]: {q()}

c (Conclusion): {0,q()}
test(verbose=False): Method used to test the example
```

## e25iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L993)


```
description:
    Example 25iii, p89
    
v[0]: {p()q(),p()r(),s(),t()}
v[1]: {p(),s()}

c (Conclusion): {0,p(),s()}
test(verbose=False): Method used to test the example
```

## e25iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1005)


```
description:
    Example 25iv, p89
    
v[0]: {p()q(),p()r(),s(),t()}
v[1]: {p(),s(),t()}

c (Conclusion): {p(),s(),t()}
test(verbose=False): Method used to test the example
```

## e25v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1017)


```
description:
    Example 25v, p89
    
v[0]: {p()q()s(),p()r()s()}
v[1]: {p()}^{s()}

c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25vi
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1029)


```
description:
    Example 25vi, p89
    
v[0]: {p()q()s(),p()r()s()}
v[1]: {p()}^{t()}

c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e26
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1041)


```
description:
    Example 26, p90

    P1 Either John plays and wins, or Mary plays, or Bill plays
    C Supposing John plays, John wins
    
v[0]: {Play(B()),Play(J())Win(J()),Play(M())}
v[1]: {Play(J())}
v[2]: {Win(J())}^{Play(J())}

v[0]: {Play(J())Win(J())}^{Play(J())}
v[1]: {Win(J())}^{Play(J())}

test(verbose=False): Method used to test the example
```

## e26_does_it_follow
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1074)


```
v[0]: {Play(B()),Play(J())Win(J()),Play(M())}
v[1]: {Play(J())}
v[2]: {Win(J())}^{Play(J())}

v[0]: {Play(J())Win(J())}^{Play(J())}
v[1]: {Win(J())}^{Play(J())}

test(verbose=False): Method used to test the example
```

## e28
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1085)


```
description:
    Example 28, p96

    P1 Is there a tiger?
    P2 Supposing there is a tiger, there is orange fur.
    P3 There is orange fur.
    C There is a tiger.
    
v[0]: {Tiger(),~Tiger()}
v[1]: {Orange()Tiger()}^{Tiger()}
v[2]: {Orange()}

c (Conclusion): {Orange()Tiger()}
test(verbose=False): Method used to test the example
```

## e32_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1103)


```
description:
    Example 32-1, p107

    P1 If P then Q.
    P2 P
    C Q
    
v[0]: {P()Q()}^{P()}
v[1]: {P()}

c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e32_2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1119)


```
description:
    Example 32-2, p107

    P1 P
    P2 If P then Q.
    C Q
    
v[0]: {P()}
v[1]: {P()Q()}^{P()}

c (Conclusion): {Q()}
test(verbose=False): Method used to test the example
```

## e33
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1135)


```
description:
    Example 33, p108

    P1 If the card is red then the number is even.
    P2 The number is even.
    C The card is red
    
v[0]: {E()R()}^{R()}
v[1]: {E()}

c (Conclusion): {R()}
test(verbose=False): Method used to test the example
```

## e40i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1151)


```
description:
    Example 40, p119

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    
v[0]: {CircleB()~SquareB()~TriangleB(),SquareB()~CircleB()~TriangleB(),TriangleB()~CircleB()~SquareB()}
v[1]: {CircleT()SquareB()}^{CircleT()}
v[2]: {TriangleB()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e40ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1184)


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
    
v[0]: {CircleB()~SquareB()~TriangleB(),SquareB()~CircleB()~TriangleB(),TriangleB()~CircleB()~SquareB()}
v[1]: {TriangleB()}
v[2]: {CircleT()SquareB()}^{CircleT()}

c (Conclusion): {TriangleB()~CircleB()~CircleT()~SquareB()}
test(verbose=False): Method used to test the example
```

## e41
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1221)


```
description:
    Example 41, p121

    P1 P only if Q.
    P2 Not Q.
    C Not P.
    
v[0]: {~P()~Q()}^{~Q()}
v[1]: {~Q()}

c (Conclusion): {~P()}
test(verbose=False): Method used to test the example
```

## e42
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1237)


```
description:
    Example 42, p122

    P1 There is a circle at the top of the card only if there is a square
    at the bottom.
    P2 There is not a square at the bottom
    C There is not a circle at the top
    
v[0]: {~CircleT()~SquareB()}^{~SquareB()}
v[1]: {~SquareB()}

c (Conclusion): {~CircleT()}
test(verbose=False): Method used to test the example
```

## e44_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1257)


```
description:
    Example 44-1, p123

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    
v[0]: {Elegant(c())Saleable(c()),~Elegant(c())~Saleable(c())}
v[1]: {Elegant(c())Stable(c()),~Elegant(c())~Stable(c())}
v[2]: {Elegant(c())Saleable(c()),Saleable(c()),Stable(c())}

c (Conclusion): {Elegant(c())Saleable(c())Stable(c())}
test(verbose=False): Method used to test the example
```

## e45
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1275)


```
description:
    Example 45, p125

    It is possible that Steven is in Madrid and it is possible that Emma is in
    Berlin.
    Therefore it is possible that Steven is in Madrid and that Emma is in Berlin.
    
v[0]: {0,M()}
v[1]: {0,B()}
v[2]: {0,B()M()}

v[0]: {0,B(),B()M(),M()}
v[1]: {0,B()M()}

test(verbose=False): Method used to test the example
```

## e46i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1302)


```
description:
    Example 46, p126

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    
v[0]: {P()V()}^{P()}
v[1]: {M()~P(),P()~M()}
v[2]: {0,M()V()}

v[0]: {M()~P(),P()V()~M()}
v[1]: {0}

test(verbose=False): Method used to test the example
```

## e46ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1339)


```
description:
    Example 46, part ii, p126

    If we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
    
v[0]: {M()R()V(),M()S()V(),T()}
v[1]: {0,M()V()}

c (Conclusion): {0,M()V()}
test(verbose=False): Method used to test the example
```

## e47
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1353)


```
description:
    Example 47, p129

    P1: Some thermotogum stains gram-negative
    P2: Maritima is a thermotogum

    C: Maritima stains gram negative
    
v[0]: ∃x {StainsGramNegative(x)Thermotogum(x*)}
v[1]: {Thermotogum(Maritima()*)}

c (Conclusion): {StainsGramNegative(Maritima())}
test(verbose=False): Method used to test the example
```

## e48
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1370)


```
description:
    Example 48, p130

    P1 Some dictyoglomus is thermophobic.
    P2 Turgidum is not a dictyoglomus.
    C Truth
    
v[0]: ∃x {D(x*)T(x)}
v[1]: {~D(Turgidum()*)}

c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e49
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1386)


```
description:
    Example 49, p130

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    
v[0]: ∃x ∃y {Ace(Mary())King(x),Jack(y)Queen(John())}
v[1]: {King(Sally())}

c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e50_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1403)


```
description:
    Example 50, part1, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v[0]: {L(j(),s())L(s(),g())}
v[1]: {M(j()*)~M(g()*)}
v[2]: {}
v[3]: ∃a ∃b {L(a,b)M(a*)~M(b*)}

v[0]: {L(j(),s())L(s(),g())M(j()*)~M(g()*)}
v[1]: {0}

test(verbose=False): Method used to test the example
```

## e50_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1440)


```
description:
    Example 50, part2, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v[0]: {L(j(),s())L(s(),g())}
v[1]: {M(j())~M(g())}
v[2]: {M(s())}
v[3]: ∃a ∃b {L(a,b)M(a*)~M(b*)}

c (Conclusion): ∃a ∃b {L(a,b)M(a*)~M(b*)}
g1 (Another View): {L(j(),s())L(s(),g())M(j())M(s())~M(g()),L(j(),s())L(s(),g())M(j())~M(g())~M(s())}
g2 (Another View): {L(j(),s())L(s(),g())M(j()*)M(s())~M(g()*),L(j(),s())L(s(),g())M(j()*)~M(g()*)~M(s()*)}
test(verbose=False): Method used to test the example
```

## e50_part2_arbs
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1485)


```
description:
    Duplicate of e50, uses arb objects, some changes
    
v[0]: ∃g ∃j ∃s {L(j,s)L(s,g)M(j)~M(g)}
v[1]: ∃s {M(s)}
v[2]: ∃a ∃b {L(a,b)M(a*)~M(b*)}

c (Conclusion): ∃a ∃b {L(a,b)M(a*)~M(b*)}
g1 (Another View): ∃g ∃j ∃s {L(j,s)L(s,g)M(j)M(s)~M(g),L(j,s)L(s,g)M(j)~M(g)~M(s)}
g2 (Another View): ∃g ∃j ∃s {L(j,s)L(s,g)M(j*)M(s)~M(g*),L(j,s)L(s,g)M(j*)~M(g*)~M(s*)}
test(verbose=False): Method used to test the example
```

## e51
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1516)


```
description:
    Example 51, p131

    P1: Every archaeon has a nucleus
    P2: Halobacterium is an archaeon

    C: Halobacterium is an archaeon and has a nucleus
    
v[0]: ∀x {HasNucleus(x)IsArchaeon(x*)}^{IsArchaeon(x*)}
v[1]: {IsArchaeon(Halobacterium()*)}

c (Conclusion): {HasNucleus(Halobacterium())IsArchaeon(Halobacterium()*)}
test(verbose=False): Method used to test the example
```

## e52
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1533)


```
description:
    Example 52, p132

    P1 All Fs G.
    P2 John Gs.
    C John Fs and Gs.
    
v[0]: ∀x {F(x)G(x*)}^{F(x)}
v[1]: {G(John()*)}

c (Conclusion): {F(John())G(John()*)}
test(verbose=False): Method used to test the example
```

## e53
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1549)


```
description:
    Example 53, p132 & p175

    P All A are B.
    C All B are A.
    
v[0]: ∀x {A(x)B(x)}^{A(x)}
v[1]: ∀x {B(x)}
v[2]: ∀x {A(x)B(x)}^{B(x)}

c (Conclusion): ∀x {A(x)B(x)}^{B(x)}
test(verbose=False): Method used to test the example
```

## e53_does_it_follow
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1576)


```
v[0]: ∀x {A(x)B(x)}^{A(x)}
v[1]: ∀x {B(x)}
v[2]: ∀x {A(x)B(x)}^{B(x)}

c (Conclusion): ∀x {A(x)B(x)}^{B(x)}
test(verbose=False): Method used to test the example
```

## e54
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1587)


```
description:
    Example 54, p133

    P1 Sharks attack bathers.
    P2 Whitey is a shark.
    C Whitey attacks bathers.
    
v[0]: ∀x {0,Attack(x)Shark(x*)}^{Shark(x*)}
v[1]: {Shark(Whitey()*)}

c (Conclusion): {Attack(Whitey())Shark(Whitey()*)}
test(verbose=False): Method used to test the example
```

## e56_default_inference
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1620)


```
description:
    Example 56, p134

    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    
v[0]: ∀x ∃y {Professor(x)Student(y*)Teaches(x,y)}^{Professor(x)}
v[1]: ∀z ∃w {Book(w)Reads(z,w)Student(z*)}^{Student(z*)}

c (Conclusion): ∃b ∃y {0,Book(b)Reads(y,b)}
test(verbose=False): Method used to test the example
```

## e56_basic_step
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1637)


```
v[0]: ∀x ∃y {Professor(x)Student(y*)Teaches(x,y)}^{Professor(x)}
v[1]: ∀z ∃w {Book(w)Reads(z,w)Student(z*)}^{Student(z*)}

c (Conclusion): ∀a ∃b ∃c {Book(c)Professor(a)Reads(b,c)Student(b*)Teaches(a,b),~Professor(a)}
test(verbose=False): Method used to test the example
```

## e57
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1643)


```
description:
    Example 57, p134

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    
v[0]: ∀x {A(x)B(x*)}^{B(x*)}
v[1]: ∃x {B(x*)C(x)}

c (Conclusion): ∃y {A(y)B(y*)C(y)}
test(verbose=False): Method used to test the example
```

## e58_reversed
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1659)


```
description:
    Example 58 reversed, based on p135

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    
v[0]: ∀y {B(y*)C(y)}^{C(y)}
v[1]: ∃x {A(x)B(x*)}

c (Conclusion): ∃y {A(y)B(y*)C(y)}
test(verbose=False): Method used to test the example
```

## e61
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1675)


```
description:
    Example 61, p166
    P1 All dogs bite some man
    P2 John is a man

    C All dogs bite John
    
v[0]: ∀x ∃a {B(x,a)D(x)M(a*),~D(x)}
v[1]: {M(j()*)}

c (Conclusion): ∀x ∃a {B(x,a)D(x)M(a*)M(j()*),M(j()*)~D(x)}
test(verbose=False): Method used to test the example
```

## e62
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1688)


```
description:
    Example 62, p176
    
v[0]: {D(b())~S(n()*),D(m())S(j()*)T(n()),L(n(),m())S(m()*)}
v[1]: ∃a {S(a*)}

c (Conclusion): {0,S(j()*),S(m()*)}
test(verbose=False): Method used to test the example
```

## e63
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1700)


```
description:
    Example 63, p176
    
v[0]: {D(n()*)S(j()*),D(n()*)T(j())~D(j()*)}
v[1]: ∃a {D(a*)}

c (Conclusion): {D(n()*)}
test(verbose=False): Method used to test the example
```

## e63_modified
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1712)


```
description:
    Example 63, p176
    
v[0]: ∀x ∃y {D(f(y,x)*)T(j())~D(j()*),D(n()*)S(j()*)}
v[1]: ∃a {D(a*)}

c (Conclusion): ∀x ∃y {D(f(y,x)*),D(n()*)}
test(verbose=False): Method used to test the example
```

## e64i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1724)


```
description:
    Example 64, p189, p223

    A device has been invented for screening a population for a disease known as psylicrapitis.
    The device is a very good one, but not perfect. If someone is a sufferer, there is a 90% chance
    that he will recorded positively. If he is not a sufferer, there is still a 1% chance that he will
    be recorded positively.

    Roughly 1% of the population has the disease. Mr Smith has been tested, and the result is positive.

    What is the chance that he is in fact a sufferer?
    
v[0]: ∀x {90.0=* S(x*)T(x*),S(x*)~T(x)}^{S(x*)}
v[1]: ∀x {1.0=* T(x)~S(x*),~S(x*)~T(x)}^{~S(x*)}
v[2]: {T(Smith()*)}
v[3]: {S(Smith())}

c (Conclusion): {0,90.0=* S(Smith()*)}
test(verbose=False): Method used to test the example
```

## e64ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1756)


```
v[0]: ∀x {90.0=* P(x)S(x*)T(x*),P(x)S(x*)~T(x)}^{P(x)S(x*)}
v[1]: ∀x {1.0=* P(x)T(x)~S(x*),P(x)~S(x*)~T(x)}^{P(x)~S(x*)}
v[2]: ∀x {1.0=* P(x)S(x*),P(x)~S(x)}^{P(x)}
v[3]: {P(Smith())T(Smith()*)}
v[4]: {S(Smith())}

c (Conclusion): {90.0=* S(Smith()*)}
test(verbose=False): Method used to test the example
```

## e65
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1776)


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
    
v[0]: ∀x {0.3=* C(x)P(x*),P(x*)~C(x)}^{P(x*)}
v[1]: ∀x {50.0=* C(x)P(x*)T(x),C(x)P(x*)~T(x)}^{C(x)P(x*)}
v[2]: ∀x {3.0=* P(x*)T(x)~C(x),P(x*)~C(x)~T(x)}^{P(x*)~C(x)}
v[3]: ∃a {P(a*)T(a)}
v[4]: ∃a {C(a)}

c (Conclusion): ∃a {0,15.0=* C(a)}
test(verbose=False): Method used to test the example
```

## e66i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1810)


```
description:
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ?
    
v[0]: {1.0=* D()T(),1.0=* T()~D(),98.0=* ~D()}
v[1]: {D()T()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e66ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1838)


```
v[0]: {1.0=* D()T(),1.0=* T()~D(),98.0=* ~D()}
v[1]: {T()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e67
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1855)


```
description:
    Example 67, p191, p220

    Results of a recent survey of seventy-four chief executive officers indicate there
    may be a link between childhood pet ownership and future career success. Fully 94%
    of the CEOs, all of them employed within Fortune 500 companies, had possessed a dog,
    a cat, or both, as youngsters.
    
v[0]: {94.0=* HadPet()IsCEO(),~IsCEO()}
v[1]: {HadPet()}
v[2]: {IsCEO()}

c (Conclusion): {0,94.0=* IsCEO()}
test(verbose=False): Method used to test the example
```

## e69_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1884)


```
description:
    Example 69, p192, p218

    The suspect's DNA matches the crime sample.

    If the suspect is not guilty, then the probability of such a DNA match is 1 in
    a million

    Is the suspect likely to be guilty?
    
v[0]: {Match(Suspect())}
v[1]: {0.000001=* Match(Suspect())~Guilty(Suspect()),~Guilty(Suspect())~Match(Suspect())}^{~Guilty(Suspect())}

c (Conclusion): {Guilty(Suspect())Match(Suspect()),0.000001=* Match(Suspect())~Guilty(Suspect())}
test(verbose=False): Method used to test the example
```

## e69_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1918)


```
v[0]: {Guilty(Suspect())Match(Suspect()),0.000001=* Match(Suspect())~Guilty(Suspect())}
v[1]: {999999.999999=* 0}^{Guilty(Suspect())Match(Suspect())}
v[2]: {Guilty(Suspect())}

v[0]: {999999.999999=* Guilty(Suspect())Match(Suspect()),0.000001=* Match(Suspect())~Guilty(Suspect())}
v[1]: {0,999999.999999=* Guilty(Suspect())}

test(verbose=False): Method used to test the example
```

## e70
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1945)


```
description:
    Example 70, p194, p221

    P1 Pat has either the disease or a benign condition
    P2 If she has the disease, then she will have a certain symptom.
    P3 In fact, she has the symptom
    
v[0]: {Benign(),Disease()}
v[1]: {Disease()Symptom()}^{Disease()}
v[2]: {Symptom()}

c (Conclusion): {Disease()Symptom()}
test(verbose=False): Method used to test the example
```

## e71
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1970)


```
description:
    Examples 71 & 78, p209, p212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    
v[0]: {B(brown())~B(yellow()),B(yellow())~B(brown())}
v[1]: {50.0=* 0}^{B(yellow())~B(brown())}
v[2]: {50.0=* 0}^{B(brown())~B(yellow())}
v[3]: {B(yellow())~B(brown())}

v[0]: {50.0=* B(brown())~B(yellow()),50.0=* B(yellow())~B(brown())}
v[1]: {0,50.0=* B(yellow())~B(brown())}

test(verbose=False): Method used to test the example
```

## e72
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2007)


```
description:
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    
v[0]: {B(b())B(g())~B(r()),B(r())~B(b()),B(r())~B(g())}
v[1]: {33.333333=* 0}^{B(b())B(g())~B(r())}
v[2]: {33.333333=* 0}^{B(r())~B(g())}
v[3]: {33.333333=* 0}^{B(r())~B(b())}
v[4]: {B(b())B(r())}

v[0]: {33.333333=* B(b())B(g())~B(r()),33.333333=* B(r())~B(b()),33.333333=* B(r())~B(g())}
v[1]: {0,33.333333=* B(b())B(r())}

test(verbose=False): Method used to test the example
```

## e74
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2051)


```
description:
    Example 74, p197, p231

    (includes two background commitments)
    
v[0]: {D(j())H(j()),H(j()),P(j())}
v[1]: {E(j()*)}
v[2]: ∀x {0.85=* D(x)E(x*),0.15=* E(x*)~D(x)}^{E(x*)}
v[3]: ∀x {0.1=* E(x*)H(x),0.9=* E(x*)~H(x)}^{E(x*)}

v[0]: {0.085=* D(j())E(j()*)H(j()),0.765=* D(j())E(j()*)~H(j()),0.015=* E(j()*)H(j())~D(j()),0.135=* E(j()*)~D(j())~H(j())}
v[1]: {D(j())H(j())}

test(verbose=False): Method used to test the example
```

## e76
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2087)


```
description:
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    
v[0]: {Attic(a()),Fired(i()*)Guitar(j())Gun(i())Outoftune(j())}
v[1]: ∀x {0,Fired(x*)Gun(x)Trigger(x)}^{Fired(x*)Gun(x)}
v[2]: {Trigger(i())}

c (Conclusion): {Fired(i()*)Guitar(j())Gun(i())Outoftune(j())Trigger(i())}
test(verbose=False): Method used to test the example
```

## e81i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2129)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card
    
v[0]: {Box(Brown())~Box(Yellow()),Box(Yellow())~Box(Brown())}

c (Conclusion): {0,50.0=* Box(Yellow())}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2139)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card and a brown card
    
v[0]: {Box(Brown())~Box(Yellow()),Box(Yellow())~Box(Brown())}

c (Conclusion): {0}
prob (Probability): {Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2149)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is neither a yellow card nor a brown card
    
v[0]: {Box(Brown())~Box(Yellow()),Box(Yellow())~Box(Brown())}

c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2172)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card.
    
v[0]: {Box(Brown())Box(Yellow())}^{Box(Yellow())}

c (Conclusion): {0,50.0=* Box(Yellow())}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2182)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and a brown card.
    
v[0]: {Box(Brown())Box(Yellow())}^{Box(Yellow())}

c (Conclusion): {0,50.0=* Box(Brown())Box(Yellow())}
prob (Probability): {Box(Brown())Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2192)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is a yellow card and there is not a brown card.
    
v[0]: {Box(Brown())Box(Yellow())}^{Box(Yellow())}

c (Conclusion): {0}
prob (Probability): {Box(Yellow())~Box(Brown())}
test(verbose=False): Method used to test the example
```

## e82iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2202)


```
description:
    Example 82, p213

    There is a box in which if there is a yellow card then there is a brown card.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    In the box there is neither a yellow card nor a brown card.
    
v[0]: {Box(Brown())Box(Yellow())}^{Box(Yellow())}

c (Conclusion): {0}
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e83i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2231)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a red marble and blue in marble in the box.
    
v[0]: {33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* Box(Red()),33.333333333333336=* ~Box(Blue())~Box(Green())~Box(Red())}

c (Conclusion): {0}
prob (Probability): {Box(Blue())Box(Red())}
test(verbose=False): Method used to test the example
```

## e83ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2241)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a green marble and there is a blue marble.
    
v[0]: {33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* Box(Red()),33.333333333333336=* ~Box(Blue())~Box(Green())~Box(Red())}

c (Conclusion): {0,33.333333333333336=* Box(Blue())Box(Green())}
prob (Probability): {Box(Blue())Box(Green())}
test(verbose=False): Method used to test the example
```

## e84i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2254)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v[0]: {Box(Grey())Box(Mauve())~Box(White()),Box(Grey())Box(White())~Box(Mauve())}

c (Conclusion): {0,50.0=* Box(Grey())Box(Mauve())}
prob (Probability): {Box(Grey())Box(Mauve())}
test(verbose=False): Method used to test the example
```

## e84ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2276)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v[0]: {Box(Grey())~Box(Mauve())~Box(White()),Box(Mauve())~Box(Grey())~Box(White()),Box(White())~Box(Grey())~Box(Mauve())}

c (Conclusion): {0}
prob (Probability): {Box(Grey())Box(Mauve())}
test(verbose=False): Method used to test the example
```

## e85
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2299)


```
description:
    Example 85, p216

    Easy partial probability inference

    There is a box in which there is one and only one of these marbles: a
    green marble, a blue marble, or a red marble. The probability that a green
    marble is in the box is 0.6, and the probability that a blue marble is in
    the box is 0.2.

    What is the probability that a red marble is in the box?
    
v[0]: {Box(Blue()),Box(Green()),Box(Red())}
v[1]: {60.0=* Box(Green())}^{Box(Green())}
v[2]: {20.0=* Box(Blue())}^{Box(Blue())}

c (Conclusion): {0,20.0=* Box(Red())}
prob (Probability): {Box(Red())}
test(verbose=False): Method used to test the example
```

## e86
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2322)


```
description:
    Example 86, p217

    You have a hand of several cards with only limited information about it.

    There is an ace and a queen or a king and a jack or a ten.
    The probability that there is an ace and a queen is 0.6
    The probability that there is a king and a jack is 0.2

    What is the probability that there is a ten?
    
v[0]: {A()Q(),J()K(),X()}
v[1]: {60.0=* A()Q()}^{A()Q()}
v[2]: {20.0=* J()K()}^{J()K()}

c (Conclusion): {0,20.0=* X()}
prob (Probability): {X()}
test(verbose=False): Method used to test the example
```

## e88
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2344)


```
description:
    Example 88, p233

    P1: There is a 90% chance Superman can fly
    P2: Clark is superman

    C: There is a 90% chance Clark can fly
    
v[0]: {90.0=* CanFly(Superman())}
v[1]: {==(Clark(),Superman())}
v[2]: {==(Clark(),Superman()*)}
v[3]: {==(Clark(),Clark())}

c (Conclusion): {90.0=* CanFly(Clark())}
test(verbose=False): Method used to test the example
```

## e90_condA
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2374)


```
description:
    Example 90, p249, p273

    Imagine that you have been saving some extra money on the side to make some purchases,
    and on your most recent visit to the video store you come across a special sale of a new
    video. This video is one with your favourite actor or actress, and your favourite type of
    movie (such as a comedy, drama, thriller etc.). This particular video that you are considering
    is one you have been thinking about buying a long time. It is a available at a special sale price
    of $14.99. What would you do in this situation?
    
v[0]: {do(Buy(Video()*)),~do(Buy(Video()*))}

c (Conclusion): {do(Buy(Video()*))}
v[0]: ∀x {Fun()}^{do(Buy(x*))}

v[0]: {1.0=+ 0}^{Fun()}

test(verbose=False): Method used to test the example
```

## e90_condB
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2392)


```
v[0]: ∃a {do(Buy(Video()*)),do(Buy(a*))}

c (Conclusion): ∃a {do(Buy(Video()*)),do(Buy(a*))}
v[0]: ∀x {Fun()}^{do(Buy(x*))}

v[0]: {1.0=+ 0}^{Fun()}

test(verbose=False): Method used to test the example
```

## e92_award
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2428)


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
    
v[0]: {do(Award(ParentA()*)),do(Award(ParentB()*))}

c (Conclusion): {do(Award(ParentB()*))}
v[0]: ∀x {Custody(x*)}^{do(Award(x*))}
v[1]: ∀x {~Custody(x*)}^{do(Deny(x*))}
v[2]: {HighRapp(ParentB())LowTime(ParentB())MedRapp(ParentA())MedTime(ParentA())}

v[0]: ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)}
v[1]: ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)}
v[2]: ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)}
v[3]: ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)}
v[4]: ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}

test(verbose=False): Method used to test the example
```

## e92_deny
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2439)


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
    
v[0]: {do(Deny(ParentA()*)),do(Deny(ParentB()*))}

c (Conclusion): {do(Deny(ParentB()*))}
v[0]: ∀x {Custody(x*)}^{do(Award(x*))}
v[1]: ∀x {~Custody(x*)}^{do(Deny(x*))}
v[2]: {HighRapp(ParentB())LowTime(ParentB())MedRapp(ParentA())MedTime(ParentA())}

v[0]: ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)}
v[1]: ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)}
v[2]: ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)}
v[3]: ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)}
v[4]: ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}

test(verbose=False): Method used to test the example
```

## e93_grp1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2449)


```
description:
    Example 93, p255, p276

    The US is preparing for the outbreak of an unusual Asian disease, which
    is expected to kill 600 people. There are two possible treatments (A) and (B)
    with the following results:

    (Group 1) (A) 400 people die. (B) Nobody dies with 1/3 chance, 600 people die with 2/3 chance.
    Which treatment would you choose?
    
v[0]: {do(A()),do(B())}

c (Conclusion): {do(B())}
v[0]: {D(400.0*)}^{do(A())}
v[1]: {0.33=* D(0.0*),~D(0.0)}^{do(B())}
v[2]: {0.67=* D(600.0*),~D(600.0)}^{do(B())}

v[0]: ∀x {power(σ(1.0,log(σ(1.0,x))),-1.0)=+ 0}^{D(x*)}
v[1]: ∀x {σ(1.0,log(σ(1.0,x)))=+ 0}^{S(x*)}

test(verbose=False): Method used to test the example
```

## new_e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2491)


```
v[0]: ∀x ∃a ∀y {P(x,a)Q(a,y)}
v[1]: ∃b ∀z {P(b,z)}

c (Conclusion): ∃b ∀x ∀z ∃a ∀y {P(b,z)P(x,a)Q(a,y)}
test(verbose=False): Method used to test the example
```

## new_e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2502)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀x ∃b {Q(x*)R(b)}^{Q(x*)}

c (Conclusion): ∃a ∀x ∃b {P(a)Q(x*)R(b)}
test(verbose=False): Method used to test the example
```

## else_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2520)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀x ∃b {Q(x*)R(b)}^{Q(x*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_merge
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2524)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀x ∃b {Q(x*)R(b)}^{Q(x*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_suppose
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2528)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀x ∃b {Q(x*)R(b)}^{Q(x*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_uni_prod
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2532)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀x ∃b {Q(x*)R(b)}^{Q(x*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_query
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2541)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀y ∃a {Q(y*)R(a)}^{Q(y*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_which
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2545)


```
v[0]: ∃a ∀x {P(a)Q(x*)}
v[1]: ∀y ∃a {Q(y*)R(a)}^{Q(y*)}

c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## new_e5
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2549)


```
v[0]: ∀x ∀y ∃a ∃b ∀z ∃c {P(a*)P(b)P(c)P(y)P(z)Q(x*)}
v[1]: ∃d ∃e ∃f {P(d*)Q(e*)Q(f*)}

c (Conclusion): ∃d ∃e ∃f {P(d*)Q(e*)Q(f*)}
test(verbose=False): Method used to test the example
```

## new_e6_leibniz
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2557)


```
v[0]: ∃a ∃b {==(a,b)P(f(a),a)~P(f(b),a)}
v[1]: {}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e7_aristotle
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2562)


```
v[0]: ∃a {~==(a,a)}
v[1]: {}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2567)


```
v[0]: {t()=+ A()}
v[1]: {u()=* A()}

c (Conclusion): {u()=* t()=+ A()}
test(verbose=False): Method used to test the example
```

## new_e9
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2572)


```
v[0]: ∀x {P(x*)}
v[1]: {P(j()*)}

c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## new_e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2577)


```
v[0]: ∀x {f(x)=* A(x*)}
v[1]: ∃e {f(e)=* A(e*)}

c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2582)


```
v[0]: {f(12.0)=* A(12.0*)}
v[1]: ∃e {f(e)=* A(e*)}

c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e12
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2587)


```
v[0]: {A()}
v[1]: {}

c (Conclusion): {A()}
test(verbose=False): Method used to test the example
```

## new_e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2592)


```
v[0]: {f(12.0)=* A(12.0*),B()}

c (Conclusion): {}
prob (Probability): ∃e {A(e*)}
test(verbose=False): Method used to test the example
```

## new_e14
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2598)


```
v[0]: ∀x ∃y {A(f(x*))B(g(x*,y))}
v[1]: {A(f(j()*))}

c (Conclusion): ∃y {A(f(j()*))B(g(j()*,y))}
test(verbose=False): Method used to test the example
```

## new_e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2603)


```
v[0]: ∃k {==(Clark(),Superman())Defeats(k,Superman())}
v[1]: {==(Clark()*,Superman())}

c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2611)


```
v[0]: ∃k ∃x {==(Clark(),x)Defeats(k,x)}
v[1]: ∃x {==(Clark()*,x)}

c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2616)


```
v[0]: ∃k ∃x {==(Clark(),x)do(Defeats(k,x))}
v[1]: ∃x {==(Clark()*,x)}

c (Conclusion): ∃k {==(Clark(),Clark())do(Defeats(k,Clark()))}
test(verbose=False): Method used to test the example
```

## new_e18
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2621)


```
v[0]: {m()=* A()}
v[1]: {n()=* B()}

c (Conclusion): {m()**n()=* A()B()}
test(verbose=False): Method used to test the example
```

## new_e19_first_atom_do_atom
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2626)


```
v[0]: ∃k {==(Clark(),Superman())Defeats(k,Superman())}
v[1]: {do(A())}

c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e20_nested_issue_in_pred
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2631)


```
v[0]: ∃k {==(Clark(),Superman())Defeats(k,Superman())}
v[1]: {==(Clark(),f(Superman()*))}

c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e21_supp_is_something
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2639)


```
v[0]: ∃k {==(Clark(),Superman())Defeats(k,Superman())}
v[1]: {==(Clark()*,Superman())}^{}

c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e22_restrict_dep_rel_is_not_other
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2647)


```
v[0]: ∃k ∃x {==(Clark(),x)do(Defeats(k,x))}
v[1]: ∃y {==(Clark()*,y)}

c (Conclusion): ∃k ∃x {==(Clark(),x)do(Defeats(k,x))}
test(verbose=False): Method used to test the example
```

## AnswerPotential
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2652)


```
v[0]: {1.0=* 2.0=+ A()B(),A()C(),0.4=* B()C()}
v[1]: {A()}
v[2]: {B()}
v[3]: {C()}
v[4]: {C()D()}
v[5]: {C()~B()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## UniProduct
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2694)


```
v[0]: ∀x ∃a {E(x,a)P(x),~P(x*)}
v[1]: {P(j()*)}

c (Conclusion): ∃a {E(j(),a)P(j()),~P(j()*)}
test(verbose=False): Method used to test the example
```

## QueryTest
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2699)


```
description:
    From page 173
    
v[0]: ∀x {S(j()*)S(m()*)T(x,j()),S(j()*)S(m()*)T(x,m())}
v[1]: ∀x ∃a {S(a*)T(x,a)}

c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```

## QueryTest2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2711)


```
description:
    From page 173
    
v[0]: ∀x {S(j()*)S(m()*)T(x,j()),S(j()*)S(m()*)T(x,m())}
v[1]: ∃a ∀x {S(a*)T(x,a)}

c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```

## ClassicInfer
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2723)


```
v[0]: {p()}
v[1]: {q()}^{p()}

c (Conclusion): {q()}
test(verbose=False): Method used to test the example
```

## ClassicInferBlocked
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2728)


```
v[0]: {a()b(),c()d()}
v[1]: {a()}

c (Conclusion): {b()c()d(),b()c()~d(),b()d()~c(),b()~c()~d(),c()d()~b()}
test(verbose=False): Method used to test the example
```

## ClassicInferVerum
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2733)


```
v[0]: {0}
v[1]: {p()}

c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## ClassicSimpleMP
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2738)


```
v[0]: {p()}
v[1]: {q()}^{p()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## ClassicIllusoryBlocked
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2747)


```
v[0]: {a()b(),c()d()}
v[1]: {a()}

c (Conclusion): {}
test(verbose=False): Method used to test the example
```