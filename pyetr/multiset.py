from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


class Multiset(Generic[T]):
    _items: list[T]

    def __init__(self, items: list[T]) -> None:
        self._items = sorted(items, key=hash)

    def __iter__(self):
        return iter(self._items)

    def __next__(self):
        return next(self)

    def __repr__(self) -> str:
        return "Multiset(" + super().__repr__() + ")"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Multiset):
            return False
        return self._items == __value._items

    def __hash__(self) -> int:
        return hash("Multiset") + hash(tuple(self._items))


m = Multiset([1, 3, 2, 3, 3])
m2 = Multiset([2, 3, 3, 3, 1])
