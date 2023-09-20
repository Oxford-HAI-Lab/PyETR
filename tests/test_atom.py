import pytest

from pyetr.atoms import Predicate, PredicateAtom


class TestAtom:
    def test_invalid(self):
        with pytest.raises(
            ValueError, match="Inconsistent - number of terms does not equal arity"
        ):
            PredicateAtom(predicate=Predicate(name="Fred", arity=1), terms=())

    def test_repr(self):
        atom = PredicateAtom(predicate=Predicate(name="Fred", arity=0), terms=())
        assert repr(atom) == "Fred()"
