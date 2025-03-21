from typing import Callable

from pyetr.atoms.predicate import Predicate
from pyetr.atoms.terms.abstract_term import AbstractArbitraryObject
from pyetr.atoms.terms.function import Function

MatchCallback = Callable[
    [AbstractArbitraryObject | Predicate | Function],
    AbstractArbitraryObject | Predicate | Function,
]
MatchItem = str | AbstractArbitraryObject | Function | Predicate
