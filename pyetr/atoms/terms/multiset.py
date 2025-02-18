from typing import Generic, Hashable, Iterable, TypeVar, cast

T = TypeVar("T", bound=Hashable)


class Multiset(Generic[T]):
    """
    A Generic Multiset of items
    """

    _items: list[T]

    def __init__(self, items: Iterable[T]) -> None:
        self._items = sorted(items, key=hash)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"⟪{','.join([repr(i) for i in self.sorted_iter()])}⟫"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Multiset):
            return False
        else:
            return self._items == cast(Multiset[T], __value)._items

    def __hash__(self) -> int:
        return hash(type(self).__name__) + hash(tuple(self._items))

    def __len__(self):
        return len(self._items)

    @property
    def detailed(self):
        return f"<{type(self).__name__} items={self._items.__repr__()}>"

    def __add__(self, other: "Multiset[T]") -> "Multiset[T]":
        return Multiset(self._items + other._items)

    def sorted_iter(self):
        return sorted(self, key=str)
