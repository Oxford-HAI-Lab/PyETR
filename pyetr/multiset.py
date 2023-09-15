from typing import Generic, Hashable, Iterable, TypeVar

T = TypeVar("T", bound=Hashable)


class GenericMultiset(Generic[T]):
    _items: list[T]

    def __init__(self, items: Iterable[T]) -> None:
        self._items = sorted(items, key=hash)

    def __iter__(self):
        return iter(self._items)

    def __next__(self):
        return next(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__} (" + self._items.__repr__() + ")"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GenericMultiset):
            return False
        return self._items == __value._items

    def __hash__(self) -> int:
        return hash(type(self).__name__) + hash(tuple(self._items))

    def __len__(self):
        return len(self._items)

    @property
    def detailed(self):
        return f"<{type(self).__name__} items={self._items.__repr__()}>"
