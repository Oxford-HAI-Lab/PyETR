# Case Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## e1
```
description:
    Example 1, p61:

    P1 Either Jane is kneeling by the fire and she is looking at the TV or else
    Mark is standing at the window and he is peering into the garden.
    P2 Jane is kneeling by the fire.
    C Jane is looking at the TV.
    
v (Views): (
   {LookingAtTV(Jane())KneelingByTheFire(Jane()),StandingAtTheWindow(Mark())PeeringIntoTheGarden(Mark())},
   {KneelingByTheFire(Jane())}
)
c (Conclusion): {LookingAtTV(Jane())}
test(verbose=False): Method used to test the example
```

## e2
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
```
description:
    Example 5, p72, part ii
    
v (Views): (
   {r1()s1(),p1()q1()},
   {q2()p2(),r2()s2()}
)
c (Conclusion): {q2()r1()s1()p2(),r1()s1()r2()s2(),p1()r2()q1()s2(),p1()q2()q1()p2()}
test(verbose=False): Method used to test the example
```

## e5iii
```
description:
    Example 5, p72, part iii
    
v (Views): (
   {p1()q1(),r1()s1()},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e5iv
```
description:
    Example 5, p72, part iv
    
v (Views): (
   {p1()q1(),r1()s1()},
   {0}
)
c (Conclusion): {p1()q1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e5v
```
description:
    Example 5, p72, part v
    
v (Views): (
   {0},
   {p1()q1(),r1()s1()}
)
c (Conclusion): {p1()q1(),r1()s1()}
test(verbose=False): Method used to test the example
```

## e6
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
```
description:
    Example 12i, p78

    ItisnotthecasethatPorQorR
    
v (Views): (
   {P(),Q(),R()}
)
c (Conclusion): {~R()~P()~Q()}
test(verbose=False): Method used to test the example
```

## e12ii
```
description:
    Example 12ii, p78

    ItisnotthecasethatPandQandR
    
v (Views): (
   {Q()P()R()}
)
c (Conclusion): {~R(),~P(),~Q()}
test(verbose=False): Method used to test the example
```

## e12iii
```
description:
    Example 12iii, p79

    It is not the case that, supposing S, ((P and Q) or R)
    
v (Views): (
   {P()Q(),R()}^{S()}
)
c (Conclusion): {~R()~P()S(),S()~R()~Q()}
test(verbose=False): Method used to test the example
```

## e13
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
```
description:
    Example 14-2, p81

    Factor examples
    
v (Views): (
   {P()R(),P()R()S(),P()Q()S()},
   {P()}^{S()}
)
c (Conclusion): {Q()S(),P()R(),R()S()}
test(verbose=False): Method used to test the example
```

## e14_3
```
description:
    Example 14-3, p81

    Factor examples
    
v (Views): (
   {P()S(),Q()S(),P()R(),R()Q()},
   {P(),Q()}
)
c (Conclusion): {S(),R()}
test(verbose=False): Method used to test the example
```

## e14_6
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
```
description:
    Example 15, p82

    P1 There is an ace and a jack and a queen, or else there is an eight and a ten and a four, or else there is an ace.
    P2 There is an ace and a jack, and there is an eight and a ten.
    P3 There is not a queen.
    C There is a four
    
v (Views): (
   {Ace(),Jack()Ace()Queen(),Eight()Ten()Four()},
   {Eight()Ten()Jack()Ace()},
   {~Queen()}
)
c (Conclusion): {Four()}
test(verbose=False): Method used to test the example
```

## e16
```
description:
    Example 16, p83

    P1 There is a ten and an eight and a four, or else there is a jack and a king and a queen, or else there is an ace.
    P2 There isn't a four.
    P3 There isn't an ace.
    
v (Views): (
   {King()Queen()Jack(),Ace(),Eight()Ten()Four()},
   {~Four()},
   {~Ace()}
)
c (Conclusion): {King()Queen()Jack()}
test(verbose=False): Method used to test the example
```

## e17
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
```
description:
    Example 22, p87

    It is not the case that A and B and C
    
v (Views): (
   {c()b()a()},
   {a()},
   {b()},
   {c()}
)
c (Conclusion): (
   {~c(),~b(),~a()},
   {~c()a()~b(),~a()~c()~b(),~a()b()~c(),b()~c()a(),c()a()~b(),c()~a()b(),c()~a()~b()}
)
test(verbose=False): Method used to test the example
```

## e23_with_inquire
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
   {~K()P()S(),L()K(),P()K()S()},
   {L()K(),P()K()S()}
)
test(verbose=False): Method used to test the example
```

## e23_without_inquire
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
   {~q()a(),q()a()},
   {a(),q()}
)
test(verbose=False): Method used to test the example
```

## e25i
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
```
description:
    Example 40, p119

    (P0 Shapes at the bottom of the card are mutually exclusive)
    P1 If there is a circle at the top of the card, then there is a
    square on the bottom.
    P2 There is a triangle on the bottom
    C Falsum
    
v (Views): (
   {~CircleB()SquareB()~TriangleB(),~TriangleB()CircleB()~SquareB(),~CircleB()TriangleB()~SquareB()},
   {CircleT()SquareB()}^{CircleT()},
   {TriangleB()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e40ii
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
   {~CircleB()SquareB()~TriangleB(),~TriangleB()CircleB()~SquareB(),~CircleB()TriangleB()~SquareB()},
   {TriangleB()},
   {CircleT()SquareB()}^{CircleT()}
)
c (Conclusion): {~CircleB()TriangleB()~CircleT()~SquareB()}
test(verbose=False): Method used to test the example
```

## e41
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
```
description:
    Example 44-1, p123

    P1 The chair is saleable if and only if it is inelegant.
    P2 The chair is elegant if and only if it is stable.
    P3 The chair is saleable or it is stable, or both.
    C The chair is saleable elegant and stable.
    
v (Views): (
   {Saleable(c())Elegant(c()),~Saleable(c())~Elegant(c())},
   {~Stable(c())~Elegant(c()),Elegant(c())Stable(c())},
   {Saleable(c())Elegant(c()),Stable(c()),Saleable(c())}
)
c (Conclusion): {Saleable(c())Elegant(c())Stable(c())}
test(verbose=False): Method used to test the example
```

## e45
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
```
description:
    Example 46, p126

    P1 Pat is here then Viv is here
    P2 Mo is here or else Pat is here, but not both

    C No
    
v (Views): (
   {P()V()}^{P()},
   {M()~P(),~M()P()},
   {0,M()V()}
)
c (Conclusion): (
   {M()~P(),~M()P()V()},
   {0}
)
test(verbose=False): Method used to test the example
```

## e46ii
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
```
description:
    Example 49, p130

    P1 Either there is an ace in Mary's hand and some other player has a king,
    or else there is a queen in John's hand and some other player has a jack.
    P2 Sally has a king
    C Truth
    
v (Views): (
   ∃x ∃y {Ace(Mary())King(x),Jack(y)Queen(John())},
   {King(Sally())}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## e50_part1
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
   {~M(g()*)M(j()*)},
   {},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): (
   {~M(g()*)M(j()*)L(s(),g())L(j(),s())},
   {0}
)
test(verbose=False): Method used to test the example
```

## e50_part2
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
   {~M(g())M(j())},
   {M(s())},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): ∃b ∃a {M(a*)~M(b*)L(a,b)}
g1 (Another View): {L(j(),s())M(s())M(j())L(s(),g())~M(g()),L(j(),s())M(j())L(s(),g())~M(s())~M(g())}
g2 (Another View): {L(j(),s())M(s())M(j()*)L(s(),g())~M(g()*),L(j(),s())M(j()*)L(s(),g())~M(s()*)~M(g()*)}
test(verbose=False): Method used to test the example
```

## e50_part2_arbs
```
description:
    Duplicate of e50, uses arb objects, some changes
    
v (Views): (
   ∃g ∃s ∃j {L(j,s)M(j)~M(g)L(s,g)},
   ∃s {M(s)},
   ∃b ∃a {M(a*)~M(b*)L(a,b)}
)
c (Conclusion): ∃b ∃a {M(a*)~M(b*)L(a,b)}
g1 (Another View): ∃g ∃s ∃j {~M(g)L(s,g)L(j,s)M(j)M(s),~M(s)~M(g)L(s,g)L(j,s)M(j)}
g2 (Another View): ∃g ∃s ∃j {~M(g*)L(s,g)L(j,s)M(j*)M(s),~M(s*)~M(g*)L(s,g)L(j,s)M(j*)}
test(verbose=False): Method used to test the example
```

## e51
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
c (Conclusion): {G(John()*)F(John())}
test(verbose=False): Method used to test the example
```

## e53
```
description:
    Example 53, p132 & p175

    P All A are B.
    C All B are A.
    
v (Views): (
   ∀x {B(x)A(x)}^{A(x)},
   ∀x {B(x)},
   ∀x {B(x)A(x)}^{B(x)}
)
c (Conclusion): ∀x {B(x)A(x)}^{B(x)}
test(verbose=False): Method used to test the example
```

## e54
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
```
description:
    Example 56, p134

    P1: Every professor teaches some student
    P2: Every student reads some book

    C: Every professor teaches some student who reads some book
    
v (Views): (
   ∀x ∃y {Professor(x)Teaches(x,y)Student(y*)}^{Professor(x)},
   ∀z ∃w {Reads(z,w)Student(z*)Book(w)}^{Student(z*)}
)
c (Conclusion): ∃b ∃y {0,Book(b)Reads(y,b)}
test(verbose=False): Method used to test the example
```

## e56_basic_step
```
v (Views): (
   ∀x ∃y {Professor(x)Teaches(x,y)Student(y*)}^{Professor(x)},
   ∀z ∃w {Reads(z,w)Student(z*)Book(w)}^{Student(z*)}
)
c (Conclusion): ∀a ∃c ∃b {Professor(a)Teaches(a,b)Student(b*)Reads(b,c)Book(c),~Professor(a)}
test(verbose=False): Method used to test the example
```

## e57
```
description:
    Example 57, p134

    P1 All B are A.
    P2 Some C are B.
    C Some C are A.
    
v (Views): (
   ∀x {B(x*)A(x)}^{B(x*)},
   ∃x {C(x)B(x*)}
)
c (Conclusion): ∃y {A(y)C(y)B(y*)}
test(verbose=False): Method used to test the example
```

## e58_reversed
```
description:
    Example 58 reversed, based on p135

    P1 All C are B.
    P2 Some B are A.
    C Some C are A.
    
v (Views): (
   ∀y {C(y)B(y*)}^{C(y)},
   ∃x {B(x*)A(x)}
)
c (Conclusion): ∃y {A(y)C(y)B(y*)}
test(verbose=False): Method used to test the example
```

## e61
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
c (Conclusion): ∀x ∃a {D(x)B(x,a)M(a*)M(j()*),~D(x)M(j()*)}
test(verbose=False): Method used to test the example
```

## e62
```
description:
    Example 62, p176
    
v (Views): (
   {L(n(),m())S(m()*),T(n())D(m())S(j()*),D(b())~S(n()*)},
   ∃a {S(a*)}
)
c (Conclusion): {0,S(j()*),S(m()*)}
test(verbose=False): Method used to test the example
```

## e63
```
description:
    Example 63, p176
    
v (Views): (
   {D(n()*)S(j()*),~D(j()*)D(n()*)T(j())},
   ∃a {D(a*)}
)
c (Conclusion): {D(n()*)}
test(verbose=False): Method used to test the example
```

## e63_modified
```
description:
    Example 63, p176
    
v (Views): (
   ∀x ∃y {D(n()*)S(j()*),~D(j()*)D(f(y,x)*)T(j())},
   ∃a {D(a*)}
)
c (Conclusion): ∀x ∃y {D(n()*),D(f(y,x)*)}
test(verbose=False): Method used to test the example
```

## e64i
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
   ∀x {1.0=* T(x)~S(x*),~T(x)~S(x*)}^{~S(x*)},
   {T(Smith()*)},
   {S(Smith())}
)
c (Conclusion): {90.0=* S(Smith()*),0}
test(verbose=False): Method used to test the example
```

## e64ii
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
   ∀x {50.0=* C(x)T(x)P(x*),C(x)~T(x)P(x*)}^{C(x)P(x*)},
   ∀x {3.0=* T(x)~C(x)P(x*),~T(x)~C(x)P(x*)}^{~C(x)P(x*)},
   ∃a {P(a*)T(a)},
   ∃a {C(a)}
)
c (Conclusion): ∃a {15.0=* C(a),0}
test(verbose=False): Method used to test the example
```

## e66i
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
```
v (Views): (
   {1.0=* T()D(),1.0=* ~D()T(),98.0=* ~D()},
   {T()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## e67
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
```
description:
    Examples 71 & 78, p209, p212

    There is a box in which there is a yellow card or a brown card, but not both.

    Given the preceding assertion, according to you, what is the probability of the following situation?

    In the box there is a yellow card and there is not a brown card
    
v (Views): (
   {B(yellow())~B(brown()),B(brown())~B(yellow())},
   {50.0=* 0}^{B(yellow())~B(brown())},
   {50.0=* 0}^{B(brown())~B(yellow())},
   {B(yellow())~B(brown())}
)
c (Conclusion): (
   {50.0=* B(yellow())~B(brown()),50.0=* B(brown())~B(yellow())},
   {50.0=* B(yellow())~B(brown()),0}
)
test(verbose=False): Method used to test the example
```

## e72
```
description:
    Example 72 & 80, p196, p213

    There is a box in which there is at least a red marble or else there is a green
    marble and there is a blue marble, but not all three marbles.

    What is the probability of the following situation:

    There is a red marble and a blue marble in the box?
    
v (Views): (
   {B(g())B(b())~B(r()),~B(g())B(r()),~B(b())B(r())},
   {33.333333=* 0}^{B(g())B(b())~B(r())},
   {33.333333=* 0}^{~B(g())B(r())},
   {33.333333=* 0}^{~B(b())B(r())},
   {B(b())B(r())}
)
c (Conclusion): (
   {33.333333=* B(g())B(b())~B(r()),33.333333=* ~B(g())B(r()),33.333333=* ~B(b())B(r())},
   {33.333333=* B(b())B(r()),0}
)
test(verbose=False): Method used to test the example
```

## e74
```
description:
    Example 74, p197, p231

    (includes two background commitments)
    
v (Views): (
   {H(j())D(j()),H(j()),P(j())},
   {E(j()*)},
   ∀x {0.85=* D(x)E(x*),0.15=* ~D(x)E(x*)}^{E(x*)},
   ∀x {0.1=* H(x)E(x*),0.9=* ~H(x)E(x*)}^{E(x*)}
)
c (Conclusion): (
   {0.085=* H(j())E(j()*)D(j()),0.765=* ~H(j())E(j()*)D(j()),0.015=* ~D(j())H(j())E(j()*),0.135=* ~D(j())~H(j())E(j()*)},
   {H(j())D(j())}
)
test(verbose=False): Method used to test the example
```

## e76
```
description:
    Example 76 (guns and guitars), p199, p226,  p229

    (P1) The gun fired and the guitar was out of tune, or else someone was in the attic
    (P1.5, see p228) Guns who triggers are pulled fire
    (P2) The trigger (of the gun) was pulled. Does it follow that the guitar was out of
    tune?
    
v (Views): (
   {Fired(i()*)Gun(i())Guitar(j())Outoftune(j()),Attic(a())},
   ∀x {Trigger(x)Gun(x)Fired(x*),0}^{Fired(x*)Gun(x)},
   {Trigger(i())}
)
c (Conclusion): {Fired(i()*)Gun(i())Guitar(j())Trigger(i())Outoftune(j())}
test(verbose=False): Method used to test the example
```

## e81i
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
prob (Probability): {~Box(Brown())~Box(Yellow())}
test(verbose=False): Method used to test the example
```

## e82i
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
```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a red marble and blue in marble in the box.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* ~Box(Red())~Box(Blue())~Box(Green())}
)
c (Conclusion): {0}
prob (Probability): {Box(Red())Box(Blue())}
test(verbose=False): Method used to test the example
```

## e83ii
```
description:
    Example 83, p214

    There is a box in which there is a red marble, or else there is a green
    marble and there is a blue marble, but not all three marbles.

    Given the preceding assertion, according to you, what is the probability of the
    following situation?
    
    There is a green marble and there is a blue marble.
    
v (Views): (
   {33.333333333333336=* Box(Red()),33.333333333333336=* Box(Blue())Box(Green()),33.333333333333336=* ~Box(Red())~Box(Blue())~Box(Green())}
)
c (Conclusion): {33.333333333333336=* Box(Blue())Box(Green()),0}
prob (Probability): {Box(Blue())Box(Green())}
test(verbose=False): Method used to test the example
```

## e84i
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
```
description:
    Example 84, p215

    There is a box in which there is a grey marble, or else a white marble, or else a mauve marble,
    but no more than one marble.

    Given the preceding assertion, what is the probability of the following
    situation?

    In the box there is a grey marble and there is a mauve marble.
    
v (Views): (
   {~Box(Mauve())~Box(White())Box(Grey()),~Box(Grey())~Box(Mauve())Box(White()),~Box(Grey())~Box(White())Box(Mauve())}
)
c (Conclusion): {0}
prob (Probability): {Box(Grey())Box(Mauve())}
test(verbose=False): Method used to test the example
```

## e85
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
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{~Custody(x*)MedTime(x)},
   ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}
)
test(verbose=False): Method used to test the example
```

## e92_deny
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
   ∀x {1.0=+ 0}^{Custody(x*)MedRapp(x)},
   ∀x {3.0=+ 0}^{Custody(x*)HighRapp(x)},
   ∀x {1.0=+ 0}^{Custody(x*)MedTime(x)},
   ∀x {1.0=+ 0}^{~Custody(x*)MedTime(x)},
   ∀x {2.0=+ 0}^{LowTime(x)~Custody(x*)}
)
test(verbose=False): Method used to test the example
```

## e93_grp1
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
```
v (Views): (
   ∀x ∃a ∀y {Q(a,y)P(x,a)},
   ∃b ∀z {P(b,z)}
)
c (Conclusion): ∃b ∀x ∀z ∃a ∀y {Q(a,y)P(x,a)P(b,z)}
test(verbose=False): Method used to test the example
```

## new_e2
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x ∃b {Q(x*)P(a)R(b)}
test(verbose=False): Method used to test the example
```

## else_inquire
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_merge
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_suppose
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_uni_prod
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀x ∃b {Q(x*)R(b)}^{Q(x*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_query
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## else_which
```
v (Views): (
   ∃a ∀x {Q(x*)P(a)},
   ∀y ∃a {Q(y*)R(a)}^{Q(y*)}
)
c (Conclusion): ∃a ∀x {Q(x*)P(a)}
test(verbose=False): Method used to test the example
```

## new_e5
```
v (Views): (
   ∀x ∀y ∃a ∃b ∀z ∃c {P(c)P(b)P(y)P(a*)P(z)Q(x*)},
   ∃d ∃f ∃e {Q(f*)P(d*)Q(e*)}
)
c (Conclusion): ∃d ∃f ∃e {Q(f*)P(d*)Q(e*)}
test(verbose=False): Method used to test the example
```

## new_e6_leibniz
```
v (Views): (
   ∃b ∃a {==(a,b)~P(f(b),a)P(f(a),a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e7_aristotle
```
v (Views): (
   ∃a {~==(a,a)},
   {}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## new_e8
```
v (Views): (
   {t()=+ A()},
   {u()=* A()}
)
c (Conclusion): {u()=* t()=+ A()}
test(verbose=False): Method used to test the example
```

## new_e9
```
v (Views): (
   ∀x {P(x*)},
   {P(j()*)}
)
c (Conclusion): {0}
test(verbose=False): Method used to test the example
```

## new_e10
```
v (Views): (
   ∀x {f(x)=* A(x*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e11
```
v (Views): (
   {f(12.0)=* A(12.0*)},
   ∃e {f(e)=* A(e*)}
)
c (Conclusion): ∃e {f(e)=* A(e*)}
test(verbose=False): Method used to test the example
```

## new_e12
```
v (Views): (
   {A()},
   {}
)
c (Conclusion): {A()}
test(verbose=False): Method used to test the example
```

## new_e13
```
v (Views): (
   {f(12.0)=* A(12.0*),B()}
)
c (Conclusion): {}
prob (Probability): ∃e {A(e*)}
test(verbose=False): Method used to test the example
```

## new_e14
```
v (Views): (
   ∀x ∃y {B(g(x*,y))A(f(x*))},
   {A(f(j()*))}
)
c (Conclusion): ∃y {A(f(j()*))B(g(j()*,y))}
test(verbose=False): Method used to test the example
```

## new_e15
```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}
)
c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e16
```
v (Views): (
   ∃x ∃k {==(Clark(),x)Defeats(k,x)},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {==(Clark(),Clark())Defeats(k,Clark())}
test(verbose=False): Method used to test the example
```

## new_e17
```
v (Views): (
   ∃x ∃k {==(Clark(),x)do(Defeats(k,x))},
   ∃x {==(Clark()*,x)}
)
c (Conclusion): ∃k {==(Clark(),Clark())do(Defeats(k,Clark()))}
test(verbose=False): Method used to test the example
```

## new_e18
```
v (Views): (
   {m()=* A()},
   {n()=* B()}
)
c (Conclusion): {m()**n()=* B()A()}
test(verbose=False): Method used to test the example
```

## new_e19_first_atom_do_atom
```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {do(A())}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e20_nested_issue_in_pred
```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark(),f(Superman()*))}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e21_supp_is_something
```
v (Views): (
   ∃k {Defeats(k,Superman())==(Clark(),Superman())},
   {==(Clark()*,Superman())}^{}
)
c (Conclusion): ∃k {Defeats(k,Superman())==(Clark(),Superman())}
test(verbose=False): Method used to test the example
```

## new_e22_restrict_dep_rel_is_not_other
```
v (Views): (
   ∃x ∃k {==(Clark(),x)do(Defeats(k,x))},
   ∃y {==(Clark()*,y)}
)
c (Conclusion): ∃x ∃k {==(Clark(),x)do(Defeats(k,x))}
test(verbose=False): Method used to test the example
```

## AnswerPotential
```
v (Views): (
   {1.0=* 2.0=+ B()A(),0.4=* B()C(),C()A()},
   {A()},
   {B()},
   {C()},
   {D()C()},
   {C()~B()}
)
c (Conclusion): {}
test(verbose=False): Method used to test the example
```

## UniProduct
```
v (Views): (
   ∀x ∃a {E(x,a)P(x),~P(x*)},
   {P(j()*)}
)
c (Conclusion): ∃a {~P(j()*),P(j())E(j(),a)}
test(verbose=False): Method used to test the example
```

## QueryTest
```
description:
    From page 173
    
v (Views): (
   ∀x {S(j()*)T(x,m())S(m()*),S(m()*)S(j()*)T(x,j())},
   ∀x ∃a {S(a*)T(x,a)}
)
c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```

## QueryTest2
```
description:
    From page 173
    
v (Views): (
   ∀x {S(j()*)T(x,m())S(m()*),S(m()*)S(j()*)T(x,j())},
   ∃a ∀x {S(a*)T(x,a)}
)
c (Conclusion): ∀x ∃a {S(a*)T(x,a)}
test(verbose=False): Method used to test the example
```