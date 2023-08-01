from abc import ABCMeta, abstractmethod
from typing import ClassVar

from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View


class BaseExample(metaclass=ABCMeta):
    c: ClassVar[View]

    def __init__(self, views: list[str | View] | list[str] | list[View]) -> None:
        for v in views:
            if isinstance(v, View):
                pass

    @classmethod
    @abstractmethod
    def test(cls):
        raise NotImplementedError


class e1(BaseExample):
    """
    P1: Every archaeon has a nucleus; ∀x (P(x) → Q(x))
    P2: Halobacterium is an archeon; P(H)

    C: Halobacterium is an archaeon and has a nucleus; P(H) ∧ Q(H)

    """

    v = (ps("∀x (P(x) → Q(x))"), ps("P(H)"))
    c = ps("P(H) ∧ Q(H)")

    @classmethod
    def test(cls):
        print("here")
