import pytest

from pyetr.atom import Atom
from pyetr.abstract_atom import Predicate

class TestAtom:
    def test_invalid(self):
        with pytest.raises(
            ValueError, match="Inconsistent - number of terms does not equal arity"
        ):
            Atom(predicate=Predicate(name="Fred", arity=1), terms=())

    def test_repr(self):
        atom = Atom(predicate=Predicate(name="Fred", arity=0), terms=())
        assert repr(atom) == "Fred()"
