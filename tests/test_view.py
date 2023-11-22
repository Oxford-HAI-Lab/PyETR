from pyetr.view import View


class TestView:
    def test_view_hash(self):
        assert hash(View.get_falsum())
