# Case Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L404)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L423)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L439)


```
description:
    Example 3, p63:

    P1 There is at least an ace and a king or else there is at least a queen and
    a jack.
    P2 There isn't an ace.
    C There is a queen and a jack.
    
v (Views): (
   {Ace()King(),Queen()Jack()},
   {~Ace()}
)
c (Conclusion): {Queen()Jack()}
test(verbose=False): Method used to test the example
```

## e5ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L466)


```
description:
    Example 5, p72, part ii
    
v (Views): (
   {s1()r1(),p1()q1()},
   {p2()q2(),s2()r2()}
)
c (Conclusion): {p2()s1()r1()q2(),r2()s1()s2()r1(),p1()q1()s2()r2(),p2()p1()q1()q2()}
test(verbose=False): Method used to test the example
```

## e5iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L480)


```
description:
    Example 5, p72, part iii
    
v (Views): (
   {p1()q1(),s1()r1()},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e5iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L492)


```
description:
    Example 5, p72, part iv
    
v (Views): (
   {p1()q1(),s1()r1()},
   {0}
)
c (Conclusion): {p1()q1(),s1()r1()}
test(verbose=False): Method used to test the example
```

## e5v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L504)


```
description:
    Example 5, p72, part v
    
v (Views): (
   {0},
   {p1()q1(),s1()r1()}
)
c (Conclusion): {p1()q1(),s1()r1()}
test(verbose=False): Method used to test the example
```

## e6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L516)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L527)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L538)


```
description:
    Example 8, p74

    P1 There is an ace and a queen, or else there is a king and a ten
    P2 There is a king

    C There is a ten (and a king)
    
v (Views): (
   {t()k(),q()a()},
   {k()}
)
c (Conclusion): {t()}
test(verbose=False): Method used to test the example
```

## e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L552)


```
description:
    Example 10, p76

    P1 There is a king.
    P2 There is at least an ace and a queen, or else at least a king and a ten.
    C There is a king (reversed premises blocking illusory inference).
    
v (Views): (
   {K()},
   {T()K(),Q()A()}
)
c (Conclusion): {K()}
test(verbose=False): Method used to test the example
```

## e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L568)


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
c (Conclusion): {Drinks(j())Smokes(j()),Eats(m())Smokes(m())}
test(verbose=False): Method used to test the example
```

## e12i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L586)


```
description:
    Example 12i, p78

    ItisnotthecasethatPorQorR
    
v (Views): (
   {P(),Q(),R()}
)
c (Conclusion): {~Q()~R()~P()}
test(verbose=False): Method used to test the example
```

## e12ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L597)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L608)


```
description:
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    
v (Views): (
   {Q()P(),R()}^{S()}
)
c (Conclusion): {~R()S()~P(),S()~Q()~R()}
test(verbose=False): Method used to test the example
```

## e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L619)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L635)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L649)


```
description:
    Example 14-2, p81

    Factor examples
    
v (Views): (
   {R()P(),R()S()P(),Q()S()P()},
   {P()}^{S()}
)
c (Conclusion): {Q()S(),R()P(),R()S()}
test(verbose=False): Method used to test the example
```

## e14_3
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L663)


```
description:
    Example 14-3, p81

    Factor examples
    
v (Views): (
   {S()P(),Q()S(),R()P(),Q()R()},
   {P(),Q()}
)
c (Conclusion): {S(),R()}
test(verbose=False): Method used to test the example
```

## e14_6
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L677)


```
description:
    Example 14-6, p81

    Factor examples
    
v (Views): (
   {Q()S(),R()P()},
   {T(),P(),Q()}
)
c (Conclusion): {Q()S(),R()P()}
test(verbose=False): Method used to test the example
```

## e14_7
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L691)


```
description:
    Example 14-7, p81

    Factor examples
    
v (Views): (
   {Q()S(),R()P(),P()},
   {P(),Q()}
)
c (Conclusion): {0,S(),R()}
test(verbose=False): Method used to test the example
```

## e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L705)


```
description:
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    
v (Views): (
   {Ace(),Queen()Jack()Ace(),Eight()Four()Ten()},
   {Ace()Jack()Eight()Ten()},
   {~Queen()}
)
c (Conclusion): {Four()}
test(verbose=False): Method used to test the example
```

## e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L723)


```
description:
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    
v (Views): (
   {Queen()Jack()King(),Ace(),Eight()Four()Ten()},
   {~Four()},
   {~Ace()}
)
c (Conclusion): {Queen()Jack()King()}
test(verbose=False): Method used to test the example
```

## e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L740)


```
description:
    Example 17, p83

    P1 There is a king in the hand and there is not an ace in the hand, or else there is an ace in the hand and there is not a king in the hand.
    P2 There is a king in the hand.
    C There isn't an ace in the hand.
    
v (Views): (
   {~King()Ace(),~Ace()King()},
   {King()}
)
c (Conclusion): {~Ace()}
test(verbose=False): Method used to test the example
```

## e19
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L756)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L770)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L788)


```
description:
    Example 21, p86

    Any view Δ^{0} = [Δ^{0}]ᶰ can be derived from the absurd view
    
v (Views): (
   {s1()r1()}
)
c (Conclusion): {~r1(),~s1()}
test(verbose=False): Method used to test the example
```

## e22
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L806)


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
   {a()~c()~b(),~c()~a()~b(),~c()~a()b(),a()~c()b(),a()~b()c(),~a()b()c(),~a()~b()c()}
)
test(verbose=False): Method used to test the example
```

## e23_with_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L845)


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
   {~K()S()P(),K()L(),K()S()P()},
   {K()L(),K()S()P()}
)
test(verbose=False): Method used to test the example
```

## e23_without_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L881)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L913)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L946)


```
description:
    Example 25i, p89
    
v (Views): (
   {p()r(),q()p()},
   {p()}
)
c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L955)


```
description:
    Example 25ii, p89
    
v (Views): (
   {p()r(),q()p()},
   {q()}
)
c (Conclusion): {0,q()}
test(verbose=False): Method used to test the example
```

## e25iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L964)


```
description:
    Example 25iii, p89
    
v (Views): (
   {t(),p()r(),q()p(),s()},
   {p(),s()}
)
c (Conclusion): {0,p(),s()}
test(verbose=False): Method used to test the example
```

## e25iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L976)


```
description:
    Example 25iv, p89
    
v (Views): (
   {t(),p()r(),q()p(),s()},
   {t(),p(),s()}
)
c (Conclusion): {t(),p(),s()}
test(verbose=False): Method used to test the example
```

## e25v
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L988)


```
description:
    Example 25v, p89
    
v (Views): (
   {q()s()p(),s()p()r()},
   {p()}^{s()}
)
c (Conclusion): {p()}
test(verbose=False): Method used to test the example
```

## e25vi
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1000)


```
description:
    Example 25vi, p89
    
v (Views): (
   {q()s()p(),s()p()r()},
   {p()}^{t()}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e26
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1012)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1045)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1056)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1074)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1090)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1106)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1122)


```
description:
    Example 40, p119

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    
v (Views): (
   {SquareB()~TriangleB()~CircleB(),~SquareB()~TriangleB()CircleB(),~SquareB()TriangleB()~CircleB()},
   {SquareB()CircleT()}^{CircleT()},
   {TriangleB()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e40ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1155)


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
   {SquareB()~TriangleB()~CircleB(),~SquareB()~TriangleB()CircleB(),~SquareB()TriangleB()~CircleB()},
   {TriangleB()},
   {SquareB()CircleT()}^{CircleT()}
)
c (Conclusion): {~SquareB()TriangleB()~CircleB()~CircleT()}
test(verbose=False): Method used to test the example
```

## e41
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1192)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1208)


```
description:
    Example 42, p122

    P1 There is a circle at the top of the card only if there is a square
    at the bottom.
    P2 There is not a square at the bottom
    C There is not a circle at the top
    
v (Views): (
   {~SquareB()~CircleT()}^{~SquareB()},
   {~SquareB()}
)
c (Conclusion): {~CircleT()}
test(verbose=False): Method used to test the example
```

## e44_1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1228)


```
description:
    Example 44-1, p123

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    
v (Views): (
   {Saleable(c())Elegant(c()),~Elegant(c())~Saleable(c())},
   {~Elegant(c())~Stable(c()),Stable(c())Elegant(c())},
   {Saleable(c())Elegant(c()),Stable(c()),Saleable(c())}
)
c (Conclusion): {Stable(c())Saleable(c())Elegant(c())}
test(verbose=False): Method used to test the example
```

## e45
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1246)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1273)


```
description:
    Example 46, p126

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    
v (Views): (
   {V()P()}^{P()},
   {M()~P(),~M()P()},
   {0,M()V()}
)
c (Conclusion): (
   {M()~P(),~M()V()P()},
   {0}
)
test(verbose=False): Method used to test the example
```

## e46ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1310)


```
description:
    Example 46, part ii, p126

    If we had a view{VMR,VMS, T} and applied [{vm, 0}]Q we would get [{vm, 0}]
    
v (Views): (
   {S()M()V(),R()M()V(),T()},
   {0,M()V()}
)
c (Conclusion): {0,M()V()}
test(verbose=False): Method used to test the example
```

## e47
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1324)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1341)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1357)


```
description:
    Example 49, p130

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    
v (Views): (
   ∃x ∃y {King(x)Ace(Mary()),Jack(y)Queen(John())},
   {King(Sally())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e50_part1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1374)


```
description:
    Example 50, part1, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v (Views): (
   {L(s(),g())L(j(),s())},
   {M(j()*)~M(g()*)},
   {},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): (
   {L(s(),g())M(j()*)~M(g()*)L(j(),s())},
   {0}
)
test(verbose=False): Method used to test the example
```

## e50_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1411)


```
description:
    Example 50, part2, p131

    Jack is looking at Sally, but Sally is looking at George. Jack is married, but George is
    not. Is the married person looking at an unmarried person?

    (A) Yes
    (B) No
    (C) Cannot be determined
    
v (Views): (
   {L(s(),g())L(j(),s())},
   {M(j())~M(g())},
   {M(s())},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): ∃b ∃a {M(a*)~M(b*)L(a,b)}
g1 (Another View): {M(s())~M(g())L(s(),g())M(j())L(j(),s()),~M(g())L(s(),g())~M(s())M(j())L(j(),s())}
g2 (Another View): {M(s())~M(g()*)L(s(),g())M(j()*)L(j(),s()),~M(g()*)L(s(),g())~M(s()*)M(j()*)L(j(),s())}
test(verbose=False): Method used to test the example
```

## e50_part2_arbs
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1456)


```
description:
    Duplicate of e50, uses arb objects, some changes
    
v (Views): (
   ∃j ∃s ∃g {L(s,g)M(j)~M(g)L(j,s)},
   ∃s {M(s)},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): ∃b ∃a {M(a*)~M(b*)L(a,b)}
g1 (Another View): ∃j ∃s ∃g {M(j)~M(g)L(s,g)L(j,s)M(s),M(j)~M(g)L(s,g)~M(s)L(j,s)}
g2 (Another View): ∃j ∃s ∃g {M(j*)~M(g*)L(s,g)L(j,s)M(s),M(j*)~M(g*)L(s,g)~M(s*)L(j,s)}
test(verbose=False): Method used to test the example
```

## e51
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1487)


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
c (Conclusion): {HasNucleus(Halobacterium())IsArchaeon(Halobacterium()*)}
test(verbose=False): Method used to test the example
```

## e52
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1504)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1520)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1547)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1558)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1591)


```
description:
    Example 56, p134

    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    
v (Views): (
   ∀x ∃y {Teaches(x,y)Professor(x)Student(y*)}^{Professor(x)},
   ∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
)
c (Conclusion): ∃b ∃y {0,Reads(y,b)Book(b)}
test(verbose=False): Method used to test the example
```

## e56_basic_step
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1608)


```
v (Views): (
   ∀x ∃y {Teaches(x,y)Professor(x)Student(y*)}^{Professor(x)},
   ∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}
)
c (Conclusion): ∀a ∃c ∃b {Book(c)Student(b*)Professor(a)Teaches(a,b)Reads(b,c),~Professor(a)}
test(verbose=False): Method used to test the example
```

## e57
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1614)


```
description:
    Example 57, p134

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    
v (Views): (
   ∀x {A(x)B(x*)}^{B(x*)},
   ∃x {B(x*)C(x)}
)
c (Conclusion): ∃y {B(y*)A(y)C(y)}
test(verbose=False): Method used to test the example
```

## e58_reversed
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1630)


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
c (Conclusion): ∃y {B(y*)A(y)C(y)}
test(verbose=False): Method used to test the example
```

## e61
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1646)


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
c (Conclusion): ∀x ∃a {M(a*)M(j()*)D(x)B(x,a),M(j()*)~D(x)}
test(verbose=False): Method used to test the example
```

## e62
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1659)


```
description:
    Example 62, p176
    
v (Views): (
   {S(m()*)L(n(),m()),T(n())S(j()*)D(m()),~S(n()*)D(b())},
   ∃a {S(a*)}
)
c (Conclusion): {0,S(j()*),S(m()*)}
test(verbose=False): Method used to test the example
```

## e63
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1671)


```
description:
    Example 63, p176
    
v (Views): (
   {S(j()*)D(n()*),~D(j()*)D(n()*)T(j())},
   ∃a {D(a*)}
)
c (Conclusion): {D(n()*)}
test(verbose=False): Method used to test the example
```

## e63_modified
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1683)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1695)


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
   ∀x {1.0=* ~S(x*)T(x),~S(x*)~T(x)}^{~S(x*)},
   {T(Smith()*)},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*),0}
test(verbose=False): Method used to test the example
```

## e64ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1727)


```
v (Views): (
   ∀x {90.0=* P(x)T(x*)S(x*),P(x)~T(x)S(x*)}^{P(x)S(x*)},
   ∀x {1.0=* P(x)~S(x*)T(x),P(x)~S(x*)~T(x)}^{P(x)~S(x*)},
   ∀x {1.0=* P(x)S(x*),P(x)~S(x)}^{P(x)},
   {T(Smith()*)P(Smith())},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*)}
test(verbose=False): Method used to test the example
```

## e65
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1747)


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
   ∀x {0.3=* P(x*)C(x),P(x*)~C(x)}^{P(x*)},
   ∀x {50.0=* P(x*)T(x)C(x),P(x*)~T(x)C(x)}^{P(x*)C(x)},
   ∀x {3.0=* P(x*)T(x)~C(x),P(x*)~T(x)~C(x)}^{P(x*)~C(x)},
   ∃a {P(a*)T(a)},
   ∃a {C(a)}
)
c (Conclusion): ∃a {15.0=* C(a),0}
test(verbose=False): Method used to test the example
```

## e66i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1781)


```
description:
    Example 66, p191, p225

    Think of 100 people.

    1. One of the disease psylicrapitis, and he is likely to be positive.
    2. Of those who do not have the disease, 1 will also test positive.

    How many of those who test positive do have the disease? Out of ?
    
v (Views): (
   {1.0=* T()D(),1.0=* T()~D(),98.0=* ~D()},
   {T()D()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e66ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1809)


```
v (Views): (
   {1.0=* T()D(),1.0=* T()~D(),98.0=* ~D()},
   {T()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e67
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1826)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1855)


```
description:
    Example 69, p192, p218

    The suspect's DNA matches the crime sample.

    If the suspect is not guilty, then the probability of such a DNA match is 1 in
    a million

    Is the suspect likely to be guilty?
    
v (Views): (
   {Match(Suspect())},
   {0.000001=* Match(Suspect())~Guilty(Suspect()),~Match(Suspect())~Guilty(Suspect())}^{~Guilty(Suspect())}
)
c (Conclusion): {0.000001=* Match(Suspect())~Guilty(Suspect()),Match(Suspect())Guilty(Suspect())}
test(verbose=False): Method used to test the example
```

## e69_part2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1889)


```
v (Views): (
   {0.000001=* Match(Suspect())~Guilty(Suspect()),Match(Suspect())Guilty(Suspect())},
   {999999.999999=* 0}^{Match(Suspect())Guilty(Suspect())},
   {Guilty(Suspect())}
)
c (Conclusion): (
   {0.000001=* Match(Suspect())~Guilty(Suspect()),999999.999999=* Match(Suspect())Guilty(Suspect())},
   {999999.999999=* Guilty(Suspect()),0}
)
test(verbose=False): Method used to test the example
```

## e70
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1916)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1941)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L1978)


```
description:
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    
v (Views): (
   {B(b())B(g())~B(r()),B(r())~B(g()),~B(b())B(r())},
   {33.333333=* 0}^{B(b())B(g())~B(r())},
   {33.333333=* 0}^{B(r())~B(g())},
   {33.333333=* 0}^{~B(b())B(r())},
   {B(b())B(r())}
)
c (Conclusion): (
   {33.333333=* B(b())B(g())~B(r()),33.333333=* B(r())~B(g()),33.333333=* ~B(b())B(r())},
   {33.333333=* B(b())B(r()),0}
)
test(verbose=False): Method used to test the example
```

## e74
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2022)


```
description:
    Example 74, p197, p231

    (includes two background commitments)
    
v (Views): (
   {D(j())H(j()),H(j()),P(j())},
   {E(j()*)},
   ∀x {0.85=* E(x*)D(x),0.15=* E(x*)~D(x)}^{E(x*)},
   ∀x {0.1=* E(x*)H(x),0.9=* E(x*)~H(x)}^{E(x*)}
)
c (Conclusion): (
   {0.085=* E(j()*)H(j())D(j()),0.765=* ~H(j())E(j()*)D(j()),0.015=* ~D(j())E(j()*)H(j()),0.135=* ~D(j())~H(j())E(j()*)},
   {D(j())H(j())}
)
test(verbose=False): Method used to test the example
```

## e76
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2058)


```
description:
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    
v (Views): (
   {Outoftune(j())Gun(i())Guitar(j())Fired(i()*),Attic(a())},
   ∀x {Fired(x*)Trigger(x)Gun(x),0}^{Fired(x*)Gun(x)},
   {Trigger(i())}
)
c (Conclusion): {Outoftune(j())Gun(i())Fired(i()*)Trigger(i())Guitar(j())}
test(verbose=False): Method used to test the example
```

## e81i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2100)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card
    
v (Views): (
   {Box(Yellow())~Box(Brown()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {50.0=* Box(Yellow()),0}
prob (Probability): {Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e81ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2110)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is a yellow card and a brown card
    
v (Views): (
   {Box(Yellow())~Box(Brown()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {Box(Yellow())Box(Brown())}
test(verbose=False): Method used to test the example
```

## e81iii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2120)


```
description:
    Example 81, p213

    There is a box in which there is a yellow card, or a brown card, but not both

    Given the preceding assertion, according to you, what is the probability of the following situation?
    
    In the box there is neither a yellow card nor a brown card
    
v (Views): (
   {Box(Yellow())~Box(Brown()),Box(Brown())~Box(Yellow())}
)
c (Conclusion): {0}
prob (Probability): {~Box(Yellow())~Box(Brown())}
test(verbose=False): Method used to test the example
```

## e82i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2143)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2153)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2163)


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
prob (Probability): {Box(Yellow())~Box(Brown())}
test(verbose=False): Method used to test the example
```

## e82iv
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2173)


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
prob (Probability): {~Box(Yellow())~Box(Brown())}
test(verbose=False): Method used to test the example
```

## e83i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2202)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a red marble and blue in marble in the box.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Green())Box(Blue()),33.333333333333336=* ~Box(Green())~Box(Red())~Box(Blue())}
)
c (Conclusion): {0}
prob (Probability): {Box(Red())Box(Blue())}
test(verbose=False): Method used to test the example
```

## e83ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2212)


```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a green marble and there is a blue marble.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Green())Box(Blue()),33.333333333333336=* ~Box(Green())~Box(Red())~Box(Blue())}
)
c (Conclusion): {33.333333333333336=* Box(Green())Box(Blue()),0}
prob (Probability): {Box(Green())Box(Blue())}
test(verbose=False): Method used to test the example
```

## e84i
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2225)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble and either a white marble or
    else a mauve marble but not all three marbles are in the box.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {Box(White())~Box(Mauve())Box(Grey()),Box(Mauve())~Box(White())Box(Grey())}
)
c (Conclusion): {50.0=* Box(Mauve())Box(Grey()),0}
prob (Probability): {Box(Mauve())Box(Grey())}
test(verbose=False): Method used to test the example
```

## e84ii
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2247)


```
description:
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(Mauve())~Box(White())Box(Grey()),Box(White())~Box(Mauve())~Box(Grey()),Box(Mauve())~Box(White())~Box(Grey())}
)
c (Conclusion): {0}
prob (Probability): {Box(Mauve())Box(Grey())}
test(verbose=False): Method used to test the example
```

## e85
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2270)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2293)


```
description:
    Example 86, p217

    You have a hand of several cards with only limited information about it.

    There is an ace and a queen or a king and a jack or a ten.
    The probability that there is an ace and a queen is 0.6
    The probability that there is a king and a jack is 0.2

    What is the probability that there is a ten?
    
v (Views): (
   {A()Q(),K()J(),X()},
   {60.0=* A()Q()}^{A()Q()},
   {20.0=* K()J()}^{K()J()}
)
c (Conclusion): {20.0=* X(),0}
prob (Probability): {X()}
test(verbose=False): Method used to test the example
```

## e88
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2315)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2345)


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
   {do(Buy(Video()*)),~do(Buy(Video()*))}
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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2363)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2399)


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
   {MedRapp(ParentA())HighRapp(ParentB())LowTime(ParentB())MedTime(ParentA())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{~Custody(x*)LowTime(x)}
)
test(verbose=False): Method used to test the example
```

## e92_deny
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2410)


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
   {MedRapp(ParentA())HighRapp(ParentB())LowTime(ParentB())MedTime(ParentA())}
)
pr (Priority Views): (
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{MedTime(x)~Custody(x*)},
   ∀x {2.0=+ 0}^{~Custody(x*)LowTime(x)}
)
test(verbose=False): Method used to test the example
```

## e93_grp1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2420)


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
   ∀x {power(σ(1.0,log(σ(1.0,x))),-1.0)=+ 0}^{D(x*)},
   ∀x {σ(1.0,log(σ(1.0,x)))=+ 0}^{S(x*)}
)
test(verbose=False): Method used to test the example
```

## new_e1
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2462)


```
v (Views): (
   ∀x ∃a ∀y {Q(a,y)P(x,a)},
   ∃b ∀z {P(b,z)}
)
c (Conclusion): ∃b ∀x ∀z ∃a ∀y {Q(a,y)P(b,z)P(x,a)}
test(verbose=False): Method used to test the example
```

## new_e2
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2473)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x ∃b {P(a)Q(x*)R(b)}
test(verbose=False): Method used to test the example
```

## else_inquire
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2491)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_merge
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2495)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_suppose
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2499)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_uni_prod
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2503)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀x ∃b {R(b)Q(x*)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_query
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2512)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## else_which
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2516)


```
v (Views): (
   ∃a ∀x {P(a)Q(x*)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {P(a)Q(x*)}
test(verbose=False): Method used to test the example
```

## new_e5
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2520)


```
v (Views): (
   ∀y ∀x ∃a ∃b ∀z ∃c {P(y)P(z)P(b)P(c)P(a*)Q(x*)},
   ∃d ∃f ∃e {Q(f*)P(d*)Q(e*)}
)
c (Conclusion): ∃d ∃f ∃e {Q(e*)P(d*)Q(f*)}
test(verbose=False): Method used to test the example
```

## new_e6_leibniz
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2528)


```
v (Views): (
   ∃b ∃a {P(f(a),a)==(a,b)~P(f(b),a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e7_aristotle
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2533)


```
v (Views): (
   ∃a {~==(a,a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e8
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2538)


```
v (Views): (
   {t()=+ A()},
   {u()=* A()}
)
c (Conclusion): {u()=* t()=+ A()}
test(verbose=False): Method used to test the example
```

## new_e9
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2543)


```
v (Views): (
   ∀x {P(x*)},
   {P(j()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## new_e10
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2548)


```
v (Views): (
   ∀x {f(x)=* A(x*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e11
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2553)


```
v (Views): (
   {f(12.0)=* A(12.0*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e12
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2558)


```
v (Views): (
   {A()},
   {}
)
c (Conclusion): {A()}
test(verbose=False): Method used to test the example
```

## new_e13
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2563)


```
v (Views): (
   {f(12.0)=* A(12.0*),B()}
)
c (Conclusion): {}
prob (Probability): ∃e {A(e*)}
test(verbose=False): Method used to test the example
```

## new_e14
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2569)


```
v (Views): (
   ∀x ∃y {B(g(x*,y))A(f(x*))},
   {A(f(j()*))}
)
c (Conclusion): ∃y {A(f(j()*))B(g(j()*,y))}
test(verbose=False): Method used to test the example
```

## new_e15
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2574)


```
v (Views): (
   ∃k {==(Clark(),Superman())Defeats(k,Superman())},
   {==(Clark()*,Superman())}
)
c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e16
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2582)


```
v (Views): (
   ∃x ∃k {==(Clark(),x)Defeats(k,x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e17
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2587)


```
v (Views): (
   ∃x ∃k {do(Defeats(k,x))==(Clark(),x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {do(Defeats(k,Clark()))==(Clark(),Clark())}
test(verbose=False): Method used to test the example
```

## new_e18
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2592)


```
v (Views): (
   {m()=* A()},
   {n()=* B()}
)
c (Conclusion): {m()**n()=* A()B()}
test(verbose=False): Method used to test the example
```

## new_e19_first_atom_do_atom
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2597)


```
v (Views): (
   ∃k {==(Clark(),Superman())Defeats(k,Superman())},
   {do(A())}
)
c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e20_nested_issue_in_pred
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2602)


```
v (Views): (
   ∃k {==(Clark(),Superman())Defeats(k,Superman())},
   {==(Clark(),f(Superman()*))}
)
c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e21_supp_is_something
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2610)


```
v (Views): (
   ∃k {==(Clark(),Superman())Defeats(k,Superman())},
   {==(Clark()*,Superman())}^{}
)
c (Conclusion): ∃k {==(Clark(),Superman())Defeats(k,Superman())}
test(verbose=False): Method used to test the example
```

## new_e22_restrict_dep_rel_is_not_other
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2618)


```
v (Views): (
   ∃x ∃k {do(Defeats(k,x))==(Clark(),x)},
   ∃y {==(Clark()*,y)}
)
c (Conclusion): ∃x ∃k {do(Defeats(k,x))==(Clark(),x)}
test(verbose=False): Method used to test the example
```

## AnswerPotential
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2623)


```
v (Views): (
   {1.0=* 2.0=+ A()B(),0.4=* B()C(),A()C()},
   {A()},
   {B()},
   {C()},
   {D()C()},
   {~B()C()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## UniProduct
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2665)


```
v (Views): (
   ∀x ∃a {P(x)E(x,a),~P(x*)},
   {P(j()*)}
)
c (Conclusion): ∃a {~P(j()*),P(j())E(j(),a)}
test(verbose=False): Method used to test the example
```

## QueryTest
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2670)


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
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/cases.py#L2682)


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