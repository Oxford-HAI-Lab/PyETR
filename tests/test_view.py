import pytest

from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.view import View


def ps(s: str, custom_functions: list[NumFunc | Function] | None = None) -> View:
    return View.from_str(s, custom_functions)


class TestView:
    def test_view_hash(self):
        assert hash(View.get_falsum())

    def test_too_many_exis(self):
        v = (
            ps(
                "∀a ∃b ∃c ∃d ∃e ∃f ∃g ∃h ∃i ∃j ∃k ∃l ∃m ∃n ∃o ∃p ∃q ∃r ∃z {P(a)E(a,z),~P(a*), Q(b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r)}"
            ),
            ps("{P(j()*)}"),
        )
        c: View = ps(
            "∃ak ∃ac ∃aa ∃ab ∃ah ∃ae ∃x ∃w ∃y ∃s ∃u ∃ai ∃aj ∃t ∃ag ∃af ∃ad ∃v {~P(j()*),Q(aa,ac,ad,w,v,s,ae,x,ah,ai,af,t,y,ak,ag,ab,aj),E(j(),u)P(j())}"
        )

        result = v[0].universal_product(v[1])
        with pytest.raises(
            ValueError, match="Too many unis or exis to feasibly compute"
        ):
            result.is_equivalent_under_arb_sub(c)
