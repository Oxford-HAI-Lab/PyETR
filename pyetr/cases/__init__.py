__all__ = ["e1"]
from abc import ABCMeta, abstractmethod
from typing import cast

from pyetr.inference import default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View


class BaseExample(metaclass=ABCMeta):
    v: tuple[View, ...]
    c: View

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
        assert isinstance(c, View)

    @classmethod
    @abstractmethod
    def test(cls):
        raise NotImplementedError


class e1(BaseExample):
    """
    P1: Every archaeon has a nucleus; ∀x (IsArcheon(x) → HasNucleus(x))
    P2: Halobacterium is an archeon; IsArcheon(Halobacterium())

    C: Halobacterium is an archaeon and has a nucleus; IsArcheon(Halobacterium()) ∧ HasNucleus(Halobacterium())
    """

    v: tuple[View, View] = (
        ps("∀x (IsArcheon(x) → HasNucleus(x))"),
        ps("IsArcheon(Halobacterium())"),
    )
    c: View = ps("IsArcheon(Halobacterium()) ∧ HasNucleus(Halobacterium())")

    @classmethod
    def test(cls):
        result = default_inference_procedure(cls.v)
        print(result)
        print(cls.c)
        assert result.is_equivalent_under_arb_sub(cls.c)
