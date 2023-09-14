from typing import Generic, Hashable, Iterable, TypeVar

T = TypeVar("T", bound=Hashable)


class Multiset(Generic[T]):
    _items: list[T]

    def __init__(self, items: Iterable[T]) -> None:
        self._items = sorted(items, key=hash)

    def __iter__(self):
        return iter(self._items)

    def __next__(self):
        return next(self)

    def __repr__(self) -> str:
        return "Multiset(" + self._items.__repr__() + ")"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Multiset):
            return False
        return self._items == __value._items

    def __hash__(self) -> int:
        return hash("Multiset") + hash(tuple(self._items))

    def __add__(self, other: "Multiset") -> "Multiset":
        raise NotImplementedError

    def __len__(self):
        return len(self._items)

    @property
    def detailed(self):
        return f"<Multiset items={self._items.__repr__()}>"
