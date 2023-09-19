from abc import abstractmethod


class AbstractAtom:
    @property
    @abstractmethod
    def detailed(self) -> str:
        ...


class AbstractOpen(AbstractAtom):
    pass


class AbstractComplete(AbstractAtom):
    pass
